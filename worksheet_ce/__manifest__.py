# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Worksheet CE',
    'category': 'Hidden',
    'summary': 'Create customizable worksheet',
    'description': """
Worksheet CE
============

Community Edition port of the ``worksheet`` module. A worksheet
template generates its own model, form, list and search views and a QWeb
report, so that performed work can be documented per record.

The upstream module depends on ``web_studio`` only for its editing
interface (the "Design Template" button, the Studio controller and the
Studio navbar patch). Those parts are removed here; the model layer is
portable and uses only Community Edition core APIs.
""",
    'version': '18.0.1.0.0',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'security/worksheet_security.xml',
        'views/worksheet_template_view.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'worksheet_ce/static/src/scss/worksheet_portal.scss',
        ],
    },
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
}
