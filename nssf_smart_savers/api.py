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
from nssf_smart_savers.lead_scoring import calculate_lead_score

DEMO_NOTICE = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."

# ── Access control helpers ──────────────────────────────────────────────────

ALLOWED_PERSONALISATION_ROLES = {
    "SmartLife Personalisation Team",
    "NSSF Staff",
    "System Manager",
}


def _is_guest():
    return frappe.session.user == "Guest"


def _has_allowed_personalisation_role(user=None):
    user = user or frappe.session.user
    if not user or user == "Guest":
        return False
    user_roles = set(frappe.get_roles(user))
    return bool(user_roles.intersection(ALLOWED_PERSONALISATION_ROLES))


def _require_authenticated_staff():
    """Require any authenticated Frappe session. Blocks Guest."""
    if _is_guest():
        frappe.throw(
            "Staff sign-in required for this action.",
            frappe.PermissionError,
        )


def _require_personalisation_access():
    """
    Require authenticated session with an approved Personalisation Team role.
    Approved roles: SmartLife Personalisation Team, NSSF Staff, System Manager.
    """
    if _is_guest():
        frappe.throw(
            "Personalisation team sign-in required to view full lead details.",
            frappe.PermissionError,
        )
    if not _has_allowed_personalisation_role():
        frappe.throw(
            "You do not have permission to view full SmartLife lead PII.",
            frappe.PermissionError,
        )


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
    lead_dict = {
        "segment": segment,
        "goal": goal,
        "frequency": frequency,
        "initial_deposit": initial_deposit,
        "target_amount": target_amount,
        "staff_assisted": 1 if staff_assisted else 0,
        "consent_to_contact": 0,
    }
    scoring = calculate_lead_score(lead_dict)
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
        "lead_status": "Goal Selected" if goal else "New",
        "lead_score": scoring["lead_score"],
        "lead_temperature": scoring["lead_temperature"],
        "next_best_action": scoring["next_best_action"],
        "source_route": "/smartlife-staff-assist" if staff_assisted else "/smartlife-self-serve",
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
def submit_personal_details(data=None):
    """
    Accepts personal details from Step 2 of the self-serve flow.
    Accepts date_of_birth (ISO date string); computes age_years, age_band,
    birthday_month, birthday_day server-side.
    PII is stored in Frappe DocType only — never forwarded to analytics.
    """
    from datetime import date
    import re as _re

    if isinstance(data, str):
        data = json.loads(data)
    if not isinstance(data, dict):
        frappe.throw("Invalid payload.")

    first_name        = sanitise_demo_text(str(data.get("first_name") or ""), 80)
    last_name         = sanitise_demo_text(str(data.get("last_name") or ""), 80)
    primary_phone     = sanitise_demo_text(str(data.get("primary_phone") or ""), 30)
    alt_phone         = sanitise_demo_text(str(data.get("alt_phone") or ""), 30)
    email             = sanitise_demo_text(str(data.get("email") or ""), 120)
    country           = sanitise_demo_text(str(data.get("country_of_residence") or ""), 60)
    gender            = sanitise_demo_text(str(data.get("gender") or ""), 30)
    preferred_channel = sanitise_demo_text(str(data.get("preferred_contact_channel") or ""), 30)
    saver_type        = sanitise_demo_text(str(data.get("saver_type") or ""), 50)
    dob_str           = str(data.get("date_of_birth") or "").strip()
    consent           = bool(data.get("consent_to_contact", False))

    if not (first_name and last_name and primary_phone and country and consent):
        frappe.throw("Required fields missing: first_name, last_name, primary_phone, country_of_residence, consent_to_contact.")

    # Validate and compute DOB fields
    if not dob_str or not _re.match(r'^\d{4}-\d{2}-\d{2}$', dob_str):
        frappe.throw("date_of_birth is required and must be in YYYY-MM-DD format.")
    try:
        dob = date.fromisoformat(dob_str)
    except ValueError:
        frappe.throw("date_of_birth is not a valid date.")
    today = date.today()
    if dob >= today:
        frappe.throw("date_of_birth cannot be today or in the future.")
    age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age_years < 16 or age_years > 100:
        frappe.throw("date_of_birth implies an age outside the allowed range (16–100).")
    birthday_month = dob.month
    birthday_day   = dob.day
    age_band = (
        "16-19" if age_years < 20 else
        "20-24" if age_years < 25 else
        "25-34" if age_years < 35 else
        "35-44" if age_years < 45 else
        "45-54" if age_years < 55 else "55+"
    )

    session_id = str(uuid.uuid4())[:16]
    doc = frappe.get_doc({
        "doctype": "SmartLife Demo Lead",
        "first_name":              first_name,
        "last_name":               last_name,
        "primary_phone":           primary_phone,
        "alt_phone":               alt_phone,
        "email_address":           email,
        "country":                 country,
        "gender":                  gender,
        "date_of_birth":           dob_str,
        "age_years":               age_years,
        "age_band":                age_band,
        "birthday_month":          birthday_month,
        "birthday_day":            birthday_day,
        "preferred_contact_channel": preferred_channel,
        "consent_to_contact":      1 if consent else 0,
        "segment":                 saver_type,
        "lead_stage":              "Prospect",
        "lead_status":             "Personal Details Captured",
        "journey_type":            "self_serve",
        "source_route":            "/smartlife-self-serve",
        "created_session_id":      session_id,
        "demo_note":               DEMO_NOTICE,
        "analytics_labels": json.dumps({
            "age_band":         age_band,
            "gender_category":  "undisclosed" if gender == "prefer_not_to_say" else gender,
            "country_category": "local" if country.lower() == "uganda" else "international",
            "consent_status":   "consented" if consent else "not_consented",
        }),
    })
    doc.insert(ignore_permissions=True)
    # Run scoring now that PII fields exist server-side
    scoring = calculate_lead_score(doc.as_dict())
    doc.lead_score       = scoring["lead_score"]
    doc.lead_temperature = scoring["lead_temperature"]
    doc.next_best_action = scoring["next_best_action"]
    doc.save(ignore_permissions=True)
    # Return only non-PII: session reference and anonymous bands
    return {
        "success":      True,
        "session_id":   session_id,
        "age_band":     age_band,
        "demo_notice":  DEMO_NOTICE,
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


# ── Phase 2: Lead Operating System ─────────────────────────────────────────

def _mask_phone(phone):
    """Mask phone for staff-facing display: 070****545"""
    p = str(phone or "")
    if len(p) >= 9:
        return p[:3] + "****" + p[-3:]
    return "***"


def _mask_email(email):
    """Mask email for staff-facing display: ro***@domain.com"""
    e = str(email or "")
    if "@" in e:
        local, domain = e.split("@", 1)
        return local[:2] + "***@" + domain
    return "***"


@frappe.whitelist(allow_guest=True)
def score_lead(session_id):
    """
    Return lead score data for a given session_id. No PII returned.
    Demo environment — staff use only.
    """
    _check_pii(session_id)
    sid = sanitise_demo_text(session_id, 40)
    leads = frappe.get_all(
        "SmartLife Demo Lead",
        filters={"created_session_id": sid},
        fields=["name", "consent_to_contact", "initial_deposit", "target_amount",
                "frequency", "segment", "projection_viewed", "checkout_started",
                "payment_completed", "staff_assisted", "preferred_contact_channel",
                "age_band", "goal", "source_route"],
        limit=1,
    )
    if not leads:
        return {"success": False, "message": "Lead not found", "demo_notice": DEMO_NOTICE}
    scoring = calculate_lead_score(leads[0])
    return {
        "success": True,
        "lead_score":       scoring["lead_score"],
        "lead_temperature": scoring["lead_temperature"],
        "next_best_action": scoring["next_best_action"],
        "score_reasons":    scoring["score_reasons"],
        "demo_notice":      DEMO_NOTICE,
    }


@frappe.whitelist(allow_guest=True)
def get_lead_summary():
    """
    Return aggregate lead counts grouped by status and temperature.
    No PII — counts only. Demo environment — staff use only.
    """
    total = frappe.db.count("SmartLife Demo Lead")

    def _count_by(field, value):
        return frappe.db.count("SmartLife Demo Lead", filters={field: value})

    statuses = [
        "New", "Personal Details Captured", "Goal Selected",
        "Projection Viewed", "Checkout Started", "Payment Pending",
        "Payment Completed", "Staff Follow-up Required",
        "Contacted", "Converted", "Dormant", "Disqualified",
    ]
    by_status = {s: _count_by("lead_status", s) for s in statuses}

    temps = ["Hot", "Warm", "Cold"]
    by_temp = {t: _count_by("lead_temperature", t) for t in temps}

    segments = frappe.db.get_all(
        "SmartLife Demo Lead",
        fields=["segment", "count(name) as cnt"],
        group_by="segment",
        as_list=False,
        limit=20,
    )

    goals = frappe.db.get_all(
        "SmartLife Demo Lead",
        fields=["goal", "count(name) as cnt"],
        group_by="goal",
        as_list=False,
        limit=20,
    )

    channels = frappe.db.get_all(
        "SmartLife Demo Lead",
        fields=["preferred_contact_channel", "count(name) as cnt"],
        group_by="preferred_contact_channel",
        as_list=False,
        limit=20,
    )

    return {
        "success":    True,
        "total":      total,
        "by_status":  by_status,
        "by_temp":    by_temp,
        "by_segment": {r.segment: r.cnt for r in segments if r.segment},
        "by_goal":    {r.goal: r.cnt for r in goals if r.goal},
        "by_channel": {r.preferred_contact_channel: r.cnt for r in channels if r.preferred_contact_channel},
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist(allow_guest=True)
def get_staff_queue(limit=50):
    """
    Return a staff action queue: leads requiring follow-up.
    PII is masked. Demo environment — staff use only.
    """
    limit = min(_safe_int(limit, 50), 200)
    leads = frappe.get_all(
        "SmartLife Demo Lead",
        filters=[["lead_status", "in", [
            "Staff Follow-up Required", "Personal Details Captured",
            "Goal Selected", "Checkout Started", "Payment Pending",
        ]]],
        fields=["name", "lead_status", "lead_temperature", "lead_score",
                "next_best_action", "segment", "goal", "age_band",
                "preferred_contact_channel", "consent_to_contact",
                "primary_phone", "email_address", "assigned_staff",
                "next_follow_up_on", "source_route", "creation"],
        order_by="lead_score desc, creation asc",
        limit=limit,
    )
    safe_leads = []
    for l in leads:
        safe_leads.append({
            "name":                  l.name,
            "lead_status":           l.lead_status or "New",
            "lead_temperature":      l.lead_temperature or "Cold",
            "lead_score":            l.lead_score or 0,
            "next_best_action":      l.next_best_action or "—",
            "segment":               l.segment or "—",
            "goal":                  l.goal or "—",
            "age_band":              l.age_band or "—",
            "preferred_contact_channel": l.preferred_contact_channel or "—",
            "consent_to_contact":    bool(l.consent_to_contact),
            "phone_masked":          _mask_phone(l.primary_phone) if l.primary_phone else "—",
            "email_masked":          _mask_email(l.email_address) if l.email_address else "—",
            "assigned_staff":        l.assigned_staff or "Unassigned",
            "next_follow_up_on":     str(l.next_follow_up_on) if l.next_follow_up_on else "—",
            "source_route":          l.source_route or "—",
        })
    return {
        "success":    True,
        "queue":      safe_leads,
        "count":      len(safe_leads),
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist()
def update_follow_up_status(lead_name, follow_up_outcome, new_status="Contacted"):
    """
    Update follow-up outcome and lead status.
    Requires authenticated session. Staff use only. Demo environment.
    """
    _require_authenticated_staff()
    _check_pii(lead_name, follow_up_outcome)
    lead_name      = sanitise_demo_text(lead_name, 50)
    outcome        = sanitise_demo_text(follow_up_outcome, 200)
    allowed_status = [
        "New", "Personal Details Captured", "Goal Selected", "Projection Viewed",
        "Checkout Started", "Payment Pending", "Payment Completed",
        "Staff Follow-up Required", "Contacted", "Converted", "Dormant", "Disqualified",
    ]
    if new_status not in allowed_status:
        frappe.throw(f"Invalid status: {new_status}")
    doc = frappe.get_doc("SmartLife Demo Lead", lead_name)
    doc.follow_up_outcome  = outcome
    doc.lead_status        = new_status
    from datetime import date
    doc.last_contacted_on  = date.today()
    doc.save(ignore_permissions=True)
    return {"success": True, "lead_name": lead_name, "new_status": new_status, "demo_notice": DEMO_NOTICE}


@frappe.whitelist()
def assign_lead(lead_name, staff_name):
    """
    Assign a lead to a staff member name.
    Requires authenticated session. Demo environment.
    """
    _require_authenticated_staff()
    _check_pii(lead_name)
    lead_name  = sanitise_demo_text(lead_name, 50)
    staff_name = sanitise_demo_text(staff_name, 100)
    doc = frappe.get_doc("SmartLife Demo Lead", lead_name)
    doc.assigned_staff = staff_name
    if doc.lead_status in ("New", "Personal Details Captured"):
        doc.lead_status = "Staff Follow-up Required"
    doc.save(ignore_permissions=True)
    return {"success": True, "lead_name": lead_name, "assigned_staff": staff_name, "demo_notice": DEMO_NOTICE}


@frappe.whitelist()
def update_journey_flag(session_id, flag):
    """
    Update a journey progress flag (projection_viewed, checkout_started, payment_completed).
    Requires authenticated session. Demo environment.
    """
    _require_authenticated_staff()
    _check_pii(session_id)
    allowed_flags = ("projection_viewed", "checkout_started", "payment_completed")
    if flag not in allowed_flags:
        frappe.throw(f"Invalid flag: {flag}")
    sid = sanitise_demo_text(session_id, 40)
    leads = frappe.get_all(
        "SmartLife Demo Lead",
        filters={"created_session_id": sid},
        fields=["name", "consent_to_contact", "initial_deposit", "target_amount",
                "frequency", "segment", "projection_viewed", "checkout_started",
                "payment_completed", "staff_assisted", "preferred_contact_channel",
                "age_band", "goal", "source_route"],
        limit=1,
    )
    if not leads:
        return {"success": False, "message": "Lead not found", "demo_notice": DEMO_NOTICE}
    doc = frappe.get_doc("SmartLife Demo Lead", leads[0]["name"])
    setattr(doc, flag, 1)
    status_map = {
        "projection_viewed":  "Projection Viewed",
        "checkout_started":   "Checkout Started",
        "payment_completed":  "Payment Completed",
    }
    doc.lead_status = status_map[flag]
    scoring = calculate_lead_score(doc.as_dict())
    doc.lead_score       = scoring["lead_score"]
    doc.lead_temperature = scoring["lead_temperature"]
    doc.next_best_action = scoring["next_best_action"]
    doc.save(ignore_permissions=True)
    return {
        "success":          True,
        "flag":             flag,
        "lead_temperature": scoring["lead_temperature"],
        "next_best_action": scoring["next_best_action"],
        "demo_notice":      DEMO_NOTICE,
    }


# ── Personalisation Team: full PII endpoints ────────────────────────────────

@frappe.whitelist()
def get_staff_queue_full(limit=100):
    """
    Full Personalisation Team queue: returns unmasked PII fields.
    Requires SmartLife Personalisation Team, NSSF Staff, or System Manager role.
    """
    _require_personalisation_access()
    limit = min(_safe_int(limit, 100), 500)
    leads = frappe.get_all(
        "SmartLife Demo Lead",
        fields=[
            "name", "first_name", "last_name", "gender",
            "primary_phone", "alt_phone", "email_address",
            "date_of_birth", "age_years", "age_band",
            "birthday_month", "birthday_day",
            "preferred_contact_channel", "consent_to_contact",
            "segment", "goal", "goal_label",
            "frequency", "initial_deposit", "target_amount", "years",
            "country", "source_of_income", "industry",
            "lead_status", "lead_temperature", "lead_score",
            "next_best_action", "assigned_staff",
            "last_contacted_on", "next_follow_up_on",
            "follow_up_outcome", "drop_off_reason",
            "source_route", "campaign_source", "campaign_medium", "campaign_name",
            "projection_viewed", "checkout_started", "payment_completed",
            "staff_assisted", "onboarding_stage",
            "created_session_id", "creation",
        ],
        order_by="lead_score desc, creation asc",
        limit=limit,
    )
    return {
        "success":     True,
        "queue":       [dict(l) for l in leads],
        "count":       len(leads),
        "access_tier": "personalisation_team_full_pii",
        "demo_notice": DEMO_NOTICE,
    }


@frappe.whitelist()
def get_lead_full_detail(lead_name):
    """
    Full detail for a single lead including all PII.
    Requires SmartLife Personalisation Team, NSSF Staff, or System Manager role.
    """
    _require_personalisation_access()
    lead_name = sanitise_demo_text(str(lead_name or ""), 50)
    if not lead_name:
        frappe.throw("lead_name is required.")
    doc = frappe.get_doc("SmartLife Demo Lead", lead_name)
    scoring = calculate_lead_score(doc.as_dict())
    return {
        "success":     True,
        "access_tier": "personalisation_team_full_pii",
        "lead": {
            "name":                    doc.name,
            "first_name":              doc.first_name,
            "last_name":               doc.last_name,
            "gender":                  doc.gender,
            "primary_phone":           doc.primary_phone,
            "alt_phone":               doc.alt_phone,
            "email":                   doc.email_address,
            "date_of_birth":           str(doc.date_of_birth) if doc.date_of_birth else None,
            "age_years":               doc.age_years,
            "age_band":                doc.age_band,
            "birthday_month":          doc.birthday_month,
            "birthday_day":            doc.birthday_day,
            "preferred_contact_channel": doc.preferred_contact_channel,
            "consent_to_contact":      bool(doc.consent_to_contact),
            "segment":                 doc.segment,
            "goal":                    doc.goal,
            "goal_label":              doc.goal_label,
            "frequency":               doc.frequency,
            "initial_deposit":         doc.initial_deposit,
            "target_amount":           doc.target_amount,
            "years":                   doc.years,
            "country":                 doc.country,
            "source_of_income":        doc.source_of_income,
            "industry":                doc.industry,
            "lead_status":             doc.lead_status,
            "lead_temperature":        doc.lead_temperature,
            "lead_score":              scoring["lead_score"],
            "next_best_action":        scoring["next_best_action"],
            "score_reasons":           scoring["score_reasons"],
            "assigned_staff":          doc.assigned_staff,
            "last_contacted_on":       str(doc.last_contacted_on) if doc.last_contacted_on else None,
            "next_follow_up_on":       str(doc.next_follow_up_on) if doc.next_follow_up_on else None,
            "follow_up_outcome":       doc.follow_up_outcome,
            "drop_off_reason":         doc.drop_off_reason,
            "source_route":            doc.source_route,
            "campaign_source":         doc.campaign_source,
            "campaign_medium":         doc.campaign_medium,
            "campaign_name":           doc.campaign_name,
            "projection_viewed":       bool(doc.projection_viewed),
            "checkout_started":        bool(doc.checkout_started),
            "payment_completed":       bool(doc.payment_completed),
            "staff_assisted":          bool(doc.staff_assisted),
            "onboarding_stage":        doc.onboarding_stage,
            "creation":                str(doc.creation),
        },
        "demo_notice": DEMO_NOTICE,
    }


# ── Phase 4: Messaging APIs ────────────────────────────────────────────────────


@frappe.whitelist(allow_guest=True)
def get_message_templates(channel=None):
    """
    Return available message template metadata.
    Guest-safe: returns template names, channels and trigger stages only.
    No lead PII. No message bodies.
    """
    from nssf_smart_savers.communication_templates import list_templates
    return {
        "success":   True,
        "templates": list_templates(channel=channel or None),
    }


@frappe.whitelist()
def preview_smartlife_message(lead_name, template_name, channel="SMS"):
    """
    Preview a rendered message for a lead.
    Requires authenticated staff session.
    Full PII (first_name) in preview requires approved personalisation role.
    """
    _require_personalisation_access()
    lead_name     = sanitise_demo_text(str(lead_name or ""), 50)
    template_name = sanitise_demo_text(str(template_name or ""), 80)
    channel       = str(channel or "SMS")
    if channel not in ("SMS", "Email"):
        frappe.throw("Channel must be SMS or Email.")
    from nssf_smart_savers.messaging import preview_message
    return preview_message(lead_name=lead_name, template_name=template_name, channel=channel)


@frappe.whitelist()
def send_smartlife_demo_message(lead_name, template_name, channel="SMS"):
    """
    Send a message to a lead via the specified channel.
    Requires approved personalisation role.
    Enforces consent_to_contact before send.
    Never guest-open.
    """
    _require_personalisation_access()
    lead_name     = sanitise_demo_text(str(lead_name or ""), 50)
    template_name = sanitise_demo_text(str(template_name or ""), 80)
    channel       = str(channel or "SMS")
    if not lead_name or not template_name:
        frappe.throw("lead_name and template_name are required.")
    if channel not in ("SMS", "Email"):
        frappe.throw("Channel must be SMS or Email.")
    from nssf_smart_savers.messaging import send_smartlife_message
    result = send_smartlife_message(
        lead_name=lead_name,
        template_name=template_name,
        channel=channel,
        staff_user=frappe.session.user,
    )
    return result


@frappe.whitelist()
def get_communication_history(lead_name, limit=20):
    """
    Return communication history for a lead.
    Requires approved personalisation role.
    Returns masked recipient only — never raw phone/email.
    """
    _require_personalisation_access()
    lead_name = sanitise_demo_text(str(lead_name or ""), 50)
    if not lead_name:
        frappe.throw("lead_name is required.")
    try:
        limit = max(1, min(int(limit), 100))
    except (ValueError, TypeError):
        limit = 20
    logs = frappe.db.get_all(
        "SmartLife Communication Log",
        filters={"lead": lead_name},
        fields=[
            "name", "channel", "template_name", "recipient_masked",
            "message_status", "provider", "provider_reference",
            "sent_on", "failure_reason", "consent_snapshot",
            "staff_owner", "triggered_by_stage", "demo_mode",
        ],
        order_by="sent_on desc",
        limit=limit,
    )
    return {
        "success": True,
        "lead":    lead_name,
        "history": [dict(l) for l in logs],
        "count":   len(logs),
    }


@frappe.whitelist()
def get_messaging_config_status():
    """
    Return provider config status — booleans and status strings only.
    Never reveals secret values, token fragments, or credential content.
    Requires authenticated staff session.
    """
    _require_authenticated_staff()
    from nssf_smart_savers.messaging import get_messaging_provider_status
    return {
        "success": True,
        "config":  get_messaging_provider_status(),
    }
