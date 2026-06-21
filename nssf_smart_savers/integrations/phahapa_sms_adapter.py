"""
SmartLife Flexi - Phahapa SMS Adapter
Demo mode: logs messages without sending.
To activate: set site_config phahapa_api_key, phahapa_sender_id, phahapa_mode=live.
"""
import frappe
import json


def get_phahapa_config():
    return {
        'mode': frappe.conf.get('phahapa_mode', 'demo'),
        'api_key': frappe.conf.get('phahapa_api_key', ''),
        'sender_id': frappe.conf.get('phahapa_sender_id', 'SmartLife'),
        'base_url': frappe.conf.get('phahapa_base_url', 'https://api.phahapa.com'),
    }


def validate_no_pii(payload):
    """Ensure SMS payload contains no real PII."""
    from nssf_smart_savers.utils.privacy import is_pii_safe
    for k, v in payload.items():
        if k in ('phone', 'recipient'):
            continue  # phone number is needed for SMS but must be demo-only
        if not is_pii_safe(str(v)):
            raise ValueError(f'SMS payload field {k} contains PII. Blocked.')
    return True


def build_sms_payload(recipient_demo_ref, message, sender_id=None, personalisation=None):
    """
    Build SMS payload. recipient_demo_ref is a demo reference, not a real phone.
    personalisation may include: age_band, gender_category, country_category,
    birthday_month, birthday_day, preferred_contact_channel, consent_to_contact.
    Raw PII (name, phone, DOB, email) must not appear in this payload.
    """
    config = get_phahapa_config()
    payload = {
        'recipient': recipient_demo_ref,
        'message': message[:160],
        'sender_id': sender_id or config['sender_id'],
        'mode': config['mode'],
    }
    if personalisation:
        # Allow only safe anonymised fields for message personalisation routing
        safe_fields = ('age_band', 'gender_category', 'country_category',
                       'birthday_month', 'birthday_day',
                       'preferred_contact_channel', 'consent_to_contact',
                       'segment', 'goal', 'savings_goal')
        payload['personalisation'] = {k: v for k, v in personalisation.items() if k in safe_fields}
    return payload


def build_birthday_sms(recipient_demo_ref, first_name_ref, birthday_month, birthday_day):
    """Build birthday reminder SMS. first_name_ref is a placeholder, not stored in payload."""
    msg = (
        "Dear SmartLife Member, wishing you a Happy Birthday from NSSF SmartLife Flexi! "
        "Your future is worth saving for. Log in today to review your plan."
    )
    return build_sms_payload(
        recipient_demo_ref, msg,
        personalisation={'birthday_month': birthday_month, 'birthday_day': birthday_day}
    )


def build_savings_reminder_sms(recipient_demo_ref, age_band, goal, frequency):
    """Build savings reminder SMS using only anonymous personalisation."""
    msg = (
        "SmartLife Flexi: Your next contribution is due. "
        "Keep your " + str(goal or "savings") + " plan on track. "
        "Log in to stay on course."
    )
    return build_sms_payload(
        recipient_demo_ref, msg,
        personalisation={'age_band': age_band, 'savings_goal': goal, 'contribution_frequency': frequency}
    )


def send_demo_sms(recipient_demo_ref, message, event_type='demo_notification'):
    """Log an SMS in demo mode. Never sends real SMS without live credentials."""
    config = get_phahapa_config()
    payload = build_sms_payload(recipient_demo_ref, message)

    if config['mode'] != 'live':
        # Log demo SMS event
        try:
            doc = frappe.get_doc({
                'doctype': 'SmartLife Demo Notification',
                'notification_type': 'SMS',
                'channel': 'Phahapa SMS',
                'event_trigger': event_type,
                'template_name': 'demo_sms',
                'rendered_body': message,
                'status': 'Simulated',
                'simulated': 1,
            })
            doc.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(str(e), 'SmartLife SMS Demo Log Error')
        return {'status': 'simulated', 'demo': True, 'payload': payload}

    raise NotImplementedError('Live SMS requires Phahapa credentials in site_config.')
