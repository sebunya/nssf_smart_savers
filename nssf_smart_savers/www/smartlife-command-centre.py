import frappe

_PERSONALISATION_ROLES = {
    "SmartLife Personalisation Team",
    "NSSF Staff",
    "System Manager",
}


def get_context(context):
    context.title = "SmartLife Command Centre"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = (
        "SmartLife Flexi — Command Centre dashboard. "
        "Aggregate operational analytics."
    )
    context.is_guest = frappe.session.user == "Guest"
    context.has_personalisation_role = (
        not context.is_guest
        and bool(_PERSONALISATION_ROLES.intersection(set(frappe.get_roles())))
    )
