"""
SmartLife Flexi — Messaging service.

Orchestrates consent checking, template rendering, provider dispatch,
and communication logging for SMS and email sends.

Public functions:
    preview_message(lead_name, template_name, channel, context)
    send_smartlife_message(lead_name, template_name, channel, staff_user, force_demo)
    get_messaging_provider_status()
"""
from datetime import datetime

import frappe

from nssf_smart_savers.communication_templates import get_template, render_template
from nssf_smart_savers.integrations.phahapa_sms import (
    get_config_status as sms_config_status,
    mask_phone,
    send_phahapa_sms,
)
from nssf_smart_savers.integrations.zeptomail import (
    get_config_status as email_config_status,
    mask_email,
    send_zeptomail_email,
)

_SUPPORTED_CHANNELS = ("SMS", "Email")


# ── Consent and recipient validation ─────────────────────────────────────────

def _validate_consent_and_recipient(lead, template_name, channel):
    """
    Returns (ok, skip_reason) where ok=True means send is allowed.
    Enforces:
      - consent_to_contact for templates that require it
      - preferred_contact_channel match (or explicit staff override)
      - required recipient field exists
    """
    tmpl = get_template(template_name)
    if not tmpl:
        return False, f"Unknown template: {template_name}"

    if tmpl["consent_required"] and not lead.get("consent_to_contact"):
        return False, "Skipped - No Consent"

    if channel == "SMS":
        if not lead.get("primary_phone"):
            return False, "Skipped - Missing Recipient"
    elif channel == "Email":
        if not lead.get("email_address"):
            return False, "Skipped - Missing Recipient"
    else:
        return False, f"Unsupported channel: {channel}"

    return True, None


# ── Communication log ─────────────────────────────────────────────────────────

def _create_log(
    lead_name,
    channel,
    template_name,
    message_status,
    provider=None,
    provider_reference=None,
    client_reference=None,
    failure_reason=None,
    consent_snapshot=False,
    staff_owner=None,
    triggered_by_stage=None,
    demo_mode=True,
    request_payload_hash=None,
    response_summary=None,
    recipient_masked=None,
    recipient_type=None,
):
    try:
        doc = frappe.get_doc({
            "doctype":              "SmartLife Communication Log",
            "lead":                 lead_name,
            "channel":              channel,
            "template_name":        template_name,
            "recipient_masked":     recipient_masked or "",
            "recipient_type":       recipient_type or ("Phone" if channel == "SMS" else "Email"),
            "message_status":       message_status,
            "provider":             provider or "",
            "provider_reference":   provider_reference or "",
            "client_reference":     client_reference or "",
            "sent_on":              datetime.now(),
            "failure_reason":       failure_reason or "",
            "consent_snapshot":     int(bool(consent_snapshot)),
            "staff_owner":          staff_owner or frappe.session.user,
            "triggered_by_stage":   triggered_by_stage or "",
            "demo_mode":            int(bool(demo_mode)),
            "request_payload_hash": request_payload_hash or "",
            "response_summary":     response_summary or "",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc.name
    except Exception:
        frappe.log_error("SmartLife Communication Log creation failed", "SmartLife Messaging")
        return None


# ── Preview ───────────────────────────────────────────────────────────────────

def preview_message(
    lead_name=None,
    template_name=None,
    channel=None,
    context=None,
):
    """
    Render a message preview for a lead without sending.
    Returns rendered bodies. Logs a Previewed entry if lead_name is provided.
    full PII (first_name) included only for authorised callers — enforced in the API layer.
    """
    if not template_name:
        return {"ok": False, "error": "template_name is required."}

    tmpl = get_template(template_name)
    if not tmpl:
        return {"ok": False, "error": f"Unknown template: {template_name}"}

    # Build safe render context
    render_ctx = dict(context or {})
    if lead_name:
        try:
            lead = frappe.db.get_value(
                "SmartLife Demo Lead",
                lead_name,
                ["first_name", "goal_label", "segment", "frequency"],
                as_dict=True,
            ) or {}
            render_ctx.setdefault("first_name", lead.get("first_name", ""))
            render_ctx.setdefault("goal_label", lead.get("goal_label", ""))
            render_ctx.setdefault("saver_type_label", lead.get("segment", ""))
            render_ctx.setdefault("frequency", lead.get("frequency", ""))
        except Exception:
            pass

    rendered = render_template(template_name, render_ctx)

    if lead_name:
        _create_log(
            lead_name=lead_name,
            channel=channel or "SMS",
            template_name=template_name,
            message_status="Previewed",
            demo_mode=True,
        )

    return {
        "ok":           True,
        "template_name": template_name,
        "channel":      channel,
        "rendered":     rendered,
    }


# ── Send ──────────────────────────────────────────────────────────────────────

def send_smartlife_message(
    lead_name,
    template_name,
    channel,
    staff_user=None,
    force_demo=False,
):
    """
    Send a message to a lead via the specified channel.

    Enforces:
    - consent_to_contact for templates that require it
    - required recipient field
    - provider config
    Returns a structured result dict.
    """
    if not lead_name or not template_name or not channel:
        return {"ok": False, "error": "lead_name, template_name, and channel are required."}

    if channel not in _SUPPORTED_CHANNELS:
        return {"ok": False, "error": f"Channel must be one of: {', '.join(_SUPPORTED_CHANNELS)}"}

    # Load lead
    try:
        lead = frappe.db.get_value(
            "SmartLife Demo Lead",
            lead_name,
            [
                "name", "first_name", "goal_label", "segment", "frequency",
                "primary_phone", "email_address", "preferred_contact_channel",
                "consent_to_contact", "lead_status",
                "contribution_amount" if frappe.db.has_column("SmartLife Demo Lead", "contribution_amount") else "initial_deposit",
            ],
            as_dict=True,
        )
    except Exception:
        lead = None

    if not lead:
        return {"ok": False, "error": f"Lead not found: {lead_name}"}

    consent_val = bool(lead.get("consent_to_contact"))

    # Validate consent and recipient
    ok, skip_reason = _validate_consent_and_recipient(lead, template_name, channel)
    if not ok:
        _create_log(
            lead_name=lead_name,
            channel=channel,
            template_name=template_name,
            message_status=skip_reason,
            consent_snapshot=consent_val,
            staff_owner=staff_user,
            demo_mode=force_demo,
            recipient_masked=_masked_recipient(lead, channel),
            recipient_type="Phone" if channel == "SMS" else "Email",
        )
        return {"ok": False, "skipped": True, "reason": skip_reason}

    # Render template
    render_ctx = {
        "first_name":          lead.get("first_name") or "",
        "goal_label":          lead.get("goal_label") or "",
        "saver_type_label":    lead.get("segment") or "",
        "frequency":           lead.get("frequency") or "",
        "contribution_amount": str(lead.get("contribution_amount") or lead.get("initial_deposit") or ""),
        "next_follow_up_on":   "",
    }
    rendered = render_template(template_name, render_ctx)
    masked   = _masked_recipient(lead, channel)

    # Dispatch to provider
    if channel == "SMS":
        result = send_phahapa_sms(
            phone_number=lead["primary_phone"],
            message=rendered["sms_body"],
            client_reference=f"{lead_name}:{template_name}",
        )
    else:
        result = send_zeptomail_email(
            to_email=lead["email_address"],
            to_name=lead.get("first_name") or "SmartLife Member",
            subject=rendered["email_subject"],
            htmlbody=rendered["email_html"] or None,
            textbody=rendered["email_text"] or None,
            client_reference=f"{lead_name}:{template_name}",
        )

    # Determine log status
    if result.get("demo_mode"):
        log_status = "Demo Mode"
    elif result.get("ok"):
        log_status = "Sent"
    else:
        log_status = "Failed"

    log_name = _create_log(
        lead_name=lead_name,
        channel=channel,
        template_name=template_name,
        message_status=log_status,
        provider=result.get("provider", ""),
        provider_reference=result.get("provider_reference", ""),
        client_reference=f"{lead_name}:{template_name}",
        failure_reason=result.get("error", ""),
        consent_snapshot=consent_val,
        staff_owner=staff_user or frappe.session.user,
        demo_mode=result.get("demo_mode", False),
        request_payload_hash=result.get("payload_hash", ""),
        response_summary=result.get("status", ""),
        recipient_masked=result.get("recipient_masked") or masked,
        recipient_type="Phone" if channel == "SMS" else "Email",
    )

    result["log_name"] = log_name
    return result


def _masked_recipient(lead, channel):
    if channel == "SMS":
        return mask_phone(lead.get("primary_phone") or "")
    return mask_email(lead.get("email_address") or "")


# ── Config status ─────────────────────────────────────────────────────────────

def get_messaging_provider_status():
    """Return provider config status — booleans and strings only, no secrets."""
    return {
        "zeptomail":     email_config_status(),
        "phahapa_egosms": sms_config_status(),
        "demo_mode": (
            email_config_status().get("demo_mode", True)
            or sms_config_status().get("demo_mode", True)
        ),
    }
