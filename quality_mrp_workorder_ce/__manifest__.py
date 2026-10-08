# -*- encoding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'MRP features for Quality Control CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Quality Management with MRP',
    'depends': ['quality_control_ce', 'mrp_workorder_ce', 'barcodes'],
    'description': """
MRP features for Quality Control CE
===================================

Community Edition port of the ``quality_mrp_workorder`` module
Adds quality control to work orders: quality checks on the Shop
Floor display, the work-order tablet view and the operation-level
filtering of checks.

The upstream module references a template-based check type from the
optional add-on. As in ``quality_control_ce`` that support is dropped:
the check-icon patch, the confirmation-dialog extension and the tour are
removed.

The port is otherwise behaviour-preserving; the xmlid prefix is changed
(``quality_mrp_workorder.`` -> ``quality_mrp_workorder_ce.``) and the
cross-module references point at ``quality_ce`` / ``quality_control_ce``.
""",
    "data": [
        'views/quality_views.xml',
        'views/mrp_workorder_views.xml',
        'report/worksheet_custom_report_templates.xml',
    ],
    "demo": [
        'data/mrp_workorder_demo.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'quality_mrp_workorder_ce/static/src/**/*.xml',
            'quality_mrp_workorder_ce/static/src/**/*.js',
        ],
        'web.assets_tests': [
            'quality_mrp_workorder_ce/static/tests/tours/**/*',
        ],
    },
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'auto_install': True,
    'license': 'AGPL-3',
    'installable': True,
}
