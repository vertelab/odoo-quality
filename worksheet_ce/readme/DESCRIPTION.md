# Worksheet CE

Community Edition port of the `worksheet` module. A worksheet
template generates its own model, form, list and search views and a QWeb
report, so that performed work can be documented per record.

## What it provides

- `worksheet.template` — a template bound to a **host model** (for example
  `quality.check`, `maintenance.request` or `project.task`).
- On creation, the template generates:
  - a custom model (`x_<host>_worksheet_template_<id>`),
  - a form, list and search view for that model,
  - an action to open the generated records,
  - access rights and record rules (own records / all records in group),
  - a QWeb report built from the generated form view.
- A unique constraint ensures at most one worksheet record per host record.

## Difference from the upstream module

The upstream module depends on `web_studio`. That dependency is only for
the **editing interface**: the "Design Template" button, the controller that
inherited the Studio controller, and the Studio navbar patch. Those parts are
removed here. The model layer is unchanged and uses only Community Edition
core APIs (`ir.model`, `ir.model.access`, `ir.rule`, `ir.ui.view`,
`tools.sql.add_constraint`).

## Editing a template without Studio

There is no graphical form designer. The generated model is an ordinary
custom model, so the form can be changed the same way any custom model is
changed:

- Add fields with **Technical → Database Structure → Fields**
  (`ir.model.fields`) on the generated model.
- Adjust the generated form view (`ir.ui.view`) directly, or extend it from
  another module.
- After changing the form, call `_generate_qweb_report_template()` on the
  template to rebuild the QWeb report from the current form.

A host module (such as `quality_control_worksheet_ce`) can also provide
default fields and a default form arch by implementing
`_default_<host_model>_template_fields()` and
`_default_<host_model>_worksheet_form_arch()`.

## Using it

1. Create a worksheet template and pick a host model.
2. The generated model and views appear immediately.
3. Open the template's **Worksheets** button to see the generated records.
4. Use **Analysis** to see the records grouped over time.
