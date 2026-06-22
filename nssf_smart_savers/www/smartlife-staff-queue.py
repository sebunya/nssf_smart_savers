import frappe


def get_context(context):
    context.title = "SmartLife Staff Queue"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi — Staff Demo Queue. Prototype environment. No real member data."
