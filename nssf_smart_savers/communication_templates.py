"""
SmartLife Flexi — Communication templates.

Rules:
- Never include raw NIN, DOB, exact age, sensitive staff notes or full phone/email.
- first_name may appear only in consented outbound communications.
- Projection language is indicative only — not a guarantee.
- Birthday messages must not state the exact DOB.
- Do not hard-sell. Tone: professional, reassuring, NSSF-appropriate.
"""

# ── Template registry ─────────────────────────────────────────────────────────
#
# Each template dict contains:
#   channel_sms   — bool: available for SMS
#   channel_email — bool: available for email
#   consent_required — bool: must have consent_to_contact = True before sending
#   trigger_stage — informational: which lead lifecycle stage triggers this
#   required_fields — list: lead fields that must be non-null before sending
#   safe_vars     — placeholders allowed in body; no PII beyond first_name for consented sends
#   sms_body      — SMS text (≤160 chars recommended)
#   email_subject — email subject line
#   email_text    — plain-text email body
#   email_html    — HTML email body

TEMPLATES = {

    "welcome_after_personal_details": {
        "channel_sms":    True,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Personal Details Captured",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "goal_label", "saver_type_label"],
        "sms_body": (
            "Hello {first_name}, welcome to NSSF SmartLife Flexi! "
            "Your journey to a secure financial future starts here. "
            "Log in at https://nssf-smartlifeflexi.nile-gov-demo.com to continue."
        ),
        "email_subject": "Welcome to NSSF SmartLife Flexi",
        "email_text": (
            "Dear {first_name},\n\n"
            "Thank you for taking the first step towards a secure financial future with NSSF SmartLife Flexi.\n\n"
            "Your details have been captured. To continue, please log in and complete your savings plan.\n\n"
            "Warm regards,\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>Thank you for taking the first step towards a secure financial future with "
            "<strong>NSSF SmartLife Flexi</strong>.</p>"
            "<p>Your details have been captured. Please log in to continue and complete your personalised savings plan.</p>"
            "<p>Warm regards,<br><strong>NSSF SmartLife Flexi Team</strong></p>"
        ),
    },

    "projection_viewed_reminder": {
        "channel_sms":    True,
        "channel_email":  False,
        "consent_required": True,
        "trigger_stage":  "Projection Viewed (no checkout after 24h)",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "goal_label"],
        "sms_body": (
            "Hi {first_name}, you recently viewed your SmartLife Flexi savings projection. "
            "Ready to take the next step? Visit https://nssf-smartlifeflexi.nile-gov-demo.com"
        ),
        "email_subject": "Your SmartLife Flexi savings plan is waiting",
        "email_text": "",
        "email_html": "",
    },

    "checkout_abandoned_reminder": {
        "channel_sms":    True,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Checkout Started (no payment after 2h)",
        "required_fields": ["first_name", "goal_label"],
        "safe_vars":      ["first_name", "goal_label", "contribution_amount", "frequency"],
        "sms_body": (
            "Hi {first_name}, your SmartLife Flexi plan is almost ready. "
            "Complete your first contribution to secure your {goal_label} goal. "
            "Visit https://nssf-smartlifeflexi.nile-gov-demo.com"
        ),
        "email_subject": "Complete your SmartLife Flexi plan — {goal_label}",
        "email_text": (
            "Dear {first_name},\n\n"
            "You were so close! Your SmartLife Flexi savings plan for {goal_label} is ready.\n\n"
            "Completing your first contribution will activate your plan and start your savings journey.\n\n"
            "Log in now: https://nssf-smartlifeflexi.nile-gov-demo.com\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>You were so close! Your <strong>SmartLife Flexi</strong> savings plan for "
            "<strong>{goal_label}</strong> is ready and waiting.</p>"
            "<p>Completing your first contribution will activate your plan and start your savings journey.</p>"
            "<p><a href='https://nssf-smartlifeflexi.nile-gov-demo.com'>Complete your plan now</a></p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

    "initial_deposit_reminder": {
        "channel_sms":    False,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Payment Pending (after 48h)",
        "required_fields": ["first_name", "contribution_amount"],
        "safe_vars":      ["first_name", "contribution_amount", "frequency"],
        "sms_body": "",
        "email_subject": "Your NSSF SmartLife Flexi contribution is pending",
        "email_text": (
            "Dear {first_name},\n\n"
            "Your initial contribution of {contribution_amount} is still pending.\n\n"
            "Please complete your payment to activate your SmartLife Flexi savings plan.\n\n"
            "Log in: https://nssf-smartlifeflexi.nile-gov-demo.com\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>Your initial contribution of <strong>{contribution_amount}</strong> is still pending.</p>"
            "<p>Please complete your payment to activate your SmartLife Flexi savings plan.</p>"
            "<p><a href='https://nssf-smartlifeflexi.nile-gov-demo.com'>Complete payment now</a></p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

    "birthday_message": {
        "channel_sms":    True,
        "channel_email":  False,
        "consent_required": True,
        "trigger_stage":  "Birthday month — birthday_day matches today",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name"],
        # Note: exact DOB must never be stated in the message.
        "sms_body": (
            "Happy Birthday, {first_name}! NSSF SmartLife Flexi wishes you a wonderful day. "
            "Keep saving towards your future. Every contribution counts."
        ),
        "email_subject": "Happy Birthday from NSSF SmartLife Flexi!",
        "email_text": "",
        "email_html": "",
    },

    "staff_follow_up_message": {
        "channel_sms":    True,
        "channel_email":  False,
        "consent_required": True,
        "trigger_stage":  "Staff Follow-up Required",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "next_follow_up_on"],
        "sms_body": (
            "Hi {first_name}, an NSSF SmartLife Flexi adviser will be in touch with you soon "
            "to help you with your savings plan. Thank you for your patience."
        ),
        "email_subject": "An NSSF SmartLife Flexi adviser will contact you",
        "email_text": "",
        "email_html": "",
    },

    "savings_milestone_message": {
        "channel_sms":    True,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Payment Completed",
        "required_fields": ["first_name", "goal_label"],
        "safe_vars":      ["first_name", "goal_label"],
        "sms_body": (
            "Congratulations, {first_name}! Your SmartLife Flexi contribution is confirmed. "
            "You are one step closer to your {goal_label} goal. Keep it up!"
        ),
        "email_subject": "Contribution confirmed — NSSF SmartLife Flexi",
        "email_text": (
            "Dear {first_name},\n\n"
            "Your SmartLife Flexi contribution has been confirmed.\n\n"
            "You are making excellent progress towards your {goal_label} goal. "
            "Keep saving — every contribution brings you closer.\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>Your SmartLife Flexi contribution has been <strong>confirmed</strong>.</p>"
            "<p>You are making excellent progress towards your <strong>{goal_label}</strong> goal. "
            "Keep saving — every contribution brings you closer.</p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

    "dormant_lead_reactivation": {
        "channel_sms":    True,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Dormant (after 30 days of inactivity)",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "goal_label"],
        "sms_body": (
            "Hi {first_name}, we miss you at NSSF SmartLife Flexi! "
            "Your savings plan is still available. Pick up where you left off: "
            "https://nssf-smartlifeflexi.nile-gov-demo.com"
        ),
        "email_subject": "Your SmartLife Flexi savings plan is waiting for you",
        "email_text": (
            "Dear {first_name},\n\n"
            "We noticed you have not visited your SmartLife Flexi savings plan recently.\n\n"
            "Your personalised plan is still available and ready for you. "
            "It is not too late to get back on track towards your goal.\n\n"
            "Log in now: https://nssf-smartlifeflexi.nile-gov-demo.com\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>We noticed you have not visited your SmartLife Flexi savings plan recently.</p>"
            "<p>Your personalised plan is still available and ready for you. "
            "It is not too late to get back on track towards your goal.</p>"
            "<p><a href='https://nssf-smartlifeflexi.nile-gov-demo.com'>Return to your plan</a></p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

    "diaspora_saver_follow_up": {
        "channel_sms":    False,
        "channel_email":  True,
        "consent_required": True,
        "trigger_stage":  "Any stage — segment = diaspora_ugandan",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "goal_label", "saver_type_label"],
        "sms_body": "",
        "email_subject": "Save for Uganda from anywhere — NSSF SmartLife Flexi",
        "email_text": (
            "Dear {first_name},\n\n"
            "Thank you for your interest in NSSF SmartLife Flexi.\n\n"
            "As a Ugandan in the diaspora, you can contribute to your SmartLife Flexi plan "
            "from anywhere in the world. We will be in touch with details on how to get started.\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear {first_name},</p>"
            "<p>Thank you for your interest in <strong>NSSF SmartLife Flexi</strong>.</p>"
            "<p>As a Ugandan in the diaspora, you can contribute to your SmartLife Flexi plan "
            "from anywhere in the world. We will be in touch with details on how to get started.</p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

    "informal_sector_saver_follow_up": {
        "channel_sms":    True,
        "channel_email":  False,
        "consent_required": True,
        "trigger_stage":  "Any stage — segment = informal_sector",
        "required_fields": ["first_name"],
        "safe_vars":      ["first_name", "saver_type_label"],
        "sms_body": (
            "Hi {first_name}, NSSF SmartLife Flexi is built for people like you. "
            "Save as little or as much as you can — your future is worth protecting. "
            "Visit https://nssf-smartlifeflexi.nile-gov-demo.com"
        ),
        "email_subject": "SmartLife Flexi — built for the informal sector",
        "email_text": "",
        "email_html": "",
    },

    "consent_missing_education": {
        "channel_sms":    False,
        "channel_email":  True,
        # This is educational content only — no commercial ask.
        # consent_required = False means this CAN be sent without consent_to_contact,
        # but must never include a commercial push or claim to be selling anything.
        "consent_required": False,
        "trigger_stage":  "consent_to_contact = False — educational send only",
        "required_fields": ["email_address"],
        "safe_vars":      [],
        "sms_body": "",
        "email_subject": "Understanding your NSSF SmartLife Flexi rights",
        "email_text": (
            "Dear SmartLife Flexi Visitor,\n\n"
            "We want to make sure you have the information you need about NSSF SmartLife Flexi.\n\n"
            "You can update your contact preferences at any time by visiting our site.\n\n"
            "This message contains information only — it is not a commercial offer.\n\n"
            "NSSF SmartLife Flexi Team"
        ),
        "email_html": (
            "<p>Dear SmartLife Flexi Visitor,</p>"
            "<p>We want to make sure you have the information you need about NSSF SmartLife Flexi.</p>"
            "<p>You can update your contact preferences at any time by visiting our site.</p>"
            "<p><em>This message contains information only — it is not a commercial offer.</em></p>"
            "<p>NSSF SmartLife Flexi Team</p>"
        ),
    },

}

TEMPLATE_NAMES = list(TEMPLATES.keys())


# ── Public helpers ────────────────────────────────────────────────────────────

def get_template(name):
    """Return template dict or None."""
    return TEMPLATES.get(name)


def list_templates(channel=None):
    """Return template metadata list — no message bodies, no PII."""
    out = []
    for name, t in TEMPLATES.items():
        if channel == "SMS" and not t["channel_sms"]:
            continue
        if channel == "Email" and not t["channel_email"]:
            continue
        out.append({
            "template_name":    name,
            "channel_sms":      t["channel_sms"],
            "channel_email":    t["channel_email"],
            "consent_required": t["consent_required"],
            "trigger_stage":    t["trigger_stage"],
        })
    return out


def render_template(name, context):
    """
    Render a template body with context variables.
    context must contain only safe variables (first_name, goal_label, etc.).
    Never put raw PII other than first_name (for consented sends) in context.
    Returns dict with rendered sms_body, email_subject, email_text, email_html.
    """
    tmpl = TEMPLATES.get(name)
    if not tmpl:
        raise ValueError(f"Unknown template: {name}")
    safe_ctx = {k: str(v or "") for k, v in (context or {}).items()}

    def _render(text):
        try:
            return text.format(**safe_ctx) if text else ""
        except KeyError:
            return text  # return unrendered if vars missing

    return {
        "sms_body":      _render(tmpl["sms_body"]),
        "email_subject": _render(tmpl["email_subject"]),
        "email_text":    _render(tmpl["email_text"]),
        "email_html":    _render(tmpl["email_html"]),
    }
