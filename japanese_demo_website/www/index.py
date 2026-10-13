from frappe import _

from japanese_demo_website.website import get_published_news, set_page_meta

HOME_NEWS_LIMIT = 3


def get_context(context):
	set_page_meta(
		context,
		# home title leads with what the company does; the base template appends the company name
		title=_("ERPNext, SAP Business One and custom system development"),
		description=_(
			"Pixelcare Consulting implements ERPNext and Frappe, integrates SAP Business One, builds "
			"custom web applications and automates routine work with AI."
		),
		active_route="/",
	)
	context.latest_news = get_published_news(HOME_NEWS_LIMIT)
