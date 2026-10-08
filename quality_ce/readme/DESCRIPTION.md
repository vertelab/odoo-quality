Quality Base CE
===============

Community Edition port of the ``quality`` module.

Defines the quality data model: quality points, quality checks, quality
alerts (with teams, stages and reasons) and quality tags. The checks are
generated on stock operations; the MRP integration lives in
``quality_mrp_ce`` and the work-order integration in
``quality_mrp_workorder_ce``.

Ported from the upstream ``quality`` module to AGPL-3.
The port is behaviour-preserving; only the manifest and the xmlid prefix
(``quality.`` -> ``quality_ce.``) differ from the original.
