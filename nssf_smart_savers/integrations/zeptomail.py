"""
SmartLife Flexi — ZeptoMail transactional email adapter.

Config keys (all stored in Frappe site config via bench set-config):
    smartlife_zeptomail_api_url     — defaults to https://api.zeptomail.com/v1.1/email
    smartlife_zeptomail_token       — full Authorization header value (Zoho-enczapikey ...)
    smartlife_zeptomail_from_email  — verified sender address
    smartlife_zeptomail_from_name   — sender display name
    smartlife_zeptomail_demo_mode   — 1 = simulate only, 0 = live send

Never commit credentials. All secrets come from frappe.conf.
"""
import hashlib
import json

import frappe
import requests

_DEFAULT_API_URL = "https://api.zeptomail.com/v1.1/email"
_TIMEOUT = 15


# ── Masking ───────────────────────────────────────────────────────────────────

def mask_email(email):
    """Return masked email: ro***@domain.com. Safe to log."""
    if not email or "@" not in str(email):
        return "***@***"
    local, domain = str(email).split("@", 1)
    visible = local[:2] if len(local) >= 2 else local[:1]
    return f"{visible}***@{domain}"


# ── Config ────────────────────────────────────────────────────────────────────

def _get_config():
    return {
        "api_url":    frappe.conf.get("smartlife_zeptomail_api_url", _DEFAULT_API_URL),
        "token":      frappe.conf.get("smartlife_zeptomail_token", ""),
        "from_email": frappe.conf.get("smartlife_zeptomail_from_email", ""),
        "from_name":  frappe.conf.get("smartlife_zeptomail_from_name", "NSSF SmartLife Flexi"),
        "demo_mode":  bool(frappe.conf.get("smartlife_zeptomail_demo_mode", 1)),
    }


def get_config_status():
    """Return booleans/status strings only — never expose secret values."""
    cfg = _get_config()
    return {
        "configured": bool(cfg["token"] and cfg["from_email"]),
        "api_url":    "configured" if cfg["api_url"] else "not_configured",
        "token":      "configured" if cfg["token"] else "not_configured",
        "from_email": "configured" if cfg["from_email"] else "not_configured",
        "from_name":  "configured" if cfg["from_name"] else "not_configured",
        "demo_mode":  cfg["demo_mode"],
    }


# ── Payload builder ───────────────────────────────────────────────────────────

def _build_payload(to_email, to_name, subject, htmlbody, textbody, client_reference):
    cfg = _get_config()
    payload = {
        "from": {
            "address": cfg["from_email"],
            "name":    cfg["from_name"],
        },
        "to": [
            {
                "email_address": {
                    "address": to_email,
                    "name":    to_name or "SmartLife Member",
                }
            }
        ],
        "subject": subject,
        "track_clicks": False,
        "track_opens":  False,
    }
    if htmlbody:
        payload["htmlbody"] = htmlbody
    if textbody:
        payload["textbody"] = textbody
    if client_reference:
        payload["client_reference"] = client_reference
    return payload


# ── Public send function ──────────────────────────────────────────────────────

def send_zeptomail_email(
    to_email,
    to_name,
    subject,
    htmlbody=None,
    textbody=None,
    client_reference=None,
    metadata=None,
):
    """
    Send a transactional email via ZeptoMail.

    Returns a structured result dict. Never raises — always returns ok=True/False.
    Never logs the token. Never logs the full recipient email.
    """
    masked = mask_email(to_email)
    cfg    = _get_config()

    # Demo mode — no real send
    if cfg["demo_mode"]:
        return {
            "ok":               True,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Demo Mode",
            "message":          "Email not sent because SmartLife messaging demo mode is enabled.",
            "recipient_masked": masked,
            "demo_mode":        True,
        }

    # Config gate
    if not cfg["token"]:
        return {
            "ok":               False,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Failed",
            "error":            "ZeptoMail token not configured in site config.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }
    if not cfg["from_email"]:
        return {
            "ok":               False,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Failed",
            "error":            "ZeptoMail sender email not configured in site config.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }

    payload = _build_payload(to_email, to_name, subject, htmlbody, textbody, client_reference)

    # Stable hash of payload for audit — does not reveal content
    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]

    try:
        headers = {
            "Authorization": cfg["token"],
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        }
        resp = requests.post(
            cfg["api_url"],
            headers=headers,
            json=payload,
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        data             = resp.json() if resp.content else {}
        provider_ref     = (
            data.get("data", {}).get("message_id")
            or data.get("message_id")
            or data.get("request_id")
            or f"zepto-{payload_hash}"
        )
        return {
            "ok":               True,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Sent",
            "provider_reference": str(provider_ref),
            "recipient_masked": masked,
            "demo_mode":        False,
            "payload_hash":     payload_hash,
        }
    except requests.exceptions.Timeout:
        frappe.log_error("ZeptoMail request timed out", "SmartLife ZeptoMail")
        return {
            "ok":               False,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Failed",
            "error":            "Email provider timed out. Please retry.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }
    except requests.exceptions.HTTPError as exc:
        safe_msg = f"Email provider returned HTTP {exc.response.status_code}."
        frappe.log_error(safe_msg, "SmartLife ZeptoMail")
        return {
            "ok":               False,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Failed",
            "error":            safe_msg,
            "recipient_masked": masked,
            "demo_mode":        False,
        }
    except Exception as exc:
        frappe.log_error("ZeptoMail send error", "SmartLife ZeptoMail")
        return {
            "ok":               False,
            "provider":         "zeptomail",
            "channel":          "Email",
            "status":           "Failed",
            "error":            "Email send failed. Check server logs.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }
