"""
SmartLife Flexi - ZeptoMail Transactional Email Adapter
Demo mode: logs emails without sending.
To activate: set site_config zeptomail_api_key, zeptomail_from_address, zeptomail_mode=live.
"""
import frappe
import json


def get_zeptomail_config():
    return {
        'mode': frappe.conf.get('zeptomail_mode', 'demo'),
        'api_key': frappe.conf.get('zeptomail_api_key', ''),
        'from_address': frappe.conf.get('zeptomail_from_address', 'noreply@demo.smartlifeflexi.com'),
        'from_name': frappe.conf.get('zeptomail_from_name', 'SmartLife Flexi Demo'),
        'base_url': 'https://api.zeptomail.com/v1.1',
    }


def validate_no_pii(payload):
    from nssf_smart_savers.utils.privacy import is_pii_safe
    for k, v in payload.items():
        if k in ('to', 'to_address', 'recipient'):
            continue
        if not is_pii_safe(str(v)):
            raise ValueError(f'Email payload field {k} contains PII. Blocked.')
    return True


def build_email_payload(to_demo_ref, subject, body_html, template_name=None, personalisation=None):
    """
    Build ZeptoMail email payload.
    personalisation may include: age_band, gender_category, country_category,
    birthday_month, birthday_day, preferred_contact_channel, consent_to_contact, segment, goal.
    Raw PII (name, email, DOB, phone) must be handled server-side and must NOT appear
    in template merge fields sent to ZeptoMail unless using secure server-side rendering.
    """
    config = get_zeptomail_config()
    payload = {
        'to': [{'email_address': {'address': to_demo_ref, 'name': 'SmartLife Member'}}],
        'from': {'address': config['from_address'], 'name': config['from_name']},
        'subject': subject,
        'htmlbody': body_html,
        'template': template_name,
        'mode': config['mode'],
    }
    if personalisation:
        safe_fields = ('age_band', 'gender_category', 'country_category',
                       'birthday_month', 'birthday_day',
                       'preferred_contact_channel', 'consent_to_contact',
                       'segment', 'goal', 'savings_goal')
        payload['merge_info'] = {k: v for k, v in personalisation.items() if k in safe_fields}
    return payload


def build_birthday_email(to_demo_ref, birthday_month, birthday_day, age_band):
    """Birthday email with anonymous personalisation only."""
    subject = "Happy Birthday from NSSF SmartLife Flexi!"
    body    = (
        "<p>Dear SmartLife Member,</p>"
        "<p>Wishing you a wonderful birthday from the NSSF SmartLife Flexi team!</p>"
        "<p>Your savings journey continues — log in today to check your progress and stay on track.</p>"
        "<p><strong>NSSF SmartLife Flexi</strong></p>"
    )
    return build_email_payload(
        to_demo_ref, subject, body,
        template_name='smartlife_birthday',
        personalisation={'birthday_month': birthday_month, 'birthday_day': birthday_day, 'age_band': age_band}
    )


def build_onboarding_email(to_demo_ref, segment, goal, age_band):
    """Onboarding confirmation email with anonymous personalisation."""
    subject = "Welcome to NSSF SmartLife Flexi!"
    body    = (
        "<p>Dear SmartLife Member,</p>"
        "<p>Thank you for starting your savings journey with NSSF SmartLife Flexi.</p>"
        "<p>Your personalised savings plan is ready. Log in to review your plan and start saving.</p>"
        "<p><strong>NSSF SmartLife Flexi</strong></p>"
    )
    return build_email_payload(
        to_demo_ref, subject, body,
        template_name='smartlife_onboarding',
        personalisation={'segment': segment, 'savings_goal': goal, 'age_band': age_band}
    )


def build_savings_reminder_email(to_demo_ref, goal, frequency, age_band):
    """Savings reminder email using only anonymous personalisation."""
    subject = "SmartLife Flexi: Your savings reminder"
    body    = (
        "<p>Dear SmartLife Member,</p>"
        "<p>Your " + str(goal or "savings") + " plan contribution is due soon.</p>"
        "<p>Log in to SmartLife Flexi to make your " + str(frequency or "scheduled") + " contribution and stay on track.</p>"
        "<p><strong>NSSF SmartLife Flexi</strong></p>"
    )
    return build_email_payload(
        to_demo_ref, subject, body,
        template_name='smartlife_savings_reminder',
        personalisation={'savings_goal': goal, 'contribution_frequency': frequency, 'age_band': age_band}
    )


def send_demo_email(to_demo_ref, subject, body_html, event_type='demo_email', template_name=None):
    config = get_zeptomail_config()
    payload = build_email_payload(to_demo_ref, subject, body_html, template_name)

    if config['mode'] != 'live':
        try:
            doc = frappe.get_doc({
                'doctype': 'SmartLife Demo Notification',
                'notification_type': 'Email',
                'channel': 'ZeptoMail Email',
                'event_trigger': event_type,
                'template_name': template_name or 'demo_email',
                'rendered_body': body_html[:500],
                'status': 'Simulated',
                'simulated': 1,
            })
            doc.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(str(e), 'SmartLife Email Demo Log Error')
        return {'status': 'simulated', 'demo': True}

    raise NotImplementedError('Live email requires ZeptoMail credentials in site_config.')
