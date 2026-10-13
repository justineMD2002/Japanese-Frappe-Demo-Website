from frappe import _

from japanese_demo_website.website import set_page_meta


def get_context(context):
	set_page_meta(
		context,
		title=_("About Us"),
		description=_(
			"Company profile, message from our president, history and office locations of Minato Link."
		),
		active_route="/about",
	)
