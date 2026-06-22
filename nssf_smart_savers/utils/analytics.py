"""
SmartLife Flexi - Analytics utilities.
Safe event logging, no PII.
Demo environment only.
"""
import uuid
import json
import frappe

# Strict allowlist: only these keys may be forwarded to analytics.
# Everything else — especially PII — is silently dropped.
# PII that must never reach analytics:
#   first_name, last_name, full_name, phone, primary_phone, email,
#   nin, national_id, date_of_birth, dob, birthday_day, birthday_month,
#   age_years, exact_age, notes, remarks, raw_remarks,
#   user_submitted_text, free_text, otp, password, payment_ref
ALLOWED_PARAMS = [
    'journey_type', 'segment', 'goal_category', 'frequency', 'period_band',
    'target_band', 'source_category', 'industry_category', 'country_band',
    'step_name', 'step_number', 'saver_type', 'staff_assisted',
    'payment_status', 'completion_status', 'dropoff_step', 'lead_stage',
    # Phase 2 safe dimensions
    'lead_temperature', 'consent_status', 'source_route', 'staff_view_type',
    'onboarding_stage', 'age_band', 'gender_category', 'country_category',
    'demo_environment',
]


def create_anonymous_session_id():
    return 'sl-' + str(uuid.uuid4())[:12]


def sanitise_event_params(params):
    """Return only allowed, PII-free params."""
    if not isinstance(params, dict):
        return {}
    safe = {}
    for k in ALLOWED_PARAMS:
        if k in params and params[k] is not None:
            safe[k] = str(params[k])[:100]
    safe['demo_environment'] = 'true'
    return safe


def get_period_band(years):
    years = int(years or 0)
    if years <= 1: return '1y'
    if years <= 3: return '1-3y'
    if years <= 5: return '3-5y'
    if years <= 10: return '5-10y'
    return '10y+'


def get_target_band(amount):
    amount = float(amount or 0)
    if amount < 500000: return '<500k'
    if amount < 2000000: return '500k-2m'
    if amount < 10000000: return '2m-10m'
    if amount < 50000000: return '10m-50m'
    return '50m+'


def get_country_band(country):
    c = str(country or '').lower()
    if c in ('uganda', 'ug'): return 'uganda'
    if c in ('kenya', 'tanzania', 'rwanda', 'burundi', 'south sudan', 'drc'): return 'east_africa'
    if c in ('', 'unknown'): return 'unknown'
    return 'diaspora'


def validate_analytics_payload(payload):
    """Validate payload is safe for analytics."""
    from nssf_smart_savers.utils.privacy import is_pii_safe
    for v in payload.values():
        if not is_pii_safe(str(v)):
            return False
    return True


def log_safe_event(event_name, payload):
    """Log a safe analytics event to SmartLife Integration Event."""
    try:
        safe = sanitise_event_params(payload)
        if not validate_analytics_payload(safe):
            frappe.log_error('SmartLife analytics: unsafe payload blocked', 'SmartLife Analytics')
            return
        doc = frappe.get_doc({
            'doctype': 'SmartLife Integration Event',
            'event_type': str(event_name)[:100],
            'event_source': 'web',
            'event_status': 'simulated',
            'payload_summary': json.dumps(safe)[:200],
            'is_simulated': 1,
        })
        doc.insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(str(e), 'SmartLife Analytics Event Error')
