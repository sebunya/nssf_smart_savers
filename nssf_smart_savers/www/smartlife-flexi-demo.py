import frappe


def get_context(context):
    context.title = "SmartLife Flexi Demo"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.segments = [
        {"key": "existing_member", "label": "Existing NSSF Member", "icon": "🏦", "description": "Already registered with NSSF"},
        {"key": "new_voluntary", "label": "New Voluntary Saver", "icon": "✨", "description": "Joining NSSF voluntarily"},
        {"key": "diaspora", "label": "Diaspora Saver", "icon": "🌍", "description": "Saving from abroad"},
        {"key": "civil_servant", "label": "Civil Servant", "icon": "🏛️", "description": "Government employee"},
        {"key": "formal_sector", "label": "Formal Sector Employee", "icon": "💼", "description": "Private sector employee"},
        {"key": "informal_sector", "label": "Informal / Self-Employed", "icon": "🛒", "description": "Business owner or freelancer"},
        {"key": "parent_guardian", "label": "Parent / Guardian", "icon": "👨‍👩‍👧", "description": "Saving for children"},
        {"key": "staff_assisted_prospect", "label": "Need Staff Help", "icon": "🤝", "description": "I'd like an advisor"},
    ]
    context.goals = [
        {"key": "marriage", "label": "Marriage", "icon": "💍"},
        {"key": "vacation", "label": "Vacation", "icon": "✈️"},
        {"key": "homeownership", "label": "Home Ownership", "icon": "🏠"},
        {"key": "school_fees", "label": "School Fees", "icon": "📚"},
        {"key": "wedding", "label": "Wedding", "icon": "💒"},
        {"key": "emergencies", "label": "Emergency Fund", "icon": "🛡️"},
        {"key": "education", "label": "Education", "icon": "🎓"},
        {"key": "avoiding_debt", "label": "Avoiding Debt", "icon": "🔒"},
        {"key": "investment", "label": "Investment", "icon": "📈"},
        {"key": "financial_security", "label": "Financial Security", "icon": "⚡"},
        {"key": "job_loss_cushion", "label": "Job Loss Cushion", "icon": "🧲"},
        {"key": "car", "label": "Car Purchase", "icon": "🚗"},
        {"key": "retirement", "label": "Retirement", "icon": "🌅"},
        {"key": "financial_independence", "label": "Financial Independence", "icon": "🦁"},
        {"key": "other", "label": "Other Goal", "icon": "⭐"},
    ]
    context.frequencies = [
        {"key": "daily", "label": "Daily"},
        {"key": "weekly", "label": "Weekly"},
        {"key": "monthly", "label": "Monthly"},
        {"key": "quarterly", "label": "Quarterly"},
        {"key": "semi-annually", "label": "Semi-Annually"},
        {"key": "annually", "label": "Annually"},
    ]
