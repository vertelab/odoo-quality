# -*- encoding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Quality Control CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 120,
    'summary': 'Control the quality of your products',
    'depends': ['quality_ce'],
    'description': """
Quality Control CE
==================

Community Edition port of the ``quality_control`` module
Adds the quality control framework on top of ``quality_ce``:
control points generate checks on pickings, manufacturing orders or work
orders (``quality_mrp_ce``), checks can be passed, failed or measured, and
quality alerts can be created from a check.

The upstream module depends on an additional module for an
optional, template-based check type. That dependency is removed here
together with its two models, its views, menu, security rules, assets and
tests. All remaining check types (pass/fail, measure, instructions,
picture) work unchanged.

The port is otherwise behaviour-preserving; the xmlid prefix is changed
(``quality_control.`` -> ``quality_control_ce.``).
""",
    'data': [
        'data/quality_control_data.xml',
        'report/worksheet_custom_reports.xml',
        'report/worksheet_custom_report_templates.xml',
        'views/quality_views.xml',
        'views/product_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_lot_views.xml',
        'wizard/quality_check_wizard_views.xml',
        'wizard/on_demand_quality_check_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/quality_control_demo.xml',
    ],
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'application': True,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'quality_control_ce/static/src/**/*',
        ],
    },
    'installable': True,
}
