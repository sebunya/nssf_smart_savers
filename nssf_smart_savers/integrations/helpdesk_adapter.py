"""
SmartLife Flexi - Helpdesk Adapter
Creates demo support tickets via Frappe Helpdesk.
Helpdesk is already installed on the site.
"""
import frappe


def prepare_ticket_payload(subject, description, demo_context=None):
    """Prepare a Helpdesk ticket payload."""
    safe_subject = 'SmartLife Demo: ' + str(subject or 'Support Request')[:100]
    safe_desc = str(description or '')[:500]
    if demo_context:
        safe_desc += '\n\n--- Demo Context ---\n'
        safe_desc += 'Journey: ' + str(demo_context.get('journey_type', '')) + '\n'
        safe_desc += 'Segment: ' + str(demo_context.get('segment', '')) + '\n'
        safe_desc += 'Goal: ' + str(demo_context.get('goal', '')) + '\n'
        safe_desc += '\n[Demo environment — no real member data]'
    return {
        'subject': safe_subject,
        'description': safe_desc,
        'raised_by': 'demo@smartlifeflexi.nile-gov-demo.com',
        'priority': 'Medium',
        'type': 'SmartLife Demo',
    }


def create_demo_support_ticket(subject, description=None, demo_context=None):
    """Create a Helpdesk ticket. Falls back to Demo Notification if Helpdesk unavailable."""
    payload = prepare_ticket_payload(subject, description, demo_context)

    try:
        # Try Frappe Helpdesk
        ticket = frappe.get_doc(dict(
            doctype='HD Ticket',
            subject=payload['subject'],
            description=payload['description'],
            raised_by=payload['raised_by'],
            priority=payload['priority'],
        ))
        ticket.insert(ignore_permissions=True)
        return {'success': True, 'ticket_name': ticket.name, 'via': 'helpdesk'}
    except Exception:
        # Fall back to Demo Notification log
        try:
            note = frappe.get_doc({
                'doctype': 'SmartLife Demo Notification',
                'notification_type': 'Email',
                'channel': 'Demo Log',
                'event_trigger': 'support_request',
                'template_name': 'support_fallback',
                'rendered_body': payload['subject'] + '\n' + payload['description'],
                'status': 'Simulated',
                'simulated': 1,
            })
            note.insert(ignore_permissions=True)
            return {'success': True, 'ticket_name': note.name, 'via': 'demo_log'}
        except Exception as e2:
            frappe.log_error(str(e2), 'SmartLife Helpdesk Adapter Error')
            return {'success': False, 'error': str(e2)}
