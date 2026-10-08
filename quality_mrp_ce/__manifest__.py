# -*- encoding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'MRP features for Quality Control CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Quality Management with MRP',
    'depends': ['quality_control_ce', 'mrp'],
    'description': """
MRP features for Quality Control CE
===================================

Community Edition port of the ``quality_mrp`` module.
Adds workcenters and manufacturing orders to the quality control
framework: quality checks generated on manufacturing orders, the
manufacturing-order smart button and the MRP worksheet report.

The port is behaviour-preserving; the xmlid prefix is changed
(``quality_mrp.`` -> ``quality_mrp_ce.``) and the cross-module references
point at ``quality_ce`` / ``quality_control_ce``.
""",
    "data": [
        'security/quality_mrp.xml',
        'views/quality_views.xml',
        'views/mrp_production_views.xml',
        'report/worksheet_custom_report_templates.xml',
        'wizard/on_demand_quality_check_wizard_views.xml',
    ],
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'auto_install': True,
    'license': 'AGPL-3',
    'installable': True,
}
