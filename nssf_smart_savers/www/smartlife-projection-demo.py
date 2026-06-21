import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Projection Calculator"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.projection_disclaimer = "Projection is indicative for demo purposes only. Actual returns may vary."
    context.frequencies = [
        {"key": "daily", "label": "Daily"},
        {"key": "weekly", "label": "Weekly"},
        {"key": "monthly", "label": "Monthly"},
        {"key": "quarterly", "label": "Quarterly"},
        {"key": "annually", "label": "Annually"},
    ]
    context.goals = [
        {"key": "emergencies", "label": "Emergency Fund"},
        {"key": "homeownership", "label": "Home Ownership"},
        {"key": "education", "label": "Education"},
        {"key": "retirement", "label": "Retirement"},
        {"key": "other", "label": "Other"},
    ]
