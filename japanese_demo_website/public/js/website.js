// Public site behaviour. Loaded on every website page through web_include_js,
// so everything is a no-op outside pages rendered by templates/site_base.html.
(() => {
	if (!document.documentElement.classList.contains("jdw")) return;

	const LANGUAGE_COOKIE = "preferred_language";
	const COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 365;
	const REQUEST_TIMEOUT_MS = 15000;

	function initNavToggle() {
		const toggle = document.querySelector(".nav-toggle");
		const nav = document.getElementById("site-nav");
		if (!toggle || !nav) return;

		const setOpen = (open) => {
			toggle.setAttribute("aria-expanded", String(open));
			nav.classList.toggle("is-open", open);
		};
		toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
		document.addEventListener("keydown", (event) => {
			if (event.key === "Escape" && nav.classList.contains("is-open")) {
				setOpen(false);
				toggle.focus();
			}
		});
	}

	// The links work without JS (?_lang=xx for one page); with JS the choice is remembered site-wide.
	function initLanguageSwitch() {
		document.querySelectorAll(".lang-switch__option[data-lang]").forEach((link) => {
			link.addEventListener("click", (event) => {
				event.preventDefault();
				const secure = location.protocol === "https:" ? "; Secure" : "";
				document.cookie = `${LANGUAGE_COOKIE}=${link.dataset.lang}; path=/; max-age=${COOKIE_MAX_AGE_SECONDS}; SameSite=Lax${secure}`;
				location.reload();
			});
		});
	}

	function initInquiryForm() {
		const form = document.getElementById("inquiry-form");
		if (!form) return;

		const alertBox = document.getElementById("inquiry-error");
		const success = document.getElementById("inquiry-success");
		const submitButton = form.querySelector('button[type="submit"]');
		const submitLabel = submitButton.textContent;
		const msg = form.dataset;

		form.addEventListener("submit", async (event) => {
			event.preventDefault();
			hideAlert();
			if (!validate()) {
				showAlert(msg.msgInvalid);
				return;
			}

			setSubmitting(true);
			try {
				const result = await postInquiry();
				form.hidden = true;
				document.getElementById("inquiry-reference").textContent = result.reference || "";
				success.hidden = false;
				success.focus();
			} catch (error) {
				showAlert(error.message || msg.msgGeneric);
			} finally {
				setSubmitting(false);
			}
		});

		// clear a field's error as soon as the visitor corrects it
		form.addEventListener("input", (event) => {
			if (event.target.getAttribute("aria-invalid") === "true" && fieldError(event.target) === null) {
				setFieldError(event.target, null);
			}
		});

		function validate() {
			let firstInvalid = null;
			form.querySelectorAll("[aria-describedby][required]").forEach((input) => {
				const error = fieldError(input);
				setFieldError(input, error);
				if (error && !firstInvalid) firstInvalid = input;
			});
			if (firstInvalid) firstInvalid.focus();
			return firstInvalid === null;
		}

		function fieldError(input) {
			if (input.type === "checkbox") return input.checked ? null : msg.msgConsent;
			const value = input.value.trim();
			if (!value) return msg.msgRequired;
			if (input.type === "email" && !input.checkValidity()) return msg.msgEmail;
			return null;
		}

		function setFieldError(input, message) {
			const errorEl = document.getElementById(`${input.id}-error`);
			input.setAttribute("aria-invalid", message ? "true" : "false");
			if (!errorEl) return;
			errorEl.textContent = message || "";
			errorEl.hidden = !message;
		}

		async function postInquiry() {
			const body = new URLSearchParams(new FormData(form));
			if (!form.elements.privacy_consent.checked) body.set("privacy_consent", "0");

			const headers = { Accept: "application/json" };
			const csrfToken = window.frappe && window.frappe.csrf_token;
			if (csrfToken && csrfToken !== "None") headers["X-Frappe-CSRF-Token"] = csrfToken;

			let response;
			try {
				response = await fetch(form.dataset.endpoint, {
					method: "POST",
					headers,
					body,
					credentials: "same-origin",
					signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
				});
			} catch {
				throw new Error(msg.msgNetwork);
			}

			if (response.status === 429) throw new Error(msg.msgRateLimit);

			const data = await response.json().catch(() => ({}));
			if (!response.ok) throw new Error(serverMessage(data) || msg.msgGeneric);
			return data.message || {};
		}

		// Frappe returns frappe.throw() text in _server_messages: a JSON list of JSON objects.
		function serverMessage(data) {
			try {
				const messages = JSON.parse(data._server_messages || "[]");
				const first = messages.length ? JSON.parse(messages[0]) : null;
				return first && first.message ? stripTags(first.message) : null;
			} catch {
				return null;
			}
		}

		// DOMParser documents are inert, so markup in the message never runs
		function stripTags(html) {
			return new DOMParser().parseFromString(html, "text/html").body.textContent;
		}

		function setSubmitting(submitting) {
			submitButton.disabled = submitting;
			submitButton.textContent = submitting ? msg.msgSending : submitLabel;
			form.setAttribute("aria-busy", String(submitting));
		}

		function showAlert(message) {
			alertBox.textContent = message;
			alertBox.hidden = false;
		}

		function hideAlert() {
			alertBox.hidden = true;
			alertBox.textContent = "";
		}
	}

	initNavToggle();
	initLanguageSwitch();
	initInquiryForm();
})();
