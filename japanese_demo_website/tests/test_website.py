from types import SimpleNamespace

import frappe
from frappe.tests import UnitTestCase
from werkzeug.datastructures import Headers

from japanese_demo_website.language import (
	SITE_PAGE_CACHE_CONTROL,
	is_site_path,
	resolve_site_language,
	set_site_cache_headers,
)
from japanese_demo_website.website import localized, site_date, status_label


class TestLanguageRule(UnitTestCase):
	def test_japanese_is_default_and_choices_are_limited(self):
		self.assertEqual(resolve_site_language(None, None), "ja")
		self.assertEqual(resolve_site_language(None, "en"), "en")
		self.assertEqual(resolve_site_language("ja", "en"), "ja")
		self.assertEqual(resolve_site_language("fr", "de"), "ja")

	def test_only_app_routes_are_affected(self):
		for path in (
			"/",
			"/about",
			"/news/",
			"/news/some-article",
			"/api/method/japanese_demo_website.api.x",
		):
			self.assertTrue(is_site_path(path), path)
		for path in ("/app", "/login", "/newsletter", "/api/method/frappe.auth.get_logged_user"):
			self.assertFalse(is_site_path(path), path)


class TestSiteCacheHeaders(UnitTestCase):
	def setUp(self):
		self._headers = getattr(frappe.local, "response_headers", None)
		frappe.local.response_headers = Headers({"Cache-Control": "private,max-age=300"})

	def tearDown(self):
		frappe.local.response_headers = self._headers

	def run_hook(self, method: str, path: str) -> str:
		set_site_cache_headers(None, SimpleNamespace(method=method, path=path))
		return frappe.local.response_headers.get("Cache-Control")

	def test_site_pages_are_revalidated(self):
		for path in ("/", "/about", "/news/website-launch"):
			self.assertEqual(self.run_hook("GET", path), SITE_PAGE_CACHE_CONTROL, path)

	def test_other_responses_keep_frappe_defaults(self):
		for method, path in (
			("GET", "/login"),
			("GET", "/assets/japanese_demo_website/images/hero-960.webp"),
			("POST", "/contact"),
			("GET", "/api/method/japanese_demo_website.api.submit_inquiry"),
		):
			self.assertEqual(self.run_hook(method, path), "private,max-age=300", path)


class TestFormatters(UnitTestCase):
	def tearDown(self):
		frappe.local.lang = "en"

	def test_site_date(self):
		frappe.local.lang = "ja"
		self.assertEqual(site_date("2026-10-01"), "2026年10月1日")
		frappe.local.lang = "en"
		self.assertEqual(site_date("2026-10-01"), "October 1, 2026")
		self.assertEqual(site_date(None), "")

	def test_localized_falls_back_to_japanese(self):
		frappe.local.lang = "en"
		self.assertEqual(localized({"title": "お知らせ", "title_en": ""}, "title"), "お知らせ")
		self.assertEqual(localized({"title": "お知らせ", "title_en": "News"}, "title"), "News")

	def test_status_label(self):
		frappe.local.lang = "en"
		self.assertEqual(status_label("IN_PROGRESS"), "In Progress")
		self.assertEqual(status_label("UNKNOWN_VALUE"), "Unknown Value")
