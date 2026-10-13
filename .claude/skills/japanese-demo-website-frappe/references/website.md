# Website layer

## Layout to use (create folders as needed)

```
japanese_demo_website/
├── www/                     # route = file path: www/about.html -> /about, www/news/index.html -> /news
│   ├── index.html + index.py   # home page; set Website Settings > Home Page = "index" only if needed
│   └── contact.html + contact.py
├── templates/
│   ├── includes/            # partials: {% include "templates/includes/header.html" %}
│   └── web.html             # optional own base; pages use {% extends "templates/web.html" %}
├── public/css/website.css   # registered via web_include_css
├── public/js/website.js     # registered via web_include_js
└── locale/ja.po             # translations
```

## Pages

- `www/<page>.py` defines `get_context(context)`. Set `context.title`, `context.no_cache = 1` for dynamic data, and `context.metatags = {"description": ..., "image": ...}` for SEO.
- Use `context.no_cache` only when the page reads per-request data. Static pages benefit from the page cache.
- Dynamic routes go in `hooks.py`: `website_route_rules = [{"from_route": "/news/<slug>", "to_route": "news/article"}]`. Read the param from `frappe.form_dict.slug`. Sibling example: `airplane_mode/hooks.py` + `www/shops/shop.py`.
- Return a 404 with `raise frappe.DoesNotExistError` or `frappe.throw(..., frappe.DoesNotExistError)`. Check `frappe.session.user != "Guest"` for pages that need a login, and set `frappe.local.flags.redirect_location` + `raise frappe.Redirect` to send visitors to `/login`.
- Register CSS/JS in `hooks.py` (`web_include_css = "/assets/japanese_demo_website/css/website.css"`, same for js), then run `bench build --app japanese_demo_website`.

## Forms that collect visitor data

Prefer a Web Form on a DocType (e.g. "Inquiry") when a standard form is enough. For a custom form, POST to a guest whitelisted method:

```python
from frappe.rate_limiter import rate_limit

@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=5, seconds=60 * 60)
def submit_inquiry(full_name: str, email: str, message: str):
	frappe.utils.validate_email_address(email, throw=True)
	if not full_name.strip() or len(message) > 5000:
		frappe.throw(_("Please check the form"))
	doc = frappe.get_doc({"doctype": "Inquiry", "full_name": full_name.strip(), "email": email, "message": message})
	doc.insert(ignore_permissions=True)  # guest insert; fields above are the allowlist
	return {"status": "RECEIVED"}
```

In page JS, call it with `frappe.call({method: "japanese_demo_website.api.submit_inquiry", args, type: "POST"})`, which sends the CSRF token for you.

## Translations (v16 uses gettext)

1. Wrap strings: Python `_("Contact us")`, Jinja `{{ _("Contact us") }}`, JS `__("Contact us")`.
2. Run `bench generate-pot-file --app japanese_demo_website`, which writes `locale/main.pot`.
3. The first time only: `bench create-po-file ja --app japanese_demo_website`. After that, use `bench update-po-files --app japanese_demo_website --locale ja`.
4. Fill in `msgstr` in `locale/ja.po`, then run `bench compile-po-to-mo --app japanese_demo_website --locale ja`.
5. The visitor language comes from the `preferred_language` cookie, `Accept-Language`, or `?_lang=ja`. Website Settings → Default Language sets the default.

## Japanese typography and content

- Set `lang="ja"` on `<html>` in the base template. Use a JP font stack such as `"Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif` and load only the weights you use. Japanese fonts are large, so subset or `display=swap`.
- Use body line-height 1.7-1.9 and `line-break: strict;`. Use `word-break: keep-all` only on short headings, because it can overflow narrow screens.
- Don't fake italics for emphasis (CJK fonts have none). Use weight or color instead.
- Format dates as `YYYY年M月D日` through one formatter, and prices as `¥1,000` (JPY has no decimals) with `frappe.utils.fmt_money(amount, currency="JPY")`.
- Copy should be specific and polite (です/ます). Don't machine-translate English marketing phrases into Japanese without a review.
