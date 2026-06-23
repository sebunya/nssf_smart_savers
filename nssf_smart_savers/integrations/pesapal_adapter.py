"""
SmartLife Flexi — Pesapal Payment Adapter (Phase 3)
===================================================
Three modes:  demo  |  sandbox  |  live (blocked)

Demo mode is the default and activates automatically when credentials
are missing. Sandbox mode talks to Pesapal's CyberQA environment.
Live mode is intentionally blocked.

Config keys read from ``frappe.conf`` (site_config.json):
    pesapal_mode, pesapal_consumer_key, pesapal_consumer_secret,
    pesapal_callback_url, pesapal_ipn_url, pesapal_ipn_id
"""

import frappe
import json
import uuid

# ── Mode Constants ──────────────────────────────────────────────────
DEMO_MODE = "demo"
SANDBOX_MODE = "sandbox"
LIVE_MODE = "live"

# ── Base URLs ───────────────────────────────────────────────────────
_SANDBOX_BASE = "https://cybqa.pesapal.com/pesapalv3"
_LIVE_BASE = "https://pay.pesapal.com/v3"

DEMO_NOTICE = (
    "Running in DEMO mode — no real payment processed. "
    "Set pesapal_consumer_key in site_config to enable sandbox."
)


# =====================================================================
# Configuration helpers
# =====================================================================

def get_pesapal_config():
    """Read Pesapal config from ``frappe.conf``. Never hard-coded."""
    return {
        "mode": frappe.conf.get("pesapal_mode", DEMO_MODE),
        "consumer_key": frappe.conf.get("pesapal_consumer_key", ""),
        "consumer_secret": frappe.conf.get("pesapal_consumer_secret", ""),
        "callback_url": frappe.conf.get("pesapal_callback_url", ""),
        "ipn_url": frappe.conf.get("pesapal_ipn_url", ""),
        "ipn_id": frappe.conf.get("pesapal_ipn_id", ""),
    }


def is_demo_mode():
    """Returns True if explicitly set to 'demo' or if keys are missing."""
    config = get_pesapal_config()
    if config["mode"] == DEMO_MODE:
        return True
    if not config["consumer_key"] or not config["consumer_secret"]:
        return True
    return False


def _get_base_url(config):
    """Retrieve base API endpoint. Raises if live is targeted."""
    mode = config.get("mode", DEMO_MODE)
    if mode == LIVE_MODE:
        frappe.throw(
            "Live Pesapal environment is blocked. Compliance reviews must pass first.",
            frappe.PermissionError
        )
    return _SANDBOX_BASE


# =====================================================================
# API integration endpoints
# =====================================================================

def get_auth_token(config=None):
    """
    Authenticate with Pesapal OAuth2 endpoint.
    POST /api/Auth/RequestToken.
    """
    if is_demo_mode():
        return "DEMO-TOKEN-MOCK-AUTHENTICATION-ONLY"

    config = config or get_pesapal_config()
    base_url = _get_base_url(config)
    url = f"{base_url}/api/Auth/RequestToken"
    payload = {
        "consumer_key": config["consumer_key"],
        "consumer_secret": config["consumer_secret"]
    }

    try:
        import requests
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        r.raise_for_status()
        res = r.json()
        return res.get("token")
    except Exception as e:
        frappe.log_error(
            message=f"Failed to fetch Pesapal auth token: {str(e)[:500]}",
            title="SmartLife Pesapal Auth Error"
        )
        return None


def create_demo_order(amount, currency="UGX", description="SmartLife Flexi Demo Contribution", reference=None):
    """Generate a clean demo redirection response."""
    ref = reference or f"SL-DEMO-{str(uuid.uuid4())[:8].upper()}"
    tracking_id = f"DEMO-{str(uuid.uuid4())}"
    return {
        "success": True,
        "redirect_url": f"/smartlife-checkout-demo?status=demo_pending&ref={ref}&tracking_id={tracking_id}",
        "tracking_id": tracking_id,
        "demo_mode": True,
        "message": DEMO_NOTICE
    }


def submit_order(intent_name, amount, currency="UGX", description="SmartLife Flexi Demo", callback_url=None):
    """
    Register transaction details on the gateway and get redirect link.
    POST /api/Transactions/SubmitOrderRequest.
    """
    config = get_pesapal_config()
    if is_demo_mode():
        return create_demo_order(amount, currency, description, intent_name)

    base_url = _get_base_url(config)
    token = get_auth_token(config)
    if not token:
        return {
            "success": False,
            "message": "Auth failure. Falling back to Demo checkout."
        }

    url = f"{base_url}/api/Transactions/SubmitOrderRequest"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "id": intent_name,
        "currency": currency,
        "amount": float(amount),
        "description": description,
        "callback_url": callback_url or config["callback_url"],
        "notification_id": config["ipn_id"],
        "billing_address": {
            "email_address": "sandbox-billing@nssfug.org",
            "phone_number": "0700000000",
            "country_code": "UG",
            "first_name": "Sandbox",
            "last_name": "User"
        }
    }

    try:
        import requests
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        res = r.json()
        redirect_url = res.get("redirect_url")
        tracking_id = res.get("order_tracking_id")
        if redirect_url and tracking_id:
            return {
                "success": True,
                "redirect_url": redirect_url,
                "tracking_id": tracking_id,
                "demo_mode": False
            }
        else:
            return {
                "success": False,
                "message": f"Malformed payload from Pesapal: {res}"
            }
    except Exception as e:
        frappe.log_error(
            message=f"SubmitOrderRequest error: {str(e)[:500]}",
            title="SmartLife Pesapal Order Error"
        )
        return {
            "success": False,
            "message": f"Sandbox request error: {str(e)[:100]}"
        }


def get_transaction_status(tracking_id):
    """
    Query the gateway status.
    GET /api/Transactions/GetTransactionStatus?orderTrackingId={tracking_id}.
    """
    if is_demo_mode() or tracking_id.startswith("DEMO-"):
        return {
            "success": True,
            "payment_status_description": "COMPLETED",
            "status_code": 1,
            "amount": 0,
            "demo": True
        }

    config = get_pesapal_config()
    base_url = _get_base_url(config)
    token = get_auth_token(config)
    if not token:
        return {"success": False, "message": "Failed to authenticate query status."}

    url = f"{base_url}/api/Transactions/GetTransactionStatus?orderTrackingId={tracking_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        import requests
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        res = r.json()
        return {
            "success": True,
            "payment_status_description": res.get("payment_status_description"),
            "status_code": res.get("status_code"),
            "amount": res.get("amount"),
            "demo": False,
            "raw": res
        }
    except Exception as e:
        frappe.log_error(
            message=f"GetTransactionStatus error for {tracking_id}: {str(e)[:500]}",
            title="SmartLife Pesapal Status Query Error"
        )
        return {"success": False, "message": str(e)}


def verify_payment_callback(params):
    """Parse payment params returned in checkout callback."""
    tracking_id = params.get("OrderTrackingId") or params.get("pesapal_transaction_tracking_id")
    merchant_ref = params.get("OrderMerchantReference") or params.get("pesapal_merchant_reference")

    if not tracking_id:
        return {"success": False, "message": "Missing Tracking ID parameters."}

    status_data = get_transaction_status(tracking_id)
    status_data["merchant_reference"] = merchant_ref
    status_data["tracking_id"] = tracking_id
    return status_data


def handle_ipn(params):
    """
    Parse server-to-server IPN message payload.
    Must always return a dictionary and never throw exceptions.
    """
    try:
        tracking_id = params.get("OrderTrackingId")
        notification_type = params.get("OrderNotificationType")
        merchant_ref = params.get("OrderMerchantReference")

        if not tracking_id:
            return {"status": "error", "message": "IPN missing OrderTrackingId"}

        status_data = get_transaction_status(tracking_id)
        return {
            "status": "ok",
            "tracking_id": tracking_id,
            "notification_type": notification_type,
            "merchant_reference": merchant_ref,
            "payment_status": status_data.get("payment_status_description"),
            "status_code": status_data.get("status_code")
        }
    except Exception as e:
        frappe.log_error(
            message=f"IPN hook execution failure: {str(e)[:500]}",
            title="SmartLife IPN Callback Exception"
        )
        return {"status": "error", "message": str(e)}
