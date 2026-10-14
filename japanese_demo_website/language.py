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


# The same URL serves Japanese or English depending on the language cookie, but browsers cache by
# URL alone. Frappe's default (max-age=300 + stale-while-revalidate) would keep showing a page in
# the language it was first loaded in. "no-cache" makes the browser revalidate every time; Frappe's
# server-side page cache, which is keyed per language, still keeps these responses fast.
SITE_PAGE_CACHE_CONTROL = "private, no-cache"


def set_site_cache_headers(response, request) -> None:
	"""after_request hook. Edits frappe.local.response_headers because Frappe copies those onto the
	response after the hooks run, which would overwrite a header set on `response` directly."""
	if request.method not in ("GET", "HEAD"):
		return
	path = request.path
	if not is_site_path(path) or path.startswith(SITE_API_PREFIX):
		return
	frappe.local.response_headers["Cache-Control"] = SITE_PAGE_CACHE_CONTROL


def is_site_path(path: str) -> bool:
	path = path.rstrip("/") or "/"
	return path in SITE_ROUTES or path.startswith(SITE_ROUTE_PREFIXES) or path.startswith(SITE_API_PREFIX)


def resolve_site_language(query_lang: str | None, cookie_lang: str | None) -> str:
	for candidate in (query_lang, cookie_lang):
		if candidate in SITE_LANGUAGES:
			return candidate
	return DEFAULT_LANGUAGE
