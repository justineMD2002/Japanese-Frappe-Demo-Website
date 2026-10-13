"""App-owned constants. Enum values are UPPERCASE; labels are English msgids translated in locale/ja.po."""

from frappe import _lt

# Languages offered by the public site. Japanese is the default for every visitor
# who has not picked a language with the header toggle.
DEFAULT_LANGUAGE = "ja"
SITE_LANGUAGES = ("ja", "en")
LANGUAGE_COOKIE = "preferred_language"  # same cookie Frappe core reads for guests

# Public routes owned by this app. The language rule in language.py only applies to these,
# so Desk and other apps' pages on the same site keep Frappe's normal language resolution.
NAV_ITEMS = (
	{"route": "/", "label": _lt("Home")},
	{"route": "/about", "label": _lt("About Us")},
	{"route": "/services", "label": _lt("Services")},
	{"route": "/news", "label": _lt("News")},
	{"route": "/contact", "label": _lt("Contact")},
)
SITE_ROUTES = frozenset(item["route"] for item in NAV_ITEMS)
SITE_ROUTE_PREFIXES = ("/news/",)
SITE_API_PREFIX = "/api/method/japanese_demo_website."

NEWS_PAGE_SIZE = 10

# Inquiry.status (Select options in inquiry.json must match)
INQUIRY_STATUS_NEW = "NEW"
INQUIRY_STATUS_IN_PROGRESS = "IN_PROGRESS"
INQUIRY_STATUS_CLOSED = "CLOSED"

# Inquiry.inquiry_type
INQUIRY_TYPES = ("SERVICES", "ESTIMATE", "PARTNERSHIP", "OTHER")

# News Article.category
NEWS_CATEGORIES = ("ANNOUNCEMENT", "PRESS_RELEASE", "EVENT")

# API response status for the contact form
SUBMISSION_RECEIVED = "RECEIVED"

# The one place enum values become display text (see website.status_label).
STATUS_LABELS = {
	INQUIRY_STATUS_NEW: _lt("New"),
	INQUIRY_STATUS_IN_PROGRESS: _lt("In Progress"),
	INQUIRY_STATUS_CLOSED: _lt("Closed"),
	"SERVICES": _lt("About our services"),
	"ESTIMATE": _lt("Request a quote"),
	"PARTNERSHIP": _lt("Partnership"),
	"OTHER": _lt("Other"),
	"ANNOUNCEMENT": _lt("Announcement"),
	"PRESS_RELEASE": _lt("Press Release"),
	"EVENT": _lt("Event"),
}

# Contact form limits, enforced server-side in api.submit_inquiry
INQUIRY_MAX_LENGTHS = {
	"full_name": 100,
	"name_kana": 100,
	"company": 140,
	"email": 254,
	"phone": 30,
	"message": 5000,
}
INQUIRY_RATE_LIMIT = 5  # submissions per IP
INQUIRY_RATE_WINDOW_SECONDS = 60 * 60
