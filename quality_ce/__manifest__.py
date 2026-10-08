# -*- encoding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Quality Base CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Basic Feature for Quality',
    'depends': ['stock'],
    'description': """
Quality Base CE
===============

Community Edition port of the ``quality`` module.

* Define quality points that will generate quality checks on pickings,
  manufacturing orders or work orders (quality_mrp_ce)
* Quality alerts can be created independently or related to quality checks
* Possibility to add a measure to the quality check with a min/max tolerance
* Define your stages for the quality alerts

The port is behaviour-preserving: models, views, security and assets are
kept, only the manifest and the xmlid prefix are changed
(``quality.`` -> ``quality_ce.``).
""",
    'data': [
        'security/quality.xml',
        'security/ir.model.access.csv',
        'data/mail_alias_data.xml',
        'data/quality_data.xml',
        'views/quality_views.xml',
    ],
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://github.com/vertelab/odoo-quality',
    'repository': 'https://github.com/vertelab/odoo-quality',
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'quality_ce/static/src/**/*',
        ],
        'web.qunit_suite_tests': [
            'quality_ce/static/tests/*.js',
        ],
    },
    'installable': True,
    'application': False,
}
