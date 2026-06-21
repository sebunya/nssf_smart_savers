import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Start Your Plan"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.projection_disclaimer = "Projection is indicative for demo purposes only. Actual returns may vary."

    # 5 saver types - no ZWJ emoji (root cause fix)
    context.saver_types = [
        {"key": "existing_member", "label": "Existing NSSF Member", "icon": "🏦"},
        {"key": "new_voluntary", "label": "New Saver / Non-Member", "icon": "✨"},
        {"key": "diaspora", "label": "Diaspora Saver", "icon": "🌍"},
        {"key": "informal_sector", "label": "Informal Sector Saver", "icon": "🛒"},
        {"key": "staff_assisted_prospect", "label": "Staff-Assisted Prospect", "icon": "🤝"},
    ]

    context.saver_type_descriptions = {
        "existing_member": "I already have an NSSF account and want to add voluntary SmartLife savings.",
        "new_voluntary": "I do not currently save with NSSF but want to start building a savings habit.",
        "diaspora": "I live outside Uganda and want to save consistently towards a goal back home.",
        "informal_sector": "My income is flexible or irregular, so I need a plan that fits how I earn.",
        "staff_assisted_prospect": "I am being guided by staff or registering through an assisted session.",
    }

    # 10 goals
    context.goals = [
        {"key": "education", "label": "Education", "icon": "🎓"},
        {"key": "homeownership", "label": "Home Ownership", "icon": "🏠"},
        {"key": "land", "label": "Land Purchase", "icon": "🌱"},
        {"key": "car", "label": "Car Purchase", "icon": "🚗"},
        {"key": "business_capital", "label": "Business Capital", "icon": "📈"},
        {"key": "emergencies", "label": "Emergency Fund", "icon": "🛡️"},
        {"key": "wedding", "label": "Wedding / Marriage", "icon": "💍"},
        {"key": "retirement", "label": "Retirement", "icon": "🌅"},
        {"key": "financial_independence", "label": "Financial Independence", "icon": "🦁"},
        {"key": "other", "label": "Other Goal", "icon": "⭐"},
    ]

    # 6 frequencies (includes semi-annually)
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
        "Business / Self-employed",
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
