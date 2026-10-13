# Bench and tests

Bench runs in Docker through Frappe Manager. Run commands inside the container:

```bash
fm shell mybench.localhost
fm shell mybench.localhost -c "bench --site mybench.localhost migrate"
```

| When | Command |
|---|---|
| First time (app not installed yet) | `bench --site mybench.localhost install-app japanese_demo_website` |
| DocType JSON, patches, fixtures changed | `bench --site mybench.localhost migrate` |
| hooks.py / templates changed | `bench --site mybench.localhost clear-cache` (+ `clear-website-cache` for pages) |
| `public/` CSS/JS changed | `bench build --app japanese_demo_website` |
| Translations changed | `bench compile-po-to-mo --app japanese_demo_website --locale ja` |
| Export fixtures | `bench --site mybench.localhost export-fixtures --app japanese_demo_website` |
| Run a job now | `bench --site mybench.localhost execute japanese_demo_website.tasks.<fn>` |
| Tests | `bench --site mybench.localhost run-tests --app japanese_demo_website` |

The site is at `http://mybench.localhost`. `developer_mode` is on, so Desk edits to standard DocTypes are written back to the app folder.

## Tests

- In v16, subclass `frappe.tests.IntegrationTestCase` (DB-backed) or `frappe.tests.UnitTestCase`. Put the file next to the DocType as `test_<doctype>.py`, or at `japanese_demo_website/tests/test_<area>.py` for API and page tests.
- Test guest endpoints with `frappe.set_user("Guest")`, and restore with `frappe.set_user("Administrator")` in `tearDown`.
- Don't commit in tests. IntegrationTestCase rolls back.

## Lint

pre-commit runs ruff, eslint, prettier and pyupgrade (`.pre-commit-config.yaml`). Python: tabs, double quotes, line length 110. CI: `.github/workflows/ci.yml` (tests) and `linter.yml` (semgrep + pip-audit).
