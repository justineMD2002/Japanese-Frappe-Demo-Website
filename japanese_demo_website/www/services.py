from frappe import _

from japanese_demo_website.website import set_page_meta


def get_context(context):
	set_page_meta(
		context,
		title=_("Services"),
		description=_(
			"Business process consulting, system implementation and operations support, "
			"and how a project with us runs from first meeting to launch."
		),
		active_route="/services",
	)
