import frappe
from frappe.tests import IntegrationTestCase

from japanese_demo_website.api import submit_inquiry
from japanese_demo_website.constants import INQUIRY_STATUS_NEW, SUBMISSION_RECEIVED

VALID = {
	"full_name": "  山田 太郎 ",
	"email": "taro.test@example.com",
	"inquiry_type": "SERVICES",
	"message": "テストのお問い合わせです。",
	"privacy_consent": "1",
}


class TestSubmitInquiry(IntegrationTestCase):
	def setUp(self):
		frappe.set_user("Guest")

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_guest_submission_is_saved_with_server_controlled_fields(self):
		result = submit_inquiry(**VALID)

		self.assertEqual(result["status"], SUBMISSION_RECEIVED)
		doc = frappe.get_doc("Inquiry", result["reference"])
		self.assertEqual(doc.full_name, "山田 太郎")
		self.assertEqual(doc.status, INQUIRY_STATUS_NEW)
		self.assertEqual(doc.privacy_consent, 1)

	def test_rejects_invalid_input(self):
		for override in (
			{"email": "not-an-email"},
			{"full_name": "   "},
			{"message": "x" * 5001},
			{"inquiry_type": "HACK"},
			{"privacy_consent": "0"},
			{"phone": "call me maybe"},
		):
			with self.subTest(override=override), self.assertRaises(frappe.ValidationError):
				submit_inquiry(**{**VALID, **override})

	def test_honeypot_does_not_save(self):
		before = frappe.db.count("Inquiry")
		result = submit_inquiry(**VALID, website="https://spam.example")

		self.assertEqual(result, {"status": SUBMISSION_RECEIVED})
		self.assertEqual(frappe.db.count("Inquiry"), before)
