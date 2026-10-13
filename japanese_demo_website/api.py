"""Public endpoints for the website. Every argument here comes from an anonymous visitor."""

import frappe
from frappe import _, _lt
from frappe.rate_limiter import rate_limit
from frappe.utils import cint, validate_email_address, validate_phone_number

from japanese_demo_website.constants import (
	INQUIRY_MAX_LENGTHS,
	INQUIRY_RATE_LIMIT,
	INQUIRY_RATE_WINDOW_SECONDS,
	INQUIRY_STATUS_NEW,
	INQUIRY_TYPES,
	SUBMISSION_RECEIVED,
)
from japanese_demo_website.website import site_lang

FIELD_LABELS = {
	"full_name": _lt("Name"),
	"name_kana": _lt("Name (Kana)"),
	"company": _lt("Company"),
	"email": _lt("Email address"),
	"phone": _lt("Phone number"),
	"message": _lt("Message"),
}


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=INQUIRY_RATE_LIMIT, seconds=INQUIRY_RATE_WINDOW_SECONDS)
def submit_inquiry(
	full_name: str,
	email: str,
	inquiry_type: str,
	message: str,
	privacy_consent: str | int = 0,
	name_kana: str | None = None,
	company: str | None = None,
	phone: str | None = None,
	website: str | None = None,
) -> dict:
	# `website` is a honeypot input hidden from people; bots that fill it get a normal-looking reply
	if website:
		return {"status": SUBMISSION_RECEIVED}

	values = {
		"full_name": (full_name or "").strip(),
		"name_kana": (name_kana or "").strip(),
		"company": (company or "").strip(),
		"email": (email or "").strip(),
		"phone": (phone or "").strip(),
		"message": (message or "").strip(),
	}
	validate_inquiry(values, inquiry_type, cint(privacy_consent))

	# explicit allowlist: visitors cannot set status or any other field
	doc = frappe.get_doc(
		{
			"doctype": "Inquiry",
			**values,
			"inquiry_type": inquiry_type,
			"privacy_consent": 1,
			"status": INQUIRY_STATUS_NEW,
			"language": site_lang(),
		}
	)
	doc.insert(ignore_permissions=True)  # guests have no Inquiry permission by design
	return {"status": SUBMISSION_RECEIVED, "reference": doc.name}


def validate_inquiry(values: dict, inquiry_type: str, privacy_consent: int) -> None:
	for fieldname in ("full_name", "email", "message"):
		if not values[fieldname]:
			frappe.throw(_("Please enter {0}.").format(FIELD_LABELS[fieldname]))

	for fieldname, max_length in INQUIRY_MAX_LENGTHS.items():
		if len(values[fieldname]) > max_length:
			frappe.throw(
				_("{0} must be {1} characters or fewer.").format(FIELD_LABELS[fieldname], max_length)
			)

	if not validate_email_address(values["email"]):
		frappe.throw(_("Please enter a valid email address."))

	if values["phone"] and not validate_phone_number(values["phone"]):
		frappe.throw(_("Please enter a valid phone number."))

	if inquiry_type not in INQUIRY_TYPES:
		frappe.throw(_("Please choose an inquiry type."))

	if not privacy_consent:
		frappe.throw(_("Please agree to the privacy policy before sending."))
