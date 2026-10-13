import frappe

from japanese_demo_website.website import localized, set_page_meta, to_news_item


def get_context(context):
	slug = frappe.form_dict.get("slug")
	article = slug and frappe.db.get_value(
		"News Article",
		{"name": slug, "published": 1},
		[
			"name",
			"title",
			"title_en",
			"summary",
			"summary_en",
			"content",
			"content_en",
			"category",
			"published_on",
		],
		as_dict=True,
	)
	if not article:
		raise frappe.DoesNotExistError

	context.article = to_news_item(article)
	# Text Editor content is sanitized by Frappe on save, so it is rendered as HTML
	context.article.content = localized(article, "content")
	set_page_meta(
		context, title=context.article.title, description=context.article.summary, active_route="/news"
	)
