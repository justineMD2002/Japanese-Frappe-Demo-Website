import frappe
from frappe.tests import UnitTestCase

from japanese_demo_website.language import is_site_path, resolve_site_language
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
