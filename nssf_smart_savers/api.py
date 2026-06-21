"""
SmartLife Flexi - Whitelisted API Methods
Demo environment. No real member data should be submitted.
"""
import frappe
import json
import uuid
from datetime import datetime

from nssf_smart_savers.utils.projection import calculate_projection, validate_minimum
from nssf_smart_savers.utils.personalisation import get_personalised_plan
from nssf_smart_savers.utils.analytics import (
    sanitise_event_params,
    get_period_band,
    get_target_band,
    get_country_band,
)
from nssf_smart_savers.utils.safe_input import (
    looks_like_nin,
    looks_like_phone,
    looks_like_email,
    sanitise_demo_text,
)

DEMO_NOTICE = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."


def _check_pii(*values):
    """Raise error if any value looks like real PII."""
    for value in values:
        if not value:
            continue
        v = str(value)
        if looks_like_nin(v):
            frappe.throw("Demo environment: do not enter real NSSF member data (NIN detected).")
        if looks_like_phone(v):
            frappe.throw("Demo environment: do not enter real phone numbers.")
        if looks_like_email(v):
            frappe.throw("Demo environment: do not enter real email addresses.")


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


@frappe.whitelist(allow_guest=True)
def get_projection(initial_deposit, periodic_contribution, frequency, years):
    """Calculate savings projection. Demo environment."""
    _check_pii(initial_deposit, periodic_contribution)
    initial_deposit = _safe_float(initial_deposit)
    periodic_contribution = _safe_float(periodic_contribution)
    years = _safe_int(years, 1)
    if not validate_minimum(periodic_contribution, frequency):
        frappe.throw("Minimum contribution is UGX 5,000.")
    result = calculate_projection(initial_deposit, periodic_contribution, frequency, years)
    result["demo_notice"] = DEMO_NOTICE
    return result


@frappe.whitelist(allow_guest=True)
def get_personalised_plan_api(
    segment,
    goal,
    target_amount,
    years,
    frequency,
    initial_deposit,
    source_of_income="",
    industry="",
    country="Uganda",
    staff_assisted=False,
    objection="",
):
    """Generate personalised plan. Demo environment."""
    _check_pii(source_of_income, industry)
    segment = sanitise_demo_text(segment, 50)
    goal = sanitise_demo_text(goal, 50)
    plan = get_personalised_plan(
        segment=segment,
        goal=goal,
        target_amount=_safe_float(target_amount),
        years=_safe_int(years, 1),
        frequency=frequency,
        initial_deposit=_safe_float(initial_deposit),
        source_of_income=sanitise_demo_text(source_of_income, 100),
        industry=sanitise_demo_text(industry, 100),
        country=sanitise_demo_text(country, 50),
        staff_assisted=bool(staff_assisted),
        objection=objection or None,
    )
    plan["demo_notice"] = DEMO_NOTICE
    return plan


@frappe.whitelist(allow_guest=True)
def submit_demo_lead(
    segment,
    goal,
    frequency,
    years,
    target_amount,
    initial_deposit,
    source_of_income="",
    industry="",
    country="Uganda",
    staff_assisted=False,
):
    """Create a SmartLife Demo Lead record. Demo environment."""
    _check_pii(source_of_income, industry)
    segment = sanitise_demo_text(segment, 50)
    goal = sanitise_demo_text(goal, 50)
    years = _safe_int(years, 1)
    target_amount = _safe_float(target_amount)
    initial_deposit = _safe_float(initial_deposit)

    from nssf_smart_savers.utils.personalisation import GOAL_MESSAGES, SEGMENT_PROFILES
    goal_data = GOAL_MESSAGES.get(goal, GOAL_MESSAGES["other"])

    analytics_labels = json.dumps({
        "journey_type": "staff_assist" if staff_assisted else "self_serve",
        "segment": segment,
        "goal_category": goal,
        "frequency": frequency,
        "period_band": get_period_band(years),
        "target_band": get_target_band(target_amount),
        "country_band": get_country_band(country),
    })

    session_id = str(uuid.uuid4())[:16]
    doc = frappe.get_doc({
        "doctype": "SmartLife Demo Lead",
        "segment": segment,
        "goal": goal,
        "goal_label": goal_data["label"],
        "target_amount": target_amount,
        "years": years,
        "frequency": frequency,
        "initial_deposit": initial_deposit,
        "source_of_income": sanitise_demo_text(source_of_income, 100),
        "industry": sanitise_demo_text(industry, 100),
        "country": sanitise_demo_text(country, 50),
        "staff_assisted": 1 if staff_assisted else 0,
        "journey_type": "staff_assist" if staff_assisted else "self_serve",
        "lead_stage": "New",
        "analytics_labels": analytics_labels,
        "created_session_id": session_id,
        "demo_note": DEMO_NOTICE,
    })
    doc.insert(ignore_permissions=True)
    return {
        "success": True,
        "lead_name": doc.name,
        "session_id": session_id,
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist(allow_guest=True)
def submit_staff_assist(
    segment,
    goal,
    initial_deposit_ready,
    objection="",
    follow_up_channel="",
    staff_owner="",
):
    """Create a SmartLife Staff Assist Session. Demo environment."""
    _check_pii(staff_owner)
    segment = sanitise_demo_text(segment, 50)
    goal = sanitise_demo_text(goal, 50)

    from nssf_smart_savers.utils.personalisation import OBJECTION_SCRIPTS
    plan = get_personalised_plan(
        segment=segment, goal=goal, target_amount=0, years=1,
        frequency="monthly", initial_deposit=0, staff_assisted=True,
        objection=objection or None,
    )
    objection_script = ""
    if objection and objection in OBJECTION_SCRIPTS:
        objection_script = OBJECTION_SCRIPTS[objection]["staff_script"]

    doc = frappe.get_doc({
        "doctype": "SmartLife Staff Assist Session",
        "prospect_segment": segment,
        "goal": goal,
        "initial_deposit_ready": initial_deposit_ready or "Unsure",
        "objection": sanitise_demo_text(objection, 100),
        "follow_up_channel": follow_up_channel or "None",
        "staff_owner": sanitise_demo_text(staff_owner, 100),
        "conversion_stage": "New Prospect",
        "next_best_action": plan["next_best_action"],
        "recommended_pitch": plan["staff_script"],
        "objection_script": objection_script,
        "is_demo": 1,
    })
    doc.insert(ignore_permissions=True)
    return {
        "success": True,
        "session_name": doc.name,
        "staff_script": plan["staff_script"],
        "objection_response": plan["objection_response"],
        "next_best_action": plan["next_best_action"],
        "crm_stage_suggestion": "New Prospect",
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist(allow_guest=True)
def simulate_payment(demo_lead_name, amount, frequency, goal):
    """Simulate a payment for demo purposes. No real payment is processed."""
    _check_pii(demo_lead_name)
    amount = _safe_float(amount)
    idempotency_key = str(uuid.uuid4())
    now_str = datetime.now().isoformat()

    doc = frappe.get_doc({
        "doctype": "SmartLife Demo Payment",
        "demo_lead": sanitise_demo_text(demo_lead_name, 100),
        "amount": amount,
        "frequency": sanitise_demo_text(frequency, 50),
        "goal": sanitise_demo_text(goal, 50),
        "payment_status": "Initiated",
        "payment_reference": "SL-DEMO-" + idempotency_key[:8].upper(),
        "provider_mode": "demo",
        "provider_name": "Pesapal (Demo)",
        "initiated_at": datetime.now(),
        "idempotency_key": idempotency_key,
        "event_log": json.dumps([{"event": "initiated", "timestamp": now_str, "demo": True}]),
        "is_demo": 1,
    })
    doc.insert(ignore_permissions=True)
    doc.payment_status = "Success"
    doc.completed_at = datetime.now()
    doc.event_log = json.dumps([
        {"event": "initiated", "timestamp": now_str, "demo": True},
        {"event": "success", "timestamp": datetime.now().isoformat(), "demo": True},
    ])
    doc.save(ignore_permissions=True)

    return {
        "success": True,
        "payment_name": doc.name,
        "payment_reference": doc.payment_reference,
        "payment_status": "Success",
        "amount": amount,
        "demo_notice": DEMO_NOTICE,
        "simulated": True,
    }


@frappe.whitelist(allow_guest=True)
def log_analytics_event(event_name, params):
    """Log an analytics event. Demo environment."""
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except (ValueError, TypeError):
            params = {}
    safe_params = sanitise_event_params(params)
    doc = frappe.get_doc({
        "doctype": "SmartLife Integration Event",
        "event_type": sanitise_demo_text(str(event_name), 100),
        "event_source": "web",
        "event_status": "simulated",
        "payload_summary": json.dumps(safe_params)[:200],
        "is_simulated": 1,
    })
    doc.insert(ignore_permissions=True)
    return {"success": True, "demo_notice": DEMO_NOTICE}


@frappe.whitelist(allow_guest=True)
def request_support(subject, channel_preference="", staff_assist=False):
    """Submit a support request. Demo environment."""
    _check_pii(subject)
    subject = sanitise_demo_text(subject, 200)
    doc = frappe.get_doc({
        "doctype": "SmartLife Demo Notification",
        "notification_type": "Email",
        "channel": "Demo Log",
        "recipient_type": "support",
        "event_trigger": "support_request",
        "template_name": "support_request",
        "rendered_body": "Subject: " + subject + "\nChannel: " + str(channel_preference) + "\nStaff Assist: " + str(staff_assist),
        "status": "Simulated",
        "simulated": 1,
    })
    doc.insert(ignore_permissions=True)
    return {
        "success": True,
        "ticket_ref": doc.name,
        "message": "Your support request has been logged. A team member will follow up. (Demo environment)",
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist(allow_guest=True)
def log_dropoff(step_name, segment="", goal="", journey_type="self_serve"):
    """Log a journey dropoff event."""
    session_id = str(uuid.uuid4())[:16]
    doc = frappe.get_doc({
        "doctype": "SmartLife Dropoff Event",
        "journey_type": sanitise_demo_text(journey_type, 50),
        "step_name": sanitise_demo_text(step_name, 100),
        "segment": sanitise_demo_text(segment, 50),
        "goal": sanitise_demo_text(goal, 50),
        "session_id": session_id,
    })
    doc.insert(ignore_permissions=True)
    return {"success": True, "demo_notice": DEMO_NOTICE}
