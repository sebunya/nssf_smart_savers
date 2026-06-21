import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Staff Assist"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.segments = [
        {"key": "existing_member", "label": "Existing NSSF Member"},
        {"key": "new_voluntary", "label": "New Voluntary Saver"},
        {"key": "diaspora", "label": "Diaspora Saver"},
        {"key": "civil_servant", "label": "Civil Servant"},
        {"key": "formal_sector", "label": "Formal Sector Employee"},
        {"key": "informal_sector", "label": "Informal / Self-Employed"},
        {"key": "parent_guardian", "label": "Parent / Guardian"},
        {"key": "staff_assisted_prospect", "label": "Unknown / General"},
    ]
    context.goals = [
        {"key": "marriage", "label": "Marriage"},
        {"key": "vacation", "label": "Vacation"},
        {"key": "homeownership", "label": "Home Ownership"},
        {"key": "school_fees", "label": "School Fees"},
        {"key": "wedding", "label": "Wedding"},
        {"key": "emergencies", "label": "Emergency Fund"},
        {"key": "education", "label": "Education"},
        {"key": "avoiding_debt", "label": "Avoiding Debt"},
        {"key": "investment", "label": "Investment"},
        {"key": "financial_security", "label": "Financial Security"},
        {"key": "job_loss_cushion", "label": "Job Loss Cushion"},
        {"key": "car", "label": "Car Purchase"},
        {"key": "retirement", "label": "Retirement"},
        {"key": "financial_independence", "label": "Financial Independence"},
        {"key": "other", "label": "Other Goal"},
    ]
    context.objections = [
        {"key": "not_enough_money", "label": "Not enough money"},
        {"key": "dont_understand", "label": "Don't understand the product"},
        {"key": "save_elsewhere", "label": "Already save elsewhere"},
        {"key": "worried_lock_in", "label": "Worried about lock-in"},
        {"key": "not_nssf_member", "label": "Not an NSSF member"},
        {"key": "distrust_digital", "label": "Distrust digital platforms"},
        {"key": "need_family_approval", "label": "Needs family approval"},
        {"key": "need_payment_help", "label": "Needs payment help"},
        {"key": "not_ready", "label": "Not ready yet"},
    ]
    context.follow_up_channels = ["Phone", "WhatsApp", "Email", "Walk-in", "None"]
