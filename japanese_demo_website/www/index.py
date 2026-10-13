from frappe import _

from japanese_demo_website.website import get_published_news, set_page_meta

HOME_NEWS_LIMIT = 3


def get_context(context):
	set_page_meta(
		context,
		# home title leads with what the company does; the base template appends the company name
		title=_("Business process consulting, system implementation, operations support"),
		description=_(
			"Minato Link supports small and mid-sized companies in Japan with business process "
			"consulting, system implementation and ongoing operations support."
		),
		active_route="/",
	)
	context.latest_news = get_published_news(HOME_NEWS_LIMIT)
