# Backend layer

## Where things go

| Change | File |
|---|---|
| Validation, defaults, derived fields | DocType controller `japanese_demo_website/japanese_demo_website/doctype/<name>/<name>.py` (`validate`, `before_insert`, `before_submit`) |
| Form behavior, link filters (`frm.set_query` in `setup`) | `<name>.js` |
| HTTP endpoints | `japanese_demo_website/api.py` → `/api/method/japanese_demo_website.api.<fn>` |
| Row/list permission rules | `japanese_demo_website/permissions.py` + `has_permission` / `permission_query_conditions` in hooks.py |
| Events on DocTypes from other apps | `japanese_demo_website/events.py` → `handler(doc, method)` in `doc_events` |
| Scheduled jobs | `japanese_demo_website/tasks.py` + `scheduler_events` |
| Install/seed data | `japanese_demo_website/install.py` (`after_install`, `after_migrate`), idempotent with `frappe.db.exists` |
| Constants and status enums | `japanese_demo_website/constants.py` |

Keep hooks.py to registration only. Sibling examples of each pattern are in `../airplane_mode/airplane_mode/`.

## Data access

- `frappe.qb` + `frappe.query_builder.functions` for aggregates and joins.
- `frappe.db.get_value(dt, filters, fields, as_dict=True)`, `exists`, `count`, `get_single_value` for lookups.
- `get_list` applies permissions, so use it for user-facing lists. `get_all` ignores them, so use it for jobs, patches, and public content you deliberately publish (filter on a `published` field).
- Raw `frappe.db.sql` with `%(name)s` params only. Use `frappe.db.escape` for anything interpolated into `permission_query_conditions`.

## Writes and transactions

- Use `doc.insert()` / `doc.save()` by default. Use `db_set` / `frappe.db.set_value` only for flags and patch backfills.
- A request is one transaction: it commits on success and rolls back on an exception. Don't commit inside request handlers. Do commit in patches, the console, and long job loops.
- Wrap a multi-step write inside a job with `frappe.db.savepoint` / `rollback(save_point=...)`.
- Side effects (email, realtime, enqueue) use `after_commit=True` / `enqueue_after_commit=True`.
- `frappe.sendmail` goes through the Email Queue. Pass `reference_doctype`/`reference_name`.

## Errors and logging

- `frappe.throw(msg, exc)`: `PermissionError` → 403, `DoesNotExistError` → 404, `ValidationError` (the default) → 417.
- In jobs, wrap each item in `try/except` with `frappe.log_error(title=..., message=frappe.get_traceback())` and continue the loop.
- `frappe.logger("japanese_demo_website")` writes to the bench `logs/` folder.

## Statuses

- Desk `Select` options and Workflow State names are Frappe-native: Title Case, because Desk shows the stored value and workflows match on it.
- App-owned enums (API responses, job or sync states) are UPPERCASE constants in `constants.py`. Shown in Title Case or Japanese through one map in `public/js/website.js` (e.g. `japanese_demo_website.status_label(value)`) or one Jinja filter. Never hardcode labels per page.

## Event order (Document, v16)

Insert: `before_insert` → `autoname` → `before_validate` → `validate` → `before_save` → insert → `after_insert` → `on_update`.
Save: `before_validate` → `validate` → `before_save` → update → `on_update`. Submit: `before_submit` → `on_submit`. Cancel: `before_cancel` → `on_cancel`.
