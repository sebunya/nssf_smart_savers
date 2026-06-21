"""
SmartLife Flexi - CRM Adapter
Maps Demo Lead records to Frappe CRM Lead/Deal format.
To activate Frappe CRM integration: install frappe/crm and set crm_enabled=1 in site_config.
"""
import frappe


def is_crm_available():
    try:
        frappe.get_doc({'doctype': 'CRM Lead'})
        return True
    except Exception:
        return False


def map_demo_lead_to_crm_lead(demo_lead_name):
    """
    Convert a SmartLife Demo Lead to a Frappe CRM Lead payload.
    Uses anonymous fields only — no real name, phone, email, DOB, or exact age in CRM.
    For birthday/lifecycle automation, only birthday_month and birthday_day are passed.
    """
    lead = frappe.get_doc('SmartLife Demo Lead', demo_lead_name)
    return {
        'doctype': 'CRM Lead',
        'first_name': 'SmartLife Demo',
        'last_name': lead.segment or 'Prospect',
        'source': 'SmartLife Flexi Demo',
        'lead_owner': lead.staff_assisted and 'Staff Assist' or 'Self-Serve',
        'custom_journey_type':       lead.journey_type,
        'custom_savings_goal':       lead.goal,
        'custom_frequency':          lead.frequency,
        'custom_saver_segment':      lead.segment,
        'custom_lead_stage':         lead.lead_stage or 'New',
        'custom_demo_lead_ref':      lead.name,
        'custom_analytics_labels':   lead.analytics_labels,
        'custom_age_band':           getattr(lead, 'age_band', ''),
        'custom_gender_category':    'undisclosed' if getattr(lead, 'gender', '') == 'prefer_not_to_say' else getattr(lead, 'gender', ''),
        'custom_country_category':   'local' if str(getattr(lead, 'country', '')).lower() == 'uganda' else 'international',
        'custom_birthday_month':     getattr(lead, 'birthday_month', None),
        'custom_birthday_day':       getattr(lead, 'birthday_day', None),
        'custom_preferred_channel':  getattr(lead, 'preferred_contact_channel', ''),
        'custom_consent_to_contact': getattr(lead, 'consent_to_contact', 0),
        'no_of_employees': '1',
        'mobile_no': '',   # Never populate real phone
        'email_id':  '',   # Never populate real email
    }


def map_demo_lead_to_crm_deal(demo_lead_name):
    """Map demo lead to CRM Deal/Opportunity payload."""
    lead = frappe.get_doc('SmartLife Demo Lead', demo_lead_name)
    return {
        'doctype': 'CRM Deal',
        'lead_name': 'SmartLife Demo - ' + lead.segment,
        'status': 'Open',
        'source': 'SmartLife Flexi Demo',
        'custom_goal': lead.goal,
        'custom_frequency': lead.frequency,
        'custom_target_amount': lead.target_amount,
        'custom_demo_lead': lead.name,
        'custom_journey_type': lead.journey_type,
    }


def prepare_crm_payload(demo_lead_name, payload_type='lead'):
    """Return CRM payload without creating the record."""
    if payload_type == 'deal':
        return map_demo_lead_to_crm_deal(demo_lead_name)
    return map_demo_lead_to_crm_lead(demo_lead_name)
