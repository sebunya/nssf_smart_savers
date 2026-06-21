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


def build_email_payload(to_demo_ref, subject, body_html, template_name=None):
    config = get_zeptomail_config()
    return {
        'to': [{'email_address': {'address': to_demo_ref, 'name': 'Demo Recipient'}}],
        'from': {'address': config['from_address'], 'name': config['from_name']},
        'subject': subject,
        'htmlbody': body_html,
        'template': template_name,
        'mode': config['mode'],
    }


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
