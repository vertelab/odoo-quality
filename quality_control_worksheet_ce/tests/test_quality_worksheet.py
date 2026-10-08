# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import Command
from odoo.exceptions import UserError
from odoo.tests.common import tagged, HttpCase, TransactionCase

from odoo.addons.quality_control_ce.tests.test_common import TestQualityCommon


@tagged('post_install', '-at_install')
class TestQualityWorksheet(HttpCase, TestQualityCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.worksheet_template = cls.env['worksheet.template'].create({
            'name': 'Quality worksheet',
            'res_model': 'quality.check',
        })
        cls.receipt_type = cls.env.ref('stock.picking_type_in')
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.supplier_location = cls.env.ref('stock.stock_location_suppliers')

    def test_multiple_worksheet_checks(self):
        """ Have a receipt for two product, to trigger quality checks for each product.
            the two worksheet should be opened back to back for completion
        """
        self.env['quality.point'].create({
            'name': 'QP1',
            'measure_on': 'move_line',
            'test_type_id': self.env.ref('quality_control_worksheet_ce.test_type_worksheet').id,
            'worksheet_template_id': self.worksheet_template.id,
            'picking_type_ids': [Command.link(self.receipt_type.id)],
            'worksheet_success_conditions': "[('x_passed', '=', True)]",
            'failure_location_ids': [Command.link(self.failure_location.id)]
        })

        receipt = self.env['stock.picking'].create({
            'picking_type_id': self.receipt_type.id,
            'location_id': self.supplier_location.id,
            'location_dest_id': self.stock_location.id,
        })

        self.env['stock.move'].create([
            {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 2,
                'picking_id': receipt.id,
                'location_id': receipt.location_id.id,
                'location_dest_id': receipt.location_dest_id.id,
            },
            {
                'name': self.product_2.name,
                'product_id': self.product_2.id,
                'product_uom_qty': 2,
                'picking_id': receipt.id,
                'location_id': receipt.location_id.id,
                'location_dest_id': receipt.location_dest_id.id,
            }
        ])
        receipt.action_confirm()
        self.assertEqual(len(receipt.check_ids), 2)
        # launch tour to test the worksheets opening back to back
        action = self.env.ref('stock.action_picking_tree_all')
        action['res_id'] = receipt.id
        action['view_id'] = self.env.ref('stock.view_picking_form')
        url = f'/odoo/{receipt.id}/action-{action.id}'
        self.start_tour(url, 'test_multiple_worksheet_checks', login='admin')
        # there should be 3 move lines and 3 checks
        self.assertEqual(len(receipt.move_line_ids), 3)
        self.assertRecordValues(receipt.check_ids, [
            {'quality_state': 'fail', 'product_id': self.product.id, 'qty_line': 1, 'failure_location_id': self.failure_location.id},
            {'quality_state': 'pass', 'product_id': self.product_2.id, 'qty_line': 2, 'failure_location_id': False},
            {'quality_state': 'pass', 'product_id': self.product.id, 'qty_line': 1, 'failure_location_id': False},
        ])


@tagged('post_install', '-at_install')
class TestQualityWorksheetMechanism(TestQualityCommon):
    """Server-side coverage of the worksheet check mechanism (no browser).

    The tour above needs ``websocket-client``; these tests exercise the same
    behaviour through the ORM so the mechanism is verified in every run: the
    worksheet value drives the check result through
    ``worksheet_success_conditions``.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The worksheet template creates a real custom model, so run in test
        # mode and reset the registry afterwards (same pattern as the
        # ``worksheet_ce`` tests).
        cls.registry.enter_test_mode(cls.cr)
        cls.addClassCleanup(cls.registry.leave_test_mode)
        cls.worksheet_template = cls.env['worksheet.template'].create({
            'name': 'Quality worksheet',
            'res_model': 'quality.check',
        })
        cls.receipt_type = cls.env.ref('stock.picking_type_in')
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.supplier_location = cls.env.ref('stock.stock_location_suppliers')

    def setUp(self):
        self.addCleanup(self.registry.reset_changes)
        super().setUp()

    def _create_worksheet_check(self, success_conditions="[('x_passed', '=', True)]"):
        point = self.env['quality.point'].create({
            'name': 'Worksheet point',
            'test_type_id': self.env.ref('quality_control_worksheet_ce.test_type_worksheet').id,
            'worksheet_template_id': self.worksheet_template.id,
            'picking_type_ids': [Command.link(self.receipt_type.id)],
            'worksheet_success_conditions': success_conditions,
        })
        receipt = self.env['stock.picking'].create({
            'picking_type_id': self.receipt_type.id,
            'location_id': self.supplier_location.id,
            'location_dest_id': self.stock_location.id,
        })
        self.env['stock.move'].create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'picking_id': receipt.id,
            'location_id': receipt.location_id.id,
            'location_dest_id': receipt.location_dest_id.id,
        })
        receipt.action_confirm()
        check = receipt.check_ids
        self.assertEqual(len(check), 1)
        self.assertEqual(check.test_type, 'worksheet')
        self.assertEqual(check.worksheet_template_id, self.worksheet_template)
        return check

    def _fill_worksheet(self, check, **values):
        model_name = self.worksheet_template.model_id.model
        return self.env[model_name].create({
            'x_quality_check_id': check.id,
            **values,
        })

    def test_worksheet_count_tracks_filled_worksheet(self):
        """The check's worksheet count reflects the filled worksheet."""
        check = self._create_worksheet_check()
        self.assertEqual(check.worksheet_count, 0)
        self._fill_worksheet(check, x_passed=True)
        # ``worksheet_count`` is a non-stored computed field; the UI reads it
        # from a fresh environment. Invalidate to mimic that (the dependency
        # ``worksheet_template_id`` does not change when a worksheet is filled).
        check.invalidate_recordset(['worksheet_count'])
        self.assertEqual(check.worksheet_count, 1)

    def test_worksheet_validation_passes(self):
        """A worksheet matching the success conditions passes the check."""
        check = self._create_worksheet_check()
        self._fill_worksheet(check, x_passed=True)
        wizard = self.env['quality.check.wizard'].create({
            'check_ids': [Command.set(check.ids)],
            'current_check_id': check.id,
        })
        check.with_context(quality_wizard_id=wizard.id).action_worksheet_check()
        self.assertEqual(check.quality_state, 'pass')

    def test_worksheet_validation_fails(self):
        """A worksheet not matching the success conditions fails the check."""
        check = self._create_worksheet_check()
        self._fill_worksheet(check, x_passed=False)
        wizard = self.env['quality.check.wizard'].create({
            'check_ids': [Command.set(check.ids)],
            'current_check_id': check.id,
        })
        check.with_context(quality_wizard_id=wizard.id).action_worksheet_check()
        self.assertEqual(check.quality_state, 'fail')

    def test_worksheet_validation_requires_filled_worksheet(self):
        """Validating without filling the worksheet is rejected."""
        check = self._create_worksheet_check()
        wizard = self.env['quality.check.wizard'].create({
            'check_ids': [Command.set(check.ids)],
            'current_check_id': check.id,
        })
        with self.assertRaises(UserError):
            check.with_context(quality_wizard_id=wizard.id).action_worksheet_check()

    def test_worksheet_is_pass_fail_applicable(self):
        """A worksheet check supports pass/fail buttons."""
        check = self._create_worksheet_check()
        self.assertTrue(check._is_pass_fail_applicable())
