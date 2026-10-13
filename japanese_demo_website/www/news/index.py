import math

import frappe
from frappe import _
from frappe.utils import cint

from japanese_demo_website.constants import NEWS_CATEGORIES, NEWS_PAGE_SIZE
from japanese_demo_website.website import count_published_news, get_published_news, set_page_meta


def get_context(context):
	set_page_meta(
		context,
		title=_("News"),
		description=_("Announcements, press releases and events from Minato Link."),
		active_route="/news",
	)

	# unknown values fall back to the full list instead of erroring
	category = frappe.form_dict.get("category")
	category = category if category in NEWS_CATEGORIES else None
	page = max(cint(frappe.form_dict.get("page")), 1)

	total = count_published_news(category)
	context.category = category
	context.categories = NEWS_CATEGORIES
	context.page = page
	context.page_count = max(math.ceil(total / NEWS_PAGE_SIZE), 1)
	context.total = total
	context.articles = get_published_news(NEWS_PAGE_SIZE, (page - 1) * NEWS_PAGE_SIZE, category)
