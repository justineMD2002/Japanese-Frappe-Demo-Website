---
name: japanese-demo-website-frappe
description: Conventions for the japanese_demo_website Frappe v16 custom app (module "Japanese Demo Website"), a public demo website for a Japanese prospect. Use for any change in this repo - hooks.py, www/ pages and their .py get_context, templates/, public/ CSS/JS, web_include_css/js, website_route_rules, Web Page / Web Form / Website Settings / Website Theme, DocTypes and controllers under japanese_demo_website/japanese_demo_website/doctype/, whitelisted methods (contact or inquiry forms, guest APIs), Japanese translations (locale/ja.po), patches, fixtures, scheduler jobs, and tests. Also use when adding a page, a form that collects visitor data, a status field, or seed content for this site.
---

# japanese_demo_website (Frappe v16.33)

A custom app on bench `frappe-bench` (Frappe Manager, site `mybench.localhost`). Python 3.14, ruff with tabs + double quotes, line length 110 (`pyproject.toml`). Module folder: `japanese_demo_website/japanese_demo_website/`. Frappe core is at `../frappe` (v16.33.0). Read it to check an API, but never edit it.

**Current state:** the app is a fresh scaffold, only `hooks.py`, `modules.txt` and `patches.txt`. It is **not installed** on the site yet, so run `bench --site mybench.localhost install-app japanese_demo_website` before anything renders. For fuller patterns, use the sibling app `../airplane_mode` as the reference: `api.py`, `permissions.py`, `tasks.py`, `install.py`, `www/shops/`.

## Hard rules

1. **Custom app only.** Never modify `apps/frappe`. Change core behavior with hooks, `doc_events`, `override_doctype_class` (subclass and call `super()`), or fixtures.
2. **Pages are code, not Desk records.** Put pages in `japanese_demo_website/www/<route>.html` + `<route>.py`, with shared layout in `japanese_demo_website/templates/`. Use Desk "Web Page" records only for content the client edits, and ship them as fixtures. Read `references/website.md` before building any page.
3. **Japanese first.** All visitor-facing text is wrapped in `_()` / `{{ _("...") }}` / `__()` with English source strings, and the Japanese goes in `japanese_demo_website/locale/ja.po`. Frappe core ships no `ja.po`, so Desk labels stay English. See `references/website.md` → Translations.
4. **Visitor input is untrusted.** Guest endpoints use `@frappe.whitelist(allow_guest=True, methods=["POST"])`, typed args, server-side validation, a rate limit (`@rate_limit`), and an explicit field allowlist on insert. Never return `"*"` to guests.
5. **Logged-in endpoints check permissions explicitly:** `frappe.has_permission(dt, ptype, throw=True)` or `doc.check_permission(...)`. `@frappe.whitelist()` doesn't do it for you.
6. **Data access:** use `frappe.qb` for aggregates and joins, and `frappe.db.get_value`/`exists`/`count` for lookups. Use `get_list` for user-facing lists, and `get_all` only for public website content you deliberately expose, or for jobs. Raw SQL uses `%(name)s` params. Details: `references/backend.md`.
7. **Schema and data ship as code:** DocType JSON (Desk with `developer_mode`, which is on), patches in `patches/v<major>_<minor>/` registered in `patches.txt`, and `fixtures` filtered by name. Install, migrate and job code is idempotent.
8. **Statuses:** Desk `Select` and Workflow values are Frappe-native, so they use Title Case. App-owned enums (API payloads, job states, constants in `japanese_demo_website/constants.py`) are UPPERCASE and shown in Title Case/Japanese through one shared label map. See `references/backend.md` → Statuses.
9. **UI** follows the global UI rules and `DESIGN.md` if the repo has one. Japanese typography specifics are in `references/website.md`.

## References

- `references/website.md`: www pages, routing, templates, assets, Website Settings/Theme, translations, Japanese typography, SEO.
- `references/backend.md`: hooks, controllers, whitelisted methods, permissions, transactions, statuses, scheduler.
- `references/bench-and-tests.md`: `fm shell`, bench commands, tests, lint.

## Before you finish

- Run `ruff check` / `ruff format` on the Python files you touched.
- List the bench commands the change needs: `migrate` for JSON, patches and fixtures; `clear-cache` for hooks and templates; `build --app japanese_demo_website` for `public/`; `compile-po-to-mo --app japanese_demo_website --locale ja` for translations.
