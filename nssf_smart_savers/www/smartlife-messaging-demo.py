"""
SmartLife Messaging Console - server context.
Access:
  Guest           -> sign-in gate
  Authenticated   -> must have approved personalisation role
  Approved role   -> full console
"""
import frappe

from nssf_smart_savers.api import _has_allowed_personalisation_role

# Module-level no_cache prevents user-specific permission pages
# from being served from website cache.
no_cache = 1


def get_context(context):
    context.title = "SmartLife Messaging Console"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.no_cache = 1
    context.demo_notice = (
        "SmartLife Flexi - Internal Messaging Console. "
        "Staff use only. Credentials are never shown here."
    )

    user = frappe.session.user
    context.is_guest = user == "Guest"
    context.current_user = user
    context.has_personalisation_role = (
        not context.is_guest
        and _has_allowed_personalisation_role(user)
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
