from frappe import _

from japanese_demo_website.constants import INQUIRY_MAX_LENGTHS, INQUIRY_TYPES
from japanese_demo_website.website import set_page_meta

no_cache = 1  # the form posts with this session's CSRF token


def get_context(context):
	set_page_meta(
		context,
		title=_("Contact"),
		description=_("Contact Pixelcare Consulting about our services, quotes or partnerships."),
		active_route="/contact",
	)
	context.inquiry_types = INQUIRY_TYPES
	context.max_lengths = INQUIRY_MAX_LENGTHS
