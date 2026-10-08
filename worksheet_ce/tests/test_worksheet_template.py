# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import psycopg2

from odoo import Command, api, models
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, TransactionCase
from odoo.tools import mute_logger


class TestWorksheetTemplate(TransactionCase):
    """Server-side tests for the worksheet template model layer.

    The generated model is a real custom model, so these tests run in test
    mode and reset the registry afterwards (same pattern as
    ``base.tests.test_ir_model.TestIrModel``).

    ``worksheet.template`` is an abstract template module: it does not
    implement the per-host-model hooks (``_get_<model>_manager_group`` etc.)
    itself. Those are provided by the consumer module — in the upstream module by
    ``quality_control_worksheet`` (``_get_quality_check_*``),
    ``maintenance_worksheet`` (``_get_maintenance_request_*``) and
    ``industry_fsm_report`` (``_get_project_task_*``).

    This test plays the role of such a consumer for ``res.partner``: the
    hooks live in ``TestWorksheetConsumer`` below (a real ``_inherit``),
    because Odoo's test loader rejects attributes added to a model at
    runtime.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The test mode is necessary because the worksheet template creates
        # custom models and fields. ``registry.reset_changes()`` after each
        # test opens a new cursor to retrieve the custom models; a regular
        # cursor would correspond to the database state before setUpClass().
        cls.registry.enter_test_mode(cls.cr)
        cls.addClassCleanup(cls.registry.leave_test_mode)

    def setUp(self):
        self.addCleanup(self.registry.reset_changes)
        super().setUp()

    def _create_template(self, name='Test Worksheet', res_model='res.partner'):
        return self.env['worksheet.template'].create({
            'name': name,
            'res_model': res_model,
        })

    # ------------------------------------------------------------------
    # Requirement: Skapa arbetsbladsmall
    # ------------------------------------------------------------------

    def test_create_generates_model_and_views(self):
        """A template generates a model, form/list/search views and an action."""
        template = self._create_template()
        self.assertTrue(template.model_id, "A model must be generated for the template")
        self.assertEqual(template.model_id.state, 'manual')
        self.assertTrue(template.action_id, "An action must be generated for the template")

        model_name = template.model_id.model
        views = self.env['ir.ui.view'].search([('model', '=', model_name)])
        self.assertEqual(
            set(views.mapped('type')),
            {'form', 'list', 'search'},
            "A form, list and search view must be generated",
        )
        self.assertEqual(template.action_id.res_model, model_name)

    def test_generated_model_has_host_field(self):
        """The generated model links back to the host record with a required m2o."""
        template = self._create_template()
        model_name = template.model_id.model
        host_field = self.env['ir.model.fields'].search([
            ('model_id', '=', template.model_id.id),
            ('name', '=', 'x_res_partner_id'),
        ])
        self.assertTrue(host_field, "The host link field must exist on the generated model")
        self.assertEqual(host_field.ttype, 'many2one')
        self.assertEqual(host_field.relation, 'res.partner')
        self.assertTrue(host_field.required, "The host link field must be required")
        self.assertEqual(host_field.on_delete, 'cascade')
        self.assertIn(model_name, self.env)

    # ------------------------------------------------------------------
    # Requirement: Länk mellan mall och värdpost
    # ------------------------------------------------------------------

    def test_one_worksheet_per_host_record(self):
        """A unique SQL constraint allows only one worksheet per host record."""
        template = self._create_template()
        model_name = template.model_id.model
        partner = self.env['res.partner'].create({'name': 'Host A'})
        self.env[model_name].create({'x_res_partner_id': partner.id})
        with self.assertRaises(psycopg2.IntegrityError), mute_logger('odoo.sql_db'):
            self.env[model_name].create({'x_res_partner_id': partner.id})

    # ------------------------------------------------------------------
    # Requirement: Egna fält i mallen
    # ------------------------------------------------------------------

    def test_custom_field_becomes_part_of_model(self):
        """A custom field added to the model is part of the generated model."""
        template = self._create_template()
        self.env['ir.model.fields'].create({
            'name': 'x_note',
            'ttype': 'char',
            'field_description': 'Note',
            'model_id': template.model_id.id,
        })
        self.assertIn('x_note', self.env[template.model_id.model]._fields)

    # ------------------------------------------------------------------
    # Requirement: Rapport per mall
    # ------------------------------------------------------------------

    def test_report_generated_from_form(self):
        """A QWeb report is generated from the template's form view."""
        template = self._create_template()
        self.assertTrue(template.report_view_id, "A report view must be generated")
        self.assertEqual(template.report_view_id.type, 'qweb')
        # ``ir.ui.view.arch`` is a str in Odoo 18 (it was bytes before 17.0).
        arch = template.report_view_id.arch
        if isinstance(arch, bytes):
            arch = arch.decode()
        self.assertIn('x_comments', arch)

    def test_report_view_type_checked(self):
        """A non-QWeb report view is rejected."""
        template = self._create_template()
        bad_view = self.env['ir.ui.view'].create({
            'name': 'not qweb',
            'type': 'form',
            'model': template.model_id.model,
            'arch': '<form/>',
        })
        with self.assertRaises(ValidationError):
            template.report_view_id = bad_view

    # ------------------------------------------------------------------
    # Requirement: Åtkomst per roll
    # ------------------------------------------------------------------

    def test_access_and_rules_generated(self):
        """Access rights and record rules are generated for the model."""
        template = self._create_template()
        accesses = self.env['ir.model.access'].search([('model_id', '=', template.model_id.id)])
        self.assertEqual(len(accesses), 2, "A manager and a user access rule must exist")
        rules = self.env['ir.rule'].search([('model_id', '=', template.model_id.id)])
        self.assertEqual(len(rules), 2, "An 'own' and an 'all' record rule must exist")
        self.assertIn("create_uid", rules[0].domain_force + rules[1].domain_force)

    # ------------------------------------------------------------------
    # Requirement: Multi-company-avgränsning
    # ------------------------------------------------------------------

    def test_companyless_template_available(self):
        """A template without a company is available for every company."""
        template = self._create_template()
        self.assertFalse(template.company_id)
        self.assertTrue(
            self.env['worksheet.template'].search([('id', '=', template.id)]),
            "A companyless template must be visible",
        )

    # ------------------------------------------------------------------
    # Requirement: Borttagning städar genererat innehåll
    # ------------------------------------------------------------------

    def test_unlink_cleans_generated_content(self):
        """Unlinking a template removes its model, views, rules and action."""
        template = self._create_template()
        model = template.model_id
        model_name = model.model
        action = template.action_id
        report = template.report_view_id

        template.unlink()

        self.assertFalse(model.exists(), "The generated model must be removed")
        self.assertFalse(action.exists(), "The generated action must be removed")
        self.assertFalse(report.exists(), "The generated report must be removed")
        self.assertFalse(
            self.env['ir.ui.view'].search([('model', '=', model_name)]),
            "The generated views must be removed",
        )
        self.assertFalse(
            self.env['ir.rule'].search([('model_id', '=', model.id)]),
            "The generated record rules must be removed",
        )
        self.assertFalse(
            self.env['ir.model.access'].search([('model_id', '=', model.id)]),
            "The generated access rules must be removed",
        )

    # ------------------------------------------------------------------
    # Requirement: Arbetsblad utan Studio
    # ------------------------------------------------------------------

    def test_no_studio_dependency(self):
        """The module must not depend on web_studio."""
        module = self.env['ir.module.module'].search([('name', '=', 'worksheet_ce')])
        self.assertTrue(module)
        self.assertNotIn('web_studio', module.dependencies_id.mapped('name'))
        self.assertFalse(
            self.env['ir.module.module'].search([('name', '=', 'web_studio'), ('state', '=', 'installed')]),
            "web_studio must not be installed in this test database",
        )

    def test_copy_forces_no_model(self):
        """Copying a template must generate a fresh model, not reuse the host model."""
        template = self._create_template()
        copied = template.copy()
        # ``copy()`` forces ``model_id=False`` before creating the copy, so the
        # copy generates its own model rather than sharing the original's.
        self.assertTrue(copied.model_id, "The copy must generate its own model")
        self.assertNotEqual(
            copied.model_id, template.model_id,
            "The copy must not reuse the original's generated model",
        )

    def test_analysis_report_action(self):
        """The analysis action targets the generated model."""
        template = self._create_template()
        action = template.action_analysis_report()
        self.assertEqual(action['res_model'], template.model_id.model)
        self.assertIn('graph', action['view_mode'])
