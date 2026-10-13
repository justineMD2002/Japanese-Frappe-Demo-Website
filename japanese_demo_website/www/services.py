from frappe import _

from japanese_demo_website.website import set_page_meta


def get_context(context):
	set_page_meta(
		context,
		title=_("Services"),
		description=_(
			"ERPNext and Frappe implementation, SAP Business One integration, custom web development "
			"and AI automation, and how a project with us runs."
		),
		active_route="/services",
	)
