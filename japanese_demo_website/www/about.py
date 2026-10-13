from frappe import _

from japanese_demo_website.website import set_page_meta


def get_context(context):
	set_page_meta(
		context,
		title=_("About Us"),
		description=_("Company profile and office of Pixelcare Consulting Corporation."),
		active_route="/about",
	)
