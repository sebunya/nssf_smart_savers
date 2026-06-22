"""
SmartLife Messaging Console — server context.
Access:
  Guest           → sign-in gate
  Authenticated   → must have approved personalisation role
  Approved role   → full console
"""
import frappe

_PERSONALISATION_ROLES = {"SmartLife Personalisation Team", "NSSF Staff", "System Manager"}


def get_context(context):
    context.title = "SmartLife Messaging Console"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = (
        "SmartLife Flexi — Internal Messaging Console. "
        "Staff use only. Credentials are never shown here."
    )

    user = frappe.session.user
    context.is_guest = (user == "Guest")
    context.has_personalisation_role = (
        not context.is_guest
        and bool(_PERSONALISATION_ROLES.intersection(set(frappe.get_roles(user))))
    )

    if context.has_personalisation_role:
        from nssf_smart_savers.messaging import get_messaging_provider_status
        from nssf_smart_savers.communication_templates import list_templates
        try:
            context.provider_status = get_messaging_provider_status()
        except Exception:
            context.provider_status = {}
        try:
            context.templates = list_templates()
        except Exception:
            context.templates = []
    else:
        context.provider_status = {}
        context.templates = []
