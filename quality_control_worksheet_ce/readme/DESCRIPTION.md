# Worksheet for Quality Control CE

Community Edition port of the `quality_control_worksheet` module.
It adds a **worksheet-based check type** to `quality_control_ce`: a quality
point can be configured with a worksheet template, the worksheet is filled in
from the quality check wizard, and the worksheet's success conditions decide
whether the check passes or fails.

## What it provides

- A new test type `worksheet` (`quality.point.test_type`).
- `worksheet.template` on `quality.point` and `quality.check`, with a
  `worksheet_success_conditions` domain that is evaluated against the filled
  worksheet.
- The check wizard opens the worksheet form; the **Validate** button saves the
  worksheet and passes or fails the check based on the success conditions.
- Back-to-back navigation between multiple worksheet checks on the same
  operation.
- A worksheet section appended to the quality worksheet QWeb report.

## Consumer hooks

`worksheet_ce` requires the consumer module to implement four hooks per host
model. This module implements them for `quality.check`:

| Hook | Returns |
|---|---|
| `_get_quality_check_manager_group` | `quality_ce.group_quality_manager` |
| `_get_quality_check_user_group` | `quality_ce.group_quality_user` |
| `_get_quality_check_access_all_groups` | `quality_ce.group_quality_manager` |
| `_get_quality_check_module_name` | `quality_control_worksheet_ce` |

The upstream version used the `quality` / `quality_control` xmlids; here
they point at `quality_ce` / `quality_control_ce`.

## Difference from the upstream module

The port is behaviour-preserving. The xmlid prefix is changed
(`quality_control_worksheet.` -> `quality_control_worksheet_ce.`) and
cross-module references point at `worksheet_ce`, `quality_ce` and
`quality_control_ce`.
