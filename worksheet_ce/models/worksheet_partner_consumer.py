# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class WorksheetTemplate(models.Model):
    """Consumer hooks for ``res.partner`` worksheet templates.

    ``worksheet.template`` (the model layer ported from the upstream module) is
    an abstract
    template module: ``_generate_worksheet_model()`` requires the consumer to
    implement four hooks per host model:

        _get_<res_model>_manager_group
        _get_<res_model>_user_group
        _get_<res_model>_access_all_groups
        _get_<res_model>_module_name

    In the upstream module those hooks live in the consumer module — ``quality_control_worksheet``
    (``_get_quality_check_*``), ``maintenance_worksheet``
    (``_get_maintenance_request_*``) and ``industry_fsm_report``
    (``_get_project_task_*``). ``worksheet_ce`` itself implements none of them.

    This module ships a ``res.partner`` consumer so that a worksheet template
    can be created out of the box on CE, and so the model layer is testable.
    Modules that add other host models (quality, maintenance, field service)
    implement their own hooks in their own repos.
    """

    _inherit = 'worksheet.template'

    @api.model
    def _get_res_partner_manager_group(self):
        return self.env.ref('base.group_partner_manager')

    @api.model
    def _get_res_partner_user_group(self):
        return self.env.ref('base.group_user')

    @api.model
    def _get_res_partner_access_all_groups(self):
        return self.env.ref('base.group_partner_manager')

    @api.model
    def _get_res_partner_module_name(self):
        return 'worksheet_ce'
