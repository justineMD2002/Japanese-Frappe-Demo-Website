# Copyright (c) 2026, Pixelcare Consulting Corporation and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class Inquiry(Document):
	def validate(self):
		for fieldname in ("full_name", "name_kana", "company", "email", "phone"):
			value = self.get(fieldname)
			if value:
				self.set(fieldname, value.strip())
		validate_email_address(self.email, throw=True)
		if not (self.message or "").strip():
			frappe.throw(frappe._("Message is required"))
