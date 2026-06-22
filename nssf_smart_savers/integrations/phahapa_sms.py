"""
SmartLife Flexi — Phahapa SMS / eGoSMS adapter.

Provider: eGoSMS (https://comms.egosms.co/api/v1/json/)

Config keys (all stored in Frappe site config via bench set-config):
    smartlife_phahapa_sms_api_url    — defaults to https://comms.egosms.co/api/v1/json/
    smartlife_phahapa_sms_username   — eGoSMS account username
    smartlife_phahapa_sms_password   — eGoSMS account password
    smartlife_phahapa_sms_sender_id  — alphanumeric sender ID
    smartlife_phahapa_sms_api_key    — API key if required (optional)
    smartlife_phahapa_sms_demo_mode  — 1 = simulate only, 0 = live send

eGoSMS JSON API v1 request format:
    POST https://comms.egosms.co/api/v1/json/
    Content-Type: application/json
    {
        "Username": "username",
        "Password": "password",
        "SenderId": "SENDER",
        "MessageParameters": [
            {"Number": "256700000000", "Text": "Hello"}
        ]
    }

Never commit credentials. All secrets come from frappe.conf.
"""
import re

import frappe
import requests

_DEFAULT_API_URL = "https://comms.egosms.co/api/v1/json/"
_TIMEOUT         = 15
_MAX_SMS_CHARS   = 160


# ── Phone normalisation and masking ───────────────────────────────────────────

def normalise_phone(phone):
    """
    Normalise Ugandan phone numbers to international format 256XXXXXXXXX.
    Accepts: 07XXXXXXXX, +2567XXXXXXXX, 2567XXXXXXXX.
    Returns cleaned string or raises ValueError.
    """
    if not phone:
        raise ValueError("Phone number is required.")
    raw = re.sub(r"[\s\-\(\)]", "", str(phone))
    if raw.startswith("+"):
        raw = raw[1:]
    if raw.startswith("0"):
        raw = "256" + raw[1:]
    if not re.match(r"^\d{11,13}$", raw):
        raise ValueError("Phone number format not recognised.")
    return raw


def mask_phone(phone):
    """Return masked phone: 070****545. Safe to log."""
    if not phone:
        return "***"
    s = str(phone)
    if len(s) <= 6:
        return "***"
    return s[:3] + "****" + s[-3:]


# ── Config ────────────────────────────────────────────────────────────────────

def _get_config():
    return {
        "api_url":   frappe.conf.get("smartlife_phahapa_sms_api_url", _DEFAULT_API_URL),
        "username":  frappe.conf.get("smartlife_phahapa_sms_username", ""),
        "password":  frappe.conf.get("smartlife_phahapa_sms_password", ""),
        "sender_id": frappe.conf.get("smartlife_phahapa_sms_sender_id", "SmartLife"),
        "api_key":   frappe.conf.get("smartlife_phahapa_sms_api_key", ""),
        "demo_mode": bool(frappe.conf.get("smartlife_phahapa_sms_demo_mode", 1)),
    }


def get_config_status():
    """Return booleans/status strings only — never expose secret values."""
    cfg = _get_config()
    return {
        "configured": bool(cfg["username"] and cfg["password"]),
        "api_url":    "configured" if cfg["api_url"] else "not_configured",
        "username":   "configured" if cfg["username"] else "not_configured",
        "password":   "configured" if cfg["password"] else "not_configured",
        "sender_id":  "configured" if cfg["sender_id"] else "not_configured",
        "api_key":    "configured" if cfg["api_key"] else "not_configured",
        "demo_mode":  cfg["demo_mode"],
    }


# ── Public send function ──────────────────────────────────────────────────────

def send_phahapa_sms(
    phone_number,
    message,
    client_reference=None,
    metadata=None,
):
    """
    Send an SMS via Phahapa/eGoSMS.

    Returns a structured result dict. Never raises — always returns ok=True/False.
    Never logs credentials. Never logs the full phone number.
    """
    # Mask first — used in all return paths
    try:
        normalised = normalise_phone(phone_number)
        masked     = mask_phone(phone_number)
    except ValueError as exc:
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            str(exc),
            "recipient_masked": mask_phone(phone_number),
            "demo_mode":        False,
        }

    cfg = _get_config()

    # Demo mode — no real send
    if cfg["demo_mode"]:
        return {
            "ok":               True,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Demo Mode",
            "message":          "SMS not sent because SmartLife messaging demo mode is enabled.",
            "recipient_masked": masked,
            "demo_mode":        True,
        }

    # Config gate
    if not cfg["username"] or not cfg["password"]:
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            "Phahapa SMS credentials not configured in site config.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }

    # Truncate message
    sms_text = str(message or "")[:_MAX_SMS_CHARS]
    if not sms_text:
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            "SMS message body is empty.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }

    payload = {
        "Username":         cfg["username"],
        "Password":         cfg["password"],
        "SenderId":         cfg["sender_id"] or "SmartLife",
        "MessageParameters": [
            {"Number": normalised, "Text": sms_text}
        ],
    }

    try:
        resp = requests.post(
            cfg["api_url"],
            json=payload,
            timeout=_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}

        # eGoSMS returns various response shapes depending on version
        provider_ref = (
            data.get("MessageId")
            or data.get("message_id")
            or data.get("Data", {}).get("MessageId") if isinstance(data.get("Data"), dict) else None
            or client_reference
            or "egosms-ok"
        )
        # Check for provider-level error in body
        status_val = str(data.get("Status", "")).lower()
        if status_val and status_val not in ("success", "ok", "200", "1"):
            err_msg = data.get("Description") or data.get("Message") or f"Provider status: {status_val}"
            frappe.log_error(f"eGoSMS reported: {err_msg}", "SmartLife Phahapa SMS")
            return {
                "ok":               False,
                "provider":         "phahapa_egosms",
                "channel":          "SMS",
                "status":           "Failed",
                "error":            "SMS provider reported a send failure. Check logs.",
                "recipient_masked": masked,
                "demo_mode":        False,
            }

        return {
            "ok":                 True,
            "provider":           "phahapa_egosms",
            "channel":            "SMS",
            "status":             "Sent",
            "provider_reference": str(provider_ref),
            "recipient_masked":   masked,
            "demo_mode":          False,
        }

    except requests.exceptions.Timeout:
        frappe.log_error("Phahapa SMS request timed out", "SmartLife Phahapa SMS")
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            "SMS provider timed out. Please retry.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }
    except requests.exceptions.HTTPError as exc:
        safe_msg = f"SMS provider returned HTTP {exc.response.status_code}."
        frappe.log_error(safe_msg, "SmartLife Phahapa SMS")
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            safe_msg,
            "recipient_masked": masked,
            "demo_mode":        False,
        }
    except Exception:
        frappe.log_error("Phahapa SMS send error", "SmartLife Phahapa SMS")
        return {
            "ok":               False,
            "provider":         "phahapa_egosms",
            "channel":          "SMS",
            "status":           "Failed",
            "error":            "SMS send failed. Check server logs.",
            "recipient_masked": masked,
            "demo_mode":        False,
        }
