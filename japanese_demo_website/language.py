"""Japanese-first language rule for this app's public pages (registered as a before_request hook).

Frappe core falls back to the browser's Accept-Language for guests, which would show English to
most people viewing the demo. On our own routes we instead use: ?_lang= > language cookie > Japanese.
"""

import frappe

from japanese_demo_website.constants import (
	DEFAULT_LANGUAGE,
	LANGUAGE_COOKIE,
	SITE_API_PREFIX,
	SITE_LANGUAGES,
	SITE_ROUTE_PREFIXES,
	SITE_ROUTES,
)


def set_site_language() -> None:
	request = getattr(frappe.local, "request", None)
	if not request or not is_site_path(request.path):
		return

	frappe.local.lang = resolve_site_language(
		frappe.form_dict.get("_lang"), request.cookies.get(LANGUAGE_COOKIE)
	)


def is_site_path(path: str) -> bool:
	path = path.rstrip("/") or "/"
	return path in SITE_ROUTES or path.startswith(SITE_ROUTE_PREFIXES) or path.startswith(SITE_API_PREFIX)


def resolve_site_language(query_lang: str | None, cookie_lang: str | None) -> str:
	for candidate in (query_lang, cookie_lang):
		if candidate in SITE_LANGUAGES:
			return candidate
	return DEFAULT_LANGUAGE
