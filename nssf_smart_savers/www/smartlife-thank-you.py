import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Thank You"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. No real account created. No real contribution made."
