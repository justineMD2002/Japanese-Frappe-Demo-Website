# Copyright (c) 2026, Pixelcare Consulting Corporation and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.website.utils import clear_cache

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class NewsArticle(Document):
	def validate(self):
		self.slug = (self.slug or "").strip().lower()
		if not SLUG_PATTERN.match(self.slug):
			frappe.throw(_("URL Slug may only contain lowercase letters, numbers and single hyphens"))

	def on_update(self):
		# home and /news list articles, so the cached pages must be rebuilt
		clear_cache()

	def on_trash(self):
		clear_cache()
