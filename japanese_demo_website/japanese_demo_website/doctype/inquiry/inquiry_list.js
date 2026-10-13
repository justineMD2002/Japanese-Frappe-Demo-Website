// Copyright (c) 2026, Pixelcare Consulting Corporation and contributors
// For license information, please see license.txt

const INQUIRY_STATUS_COLORS = { NEW: "red", IN_PROGRESS: "orange", CLOSED: "green" };

frappe.listview_settings["Inquiry"] = {
	get_indicator(doc) {
		const label = frappe.utils.to_title_case(doc.status.replace(/_/g, " ").toLowerCase());
		return [__(label), INQUIRY_STATUS_COLORS[doc.status] || "gray", `status,=,${doc.status}`];
	},
};
