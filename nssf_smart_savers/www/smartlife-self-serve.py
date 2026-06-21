import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Start Your Plan"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.projection_disclaimer = "Projection is indicative for demo purposes only. Actual returns may vary."
    context.segments = [
        {"key": "existing_member", "label": "Existing NSSF Member", "icon": "🏦"},
        {"key": "new_voluntary", "label": "New Voluntary Saver", "icon": "✨"},
        {"key": "diaspora", "label": "Diaspora Saver", "icon": "🌍"},
        {"key": "civil_servant", "label": "Civil Servant", "icon": "🏛️"},
        {"key": "formal_sector", "label": "Formal Sector Employee", "icon": "💼"},
        {"key": "informal_sector", "label": "Informal / Self-Employed", "icon": "🛒"},
        {"key": "parent_guardian", "label": "Parent / Guardian", "icon": "👨‍👩‍👧"},
        {"key": "staff_assisted_prospect", "label": "Need Staff Help", "icon": "🤝"},
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
        {"key": "daily", "label": "Daily", "min": 5000},
        {"key": "weekly", "label": "Weekly", "min": 5000},
        {"key": "monthly", "label": "Monthly", "min": 5000},
        {"key": "quarterly", "label": "Quarterly", "min": 5000},
        {"key": "semi-annually", "label": "Semi-Annually", "min": 5000},
        {"key": "annually", "label": "Annually", "min": 5000},
    ]
    context.sources_of_income = [
        "Salary / Employment",
        "Business",
        "Agriculture",
        "Remittances",
        "Pension",
        "Investments",
        "Other",
    ]
    context.industries = [
        "Agriculture", "Banking & Finance", "Construction", "Education",
        "Energy", "Government", "Healthcare", "Hospitality", "ICT",
        "Manufacturing", "NGO / Non-Profit", "Retail & Trade", "Transport",
        "Other",
    ]
    context.countries = [
        "Uganda", "Kenya", "Tanzania", "Rwanda", "Burundi",
        "South Sudan", "DRC", "United Kingdom", "United States",
        "Canada", "Australia", "Other",
    ]
    context.api_base = "/api/method/nssf_smart_savers.api"
