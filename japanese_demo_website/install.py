"""Demo seed content (wired as after_install). Idempotent, so it is safe to run again with
`bench --site <site> execute japanese_demo_website.install.seed_demo_content`.

Seeding is not tied to after_migrate on purpose: an article the client deletes in Desk stays deleted.
"""

import frappe

from japanese_demo_website.constants import (
	INQUIRY_STATUS_CLOSED,
	INQUIRY_STATUS_IN_PROGRESS,
	INQUIRY_STATUS_NEW,
)

NEWS_ARTICLES = [
	{
		"slug": "new-osaka-office",
		"category": "ANNOUNCEMENT",
		"published_on": "2026-10-01",
		"title": "大阪営業所を開設しました",
		"title_en": "We have opened our Osaka office",
		"summary": "関西エリアのお客様へのサポート体制を強化するため、2026年10月1日に大阪営業所を開設しました。",
		"summary_en": "To support our customers in the Kansai region more closely, we opened our Osaka office on October 1, 2026.",
		"content": (
			"<p>平素より格別のご高配を賜り、厚く御礼申し上げます。</p>"
			"<p>このたび、関西エリアのお客様へのサポート体制を強化するため、大阪営業所を開設いたしました。"
			"訪問でのご相談や導入後のサポートを、これまで以上に迅速にご提供してまいります。</p>"
			"<p>所在地：大阪府大阪市北区梅田1-2-3 梅田ビジネスタワー8階<br>業務開始日：2026年10月1日</p>"
			"<p>今後とも変わらぬお引き立てを賜りますよう、よろしくお願い申し上げます。</p>"
		),
		"content_en": (
			"<p>Thank you for your continued support.</p>"
			"<p>We have opened an office in Osaka so that we can support customers in the Kansai region "
			"more closely, with faster on-site consultations and after-launch support.</p>"
			"<p>Address: 8F Umeda Business Tower, 1-2-3 Umeda, Kita-ku, Osaka<br>Open from: October 1, 2026</p>"
		),
	},
	{
		"slug": "year-end-holidays-2026",
		"category": "ANNOUNCEMENT",
		"published_on": "2026-09-20",
		"title": "年末年始休業期間のお知らせ",
		"title_en": "Year-end and New Year holiday schedule",
		"summary": "2026年12月27日（日）から2027年1月4日（月）まで休業いたします。",
		"summary_en": "Our offices will be closed from Sunday, December 27, 2026 to Monday, January 4, 2027.",
		"content": (
			"<p>誠に勝手ながら、下記の期間を年末年始休業とさせていただきます。</p>"
			"<p>休業期間：2026年12月27日（日）〜2027年1月4日（月）</p>"
			"<p>休業期間中にいただいたお問い合わせは、1月5日（火）以降に順次ご回答いたします。"
			"ご不便をおかけいたしますが、何卒ご了承くださいますようお願い申し上げます。</p>"
		),
		"content_en": (
			"<p>Our offices will be closed from Sunday, December 27, 2026 to Monday, January 4, 2027.</p>"
			"<p>We will reply to inquiries received during this period in order from Tuesday, January 5.</p>"
		),
	},
	{
		"slug": "dx-seminar-november",
		"category": "EVENT",
		"published_on": "2026-09-05",
		"title": "11月開催「中小企業のための業務デジタル化セミナー」のご案内",
		"title_en": "November seminar: digitizing everyday operations for small businesses",
		"summary": "受発注や在庫管理の紙・Excel運用を見直すための無料セミナーを、11月12日に東京とオンラインで開催します。",
		"summary_en": "A free seminar on moving order and inventory work off paper and spreadsheets, held on November 12 in Tokyo and online.",
		"content": (
			"<p>受発注・在庫・請求などの業務を、紙やExcelから無理なくシステムへ移行する進め方を、"
			"導入事例を交えてご紹介します。</p>"
			"<p>日時：2026年11月12日（木）14:00〜15:30<br>会場：本社セミナールーム（オンライン同時配信）<br>参加費：無料</p>"
			"<p>お申し込みはお問い合わせフォームより「その他」を選択のうえ、セミナー参加希望とご記入ください。</p>"
		),
		"content_en": (
			"<p>We will show, with real examples, how to move order, inventory and billing work from paper "
			"and spreadsheets to a system without disrupting daily operations.</p>"
			"<p>Date: Thursday, November 12, 2026, 14:00 to 15:30<br>Venue: Head office seminar room "
			"(also streamed online)<br>Fee: Free</p>"
			'<p>To register, use the contact form, choose "Other" and mention the seminar.</p>'
		),
	},
	{
		"slug": "iso27001-certification",
		"category": "PRESS_RELEASE",
		"published_on": "2026-07-15",
		"title": "情報セキュリティマネジメントシステム（ISO/IEC 27001）の認証を取得しました",
		"title_en": "We have obtained ISO/IEC 27001 certification",
		"summary": "お客様の情報を安全に取り扱う体制が第三者機関により認められ、ISO/IEC 27001の認証を取得しました。",
		"summary_en": "An independent body has certified that our information security management meets ISO/IEC 27001.",
		"content": (
			"<p>当社は、情報セキュリティマネジメントシステムの国際規格であるISO/IEC 27001の認証を取得いたしました。</p>"
			"<p>今後も、お客様からお預かりする情報の適切な管理と継続的な改善に努めてまいります。</p>"
		),
		"content_en": (
			"<p>We have been certified to ISO/IEC 27001, the international standard for information "
			"security management systems.</p>"
			"<p>We will keep improving how we protect the information our customers entrust to us.</p>"
		),
	},
	{
		"slug": "website-renewal",
		"category": "ANNOUNCEMENT",
		"published_on": "2026-06-01",
		"title": "ウェブサイトをリニューアルしました",
		"title_en": "Our website has been redesigned",
		"summary": "より見やすく、必要な情報にすぐたどり着けるよう、ウェブサイトを全面的にリニューアルしました。",
		"summary_en": "We have redesigned our website so that the information you need is easier to find.",
		"content": (
			"<p>このたび、当社ウェブサイトを全面的にリニューアルいたしました。"
			"スマートフォンからも見やすいデザインとし、お問い合わせフォームも入力しやすく改善しました。</p>"
		),
		"content_en": (
			"<p>We have redesigned our website. It is now easier to read on smartphones, "
			"and the contact form is simpler to fill in.</p>"
		),
	},
]

SAMPLE_INQUIRIES = [
	{
		"full_name": "山田 太郎",
		"name_kana": "ヤマダ タロウ",
		"company": "山田精工株式会社",
		"email": "taro.yamada@example.com",
		"phone": "03-2345-6789",
		"inquiry_type": "ESTIMATE",
		"status": INQUIRY_STATUS_NEW,
		"language": "ja",
		"message": "在庫管理のシステム化を検討しています。概算のお見積もりをお願いできますでしょうか。",
	},
	{
		"full_name": "佐藤 花子",
		"name_kana": "サトウ ハナコ",
		"company": "株式会社さくら物流",
		"email": "hanako.sato@example.com",
		"phone": "06-2345-6789",
		"inquiry_type": "SERVICES",
		"status": INQUIRY_STATUS_IN_PROGRESS,
		"language": "ja",
		"message": "大阪営業所での訪問相談は可能でしょうか。来月中の打ち合わせを希望します。",
	},
	{
		"full_name": "John Miller",
		"company": "Northwind Trading",
		"email": "john.miller@example.com",
		"inquiry_type": "PARTNERSHIP",
		"status": INQUIRY_STATUS_CLOSED,
		"language": "en",
		"message": "We are looking for an implementation partner in Japan. Could we schedule a call?",
	},
]


def after_install():
	seed_demo_content()


def seed_demo_content():
	for article in NEWS_ARTICLES:
		if frappe.db.exists("News Article", article["slug"]):
			continue
		frappe.get_doc({"doctype": "News Article", "published": 1, **article}).insert(ignore_permissions=True)

	for inquiry in SAMPLE_INQUIRIES:
		if frappe.db.exists("Inquiry", {"email": inquiry["email"]}):
			continue
		frappe.get_doc({"doctype": "Inquiry", "privacy_consent": 1, **inquiry}).insert(
			ignore_permissions=True
		)

	frappe.db.commit()
