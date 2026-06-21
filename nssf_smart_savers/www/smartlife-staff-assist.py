import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Staff Assist"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
