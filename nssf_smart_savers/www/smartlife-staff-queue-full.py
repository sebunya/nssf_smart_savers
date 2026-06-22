import frappe


def get_context(context):
    context.title = "SmartLife Personalisation Team"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi — Internal Personalisation Team view. Full PII access enabled for authorised users."
    context.is_guest = frappe.session.user == "Guest"
