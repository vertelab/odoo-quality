# -*- encoding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Worksheet for Quality Control CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Create custom worksheet for quality control',
    'depends': ['quality_control_ce', 'worksheet_ce'],
    'description': """
Worksheet for Quality Control CE
================================

Community Edition port of the ``quality_control_worksheet``
module. Adds a worksheet-based check type to ``quality_control_ce``:
a worksheet template is attached to a quality point, the worksheet is filled
in from the check wizard, and its success conditions decide whether the check
passes or fails.

The module implements the four consumer hooks that ``worksheet_ce`` requires
for the ``quality.check`` host model (manager group, user group, access-all
groups and module name). The upstream version used the ``quality`` and
``quality_control`` groups and xmlids; here they point at ``quality_ce`` and
``quality_control_ce``.

The port is otherwise behaviour-preserving; the xmlid prefix is changed
(``quality_control_worksheet.`` -> ``quality_control_worksheet_ce.``) and
cross-module references point at ``worksheet_ce`` / ``quality_ce`` /
``quality_control_ce``.
""",
    'data': [
        'security/quality_control_security.xml',
        'security/ir.model.access.csv',
        'data/quality_control_data.xml',
        'views/quality_views.xml',
        'views/worksheet_template_views.xml',
        'report/worksheet_custom_report_templates.xml',
    ],
    'demo': [
        'data/quality_worksheet_demo.xml',
    ],
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'quality_control_worksheet_ce/static/src/**/*',
        ],
        'web.assets_tests': [
            'quality_control_worksheet_ce/static/tests/tours/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
