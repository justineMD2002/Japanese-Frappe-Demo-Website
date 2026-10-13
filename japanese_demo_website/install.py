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
from japanese_demo_website.website import site_image

NEWS_ARTICLES = [
	{
		"slug": "website-launch",
		"category": "ANNOUNCEMENT",
		"published_on": "2026-10-01",
		"image": site_image("news-website"),
		"title": "日本語ウェブサイトを公開しました",
		"title_en": "Our Japanese website is now live",
		"summary": "日本のお客様に当社のサービスをより詳しくご紹介するため、日本語のウェブサイトを公開しました。",
		"summary_en": "We have launched a Japanese website to introduce our services to customers in Japan.",
		"content": (
			"<p>このたび、日本のお客様に向けて当社ウェブサイトの日本語版を公開いたしました。</p>"
			"<p>ERPNext・Frappeの導入、SAP Business Oneとの連携、Web・アプリ開発、AIによる業務自動化について、"
			"サービス内容やご相談の流れをご紹介しています。</p>"
			"<p>ご質問やご相談は、お問い合わせフォームよりお気軽にお寄せください。</p>"
		),
		"content_en": (
			"<p>We have launched a Japanese version of our website for customers in Japan.</p>"
			"<p>It introduces our ERPNext and Frappe implementation, SAP Business One integration, "
			"web and app development and AI automation services, and how a project with us runs.</p>"
			"<p>If you have any questions, please contact us through the contact form.</p>"
		),
	},
	{
		"slug": "year-end-holidays-2026",
		"category": "ANNOUNCEMENT",
		"published_on": "2026-09-20",
		"image": site_image("news-holiday"),
		"title": "年末年始休業期間のお知らせ",
		"title_en": "Year-end holiday schedule",
		"summary": "2026年12月24日（木）から2027年1月1日（金）まで休業いたします。",
		"summary_en": "Our office will be closed from Thursday, December 24, 2026 to Friday, January 1, 2027.",
		"content": (
			"<p>誠に勝手ながら、下記の期間を年末年始休業とさせていただきます。</p>"
			"<p>休業期間：2026年12月24日（木）〜2027年1月1日（金）</p>"
			"<p>休業期間中にいただいたお問い合わせは、1月4日（月）以降に順次ご回答いたします。"
			"ご不便をおかけいたしますが、何卒ご了承くださいますようお願い申し上げます。</p>"
		),
		"content_en": (
			"<p>Our office will be closed from Thursday, December 24, 2026 to Friday, January 1, 2027.</p>"
			"<p>We will reply to inquiries received during this period in order from Monday, January 4.</p>"
		),
	},
	{
		"slug": "sample-erpnext-seminar",
		"category": "EVENT",
		"published_on": "2026-09-05",
		"image": site_image("news-seminar"),
		"title": "【サンプル】ERPNext導入の進め方 オンラインセミナー",
		"title_en": "[Sample] Online seminar: how an ERPNext project runs",
		"summary": "これはデモ用のサンプル記事です。イベント情報もDeskから登録・編集できます。",
		"summary_en": "This is a sample article for the demo. Events can also be added and edited in Desk.",
		"content": (
			"<p>これはデモ用のサンプル記事です。実際のイベントではありません。</p>"
			"<p>ニュース記事はFrappeのDesk画面から、日本語・英語の本文や画像、公開日、公開状態を編集できます。</p>"
		),
		"content_en": (
			"<p>This is a sample article for the demo, not a real event.</p>"
			"<p>News articles can be edited in Frappe Desk: Japanese and English text, image, "
			"publish date and published status.</p>"
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
		"message": "ERPNextでの在庫管理・販売管理の導入を検討しています。概算のお見積もりをお願いできますでしょうか。",
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
		"message": "SAP Business Oneと自社ECサイトの在庫連携について相談したいです。来月中にオンラインでの打ち合わせを希望します。",
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
