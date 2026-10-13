"""Helpers shared by the www/ pages and templates (exposed to Jinja through the `jinja` hook)."""

import datetime

import frappe
from frappe.utils import getdate

from japanese_demo_website.constants import (
	COMPANY,
	DEFAULT_LANGUAGE,
	IMAGE_BASE,
	IMAGE_WIDTHS,
	NAV_ITEMS,
	NEWS_FALLBACK_IMAGE,
	SERVICES,
	SITE_LANGUAGES,
	STATUS_LABELS,
)


def site_lang() -> str:
	lang = frappe.local.lang
	return lang if lang in SITE_LANGUAGES else DEFAULT_LANGUAGE


def site_nav(active_route: str | None = None) -> list[dict]:
	return [
		{"route": item["route"], "label": str(item["label"]), "is_active": item["route"] == active_route}
		for item in NAV_ITEMS
	]


def company() -> dict:
	return {
		**COMPANY,
		"address": str(COMPANY["address"]),
		"address_en": COMPANY["address"].msg,  # mailing address, always in English
	}


def site_services() -> list[dict]:
	return [
		{
			"key": service["key"],
			"title": str(service["title"]),
			"summary": str(service["summary"]),
			"description": str(service["description"]),
			"points": [str(point) for point in service["points"]],
		}
		for service in SERVICES
	]


def site_image(name: str, width: int = 960) -> str:
	return site_image_path(f"{name}-{width}.webp")


def site_image_path(filename: str) -> str:
	return f"{IMAGE_BASE}/{filename}"


def site_image_srcset(name: str) -> str:
	return ", ".join(f"{site_image(name, width)} {width}w" for width in IMAGE_WIDTHS)


def lang_switch_url(lang: str) -> str:
	"""No-JS fallback for the language toggle; jdw_site.bundle.js swaps this for a cookie + reload."""
	path = frappe.local.request.path if getattr(frappe.local, "request", None) else "/"
	return f"{path}?_lang={lang}"


def localized(doc: dict, fieldname: str) -> str:
	"""Read `<field>_en` on English pages, falling back to the Japanese source field."""
	if site_lang() == "en":
		english = doc.get(f"{fieldname}_en")
		if english:
			return english
	return doc.get(fieldname) or ""


def site_date(value: str | datetime.date | None) -> str:
	if not value:
		return ""
	date = getdate(value)
	if site_lang() == "ja":
		return f"{date.year}年{date.month}月{date.day}日"
	return f"{date:%B} {date.day}, {date.year}"


def status_label(value: str | None) -> str:
	"""Display text for an UPPERCASE enum value, in the visitor's language."""
	if not value:
		return ""
	label = STATUS_LABELS.get(value)
	return str(label) if label else value.replace("_", " ").title()


def set_page_meta(context, title: str, description: str, active_route: str | None = None) -> None:
	context.title = title
	context.active_route = active_route
	context.metatags = {"description": description}


NEWS_LIST_FIELDS = ["name", "title", "title_en", "summary", "summary_en", "category", "published_on", "image"]


def get_published_news(limit: int, start: int = 0, category: str | None = None) -> list[dict]:
	"""Published articles shaped for templates. get_all is deliberate: this is public content."""
	rows = frappe.get_all(
		"News Article",
		filters=news_filters(category),
		fields=NEWS_LIST_FIELDS,
		order_by="published_on desc, creation desc",
		limit_start=start,
		limit_page_length=limit,
	)
	return [to_news_item(row) for row in rows]


def count_published_news(category: str | None = None) -> int:
	return frappe.db.count("News Article", news_filters(category))


def news_filters(category: str | None) -> dict:
	filters = {"published": 1}
	if category:
		filters["category"] = category
	return filters


def to_news_item(row: dict) -> dict:
	return frappe._dict(
		route=f"/news/{row['name']}",
		title=localized(row, "title"),
		summary=localized(row, "summary"),
		category=row["category"],
		published_on=row["published_on"],
		# Desk uploads (/files/...) are used as-is; without one the shared fallback photo is shown
		image=row.get("image") or site_image(NEWS_FALLBACK_IMAGE),
	)
