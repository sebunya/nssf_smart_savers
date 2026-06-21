"""
SmartLife Flexi - Rule-based Personalisation Engine
Demo environment only
"""

SEGMENT_PROFILES = {
    "existing_member": {
        "label": "Existing NSSF Member",
        "hero": "You already trust NSSF. SmartLife Flexi lets you save more, your way.",
        "cta_color": "#1a5c38",
        "recommended_frequency": "monthly",
        "rhythm": "Align with your salary date for effortless saving.",
    },
    "new_voluntary": {
        "label": "New Saver / Non-Member",
        "hero": "Start your savings journey today — no employer required.",
        "cta_color": "#1a5c38",
        "recommended_frequency": "weekly",
        "rhythm": "Weekly contributions build powerful habits.",
    },
    "diaspora": {
        "label": "Diaspora Saver",
        "hero": "Invest in Uganda's future — and your own — from anywhere in the world.",
        "cta_color": "#c9a227",
        "recommended_frequency": "monthly",
        "rhythm": "Monthly transfers align with international pay cycles.",
    },
    "informal_sector": {
        "label": "Informal Sector Saver",
        "hero": "No salary? No problem. Save on your own schedule with SmartLife Flexi.",
        "cta_color": "#c9a227",
        "recommended_frequency": "weekly",
        "rhythm": "Save when business is good — weekly or daily.",
    },
    "staff_assisted_prospect": {
        "label": "Staff-Assisted Prospect",
        "hero": "Our SmartLife advisor is here to build your personalised plan.",
        "cta_color": "#1a5c38",
        "recommended_frequency": "monthly",
        "rhythm": "Your advisor will help you choose the best rhythm.",
    },
}

GOAL_MESSAGES = {
    "education": {"label": "Education", "copy": "Invest in knowledge — the return is always worth it.", "icon": "🎓"},
    "homeownership": {"label": "Home Ownership", "copy": "Every contribution brings you closer to the keys of your own home.", "icon": "🏠"},
    "land": {"label": "Land Purchase", "copy": "Own your own land — a foundation for everything else.", "icon": "🌱"},
    "car": {"label": "Car Purchase", "copy": "Drive your dream vehicle — funded by your own savings.", "icon": "🚗"},
    "business_capital": {"label": "Business Capital", "copy": "Grow your business with a dedicated savings fund.", "icon": "📈"},
    "emergencies": {"label": "Emergency Fund", "copy": "Life is unpredictable. Your SmartLife fund is always ready.", "icon": "🛡️"},
    "wedding": {"label": "Wedding / Marriage", "copy": "Celebrate love without financial stress — start saving now.", "icon": "💍"},
    "retirement": {"label": "Retirement", "copy": "Retire with dignity. Every shilling saved today is freedom tomorrow.", "icon": "🌅"},
    "financial_independence": {"label": "Financial Independence", "copy": "Your money working for you — that's true independence.", "icon": "🦁"},
    "other": {"label": "Other Goal", "copy": "Whatever your goal, SmartLife Flexi helps you get there.", "icon": "⭐"},
}

OBJECTION_SCRIPTS = {
    "not_enough_money": {
        "response": "SmartLife Flexi starts from as little as UGX 5,000. Even small, regular contributions grow significantly over time. Would you like to see a projection?",
        "staff_script": "Acknowledge the concern empathetically. Show a projection starting at UGX 5,000/week. Highlight that daily saving of less than a cup of coffee adds up to over UGX 1.8M per year.",
    },
    "dont_understand": {
        "response": "SmartLife Flexi is a voluntary savings plan — you choose your amount and frequency. You can access funds after your chosen period. Let me walk you through a quick example.",
        "staff_script": "Use the projection tool together. Walk through the 3-step setup. Offer a printed plan summary.",
    },
    "save_elsewhere": {
        "response": "SmartLife Flexi complements other savings — it's specifically designed for long-term goals with NSSF's trusted oversight. Compare your current returns with our indicative projection.",
        "staff_script": "Ask where they currently save and what rate they earn. Show how NSSF's 10% indicative return compares. Emphasise NSSF credibility and government backing.",
    },
    "worried_lock_in": {
        "response": "Your plan has a target period you choose. You can adjust contributions and access funds per the plan terms. You remain in control.",
        "staff_script": "Clarify the access terms for SmartLife Flexi. Explain the difference between target period and hard lock-in. Show the flexibility of contribution amounts.",
    },
    "not_nssf_member": {
        "response": "You can join NSSF as a voluntary member right now — it takes minutes. Once registered, SmartLife Flexi is immediately available to you.",
        "staff_script": "Offer to walk through voluntary registration. Have the registration form ready. Explain that voluntary members have full access to SmartLife Flexi.",
    },
    "distrust_digital": {
        "response": "We support in-person sign-up at any NSSF branch with staff assistance. Your data is protected under Uganda's data protection framework.",
        "staff_script": "Offer branch-based onboarding. Explain security measures. Provide printed materials. Offer to be their named support contact.",
    },
    "need_family_approval": {
        "response": "That's responsible planning. Would you like a printed plan summary to share with your family? We can also schedule a joint session.",
        "staff_script": "Offer a family consultation session. Provide printed plan summary. Schedule a follow-up after their family discussion.",
    },
    "need_payment_help": {
        "response": "We support Mobile Money (MTN, Airtel), bank transfer, and employer deduction. Our team can help you set up the easiest method for you.",
        "staff_script": "Walk through all payment options. Help set up Mobile Money standing order if appropriate. Offer employer deduction letter if they are employed.",
    },
    "not_ready": {
        "response": "No pressure. Let me save your plan and send you a reminder when you're ready. It takes just 2 minutes to start when you decide.",
        "staff_script": "Save the session notes and prospect details. Set a follow-up task for 7 days. Send a plan summary to their preferred channel.",
    },
}

CTA_COLORS = {
    "existing_member": "#1a5c38",
    "new_voluntary": "#1a5c38",
    "diaspora": "#c9a227",
    "informal_sector": "#c9a227",
    "staff_assisted_prospect": "#1a5c38",
}


def get_personalised_plan(
    segment,
    goal,
    target_amount,
    years,
    frequency,
    initial_deposit,
    source_of_income="",
    industry="",
    country="Uganda",
    staff_assisted=False,
    objection=None,
):
    """
    Generate a personalised savings plan based on segment and goal.
    Returns dict with copy, recommendations, and analytics labels.
    Demo environment only.
    """
    segment_data = SEGMENT_PROFILES.get(segment, SEGMENT_PROFILES["new_voluntary"])
    goal_data = GOAL_MESSAGES.get(goal, GOAL_MESSAGES["other"])

    hero_copy = segment_data["hero"]
    goal_copy = goal_data["copy"]
    recommended_frequency = segment_data["recommended_frequency"]
    recommended_rhythm = segment_data["rhythm"]
    cta_color = CTA_COLORS.get(segment, "#1a5c38")

    if staff_assisted:
        next_best_action = "Log session and schedule follow-up"
        cta_label = "Save Session & Generate Script"
    elif float(initial_deposit or 0) >= 50000:
        next_best_action = "Proceed to checkout and simulate your first payment"
        cta_label = "Start Saving Today"
    else:
        next_best_action = "Review your projection and adjust your plan"
        cta_label = "See My Projection"

    staff_script = ""
    if staff_assisted:
        staff_script = (
            "STAFF GUIDE — {segment_label} | Goal: {goal_label}\n\n"
            "Opening: \"{hero}\"\n\n"
            "Goal framing: \"{goal_copy}\"\n\n"
            "Recommended savings rhythm: {rhythm}\n\n"
            "Suggested frequency: {freq}\n\n"
            "Target: UGX {target:,.0f} over {years} year(s).\n\n"
            "Next steps:\n"
            "1. Confirm the goal and target amount\n"
            "2. Run the live projection together\n"
            "3. Select payment method\n"
            "4. Complete registration or log follow-up\n\n"
            "DEMO ENVIRONMENT — Do not enter real member data."
        ).format(
            segment_label=segment_data["label"],
            goal_label=goal_data["label"],
            hero=hero_copy,
            goal_copy=goal_copy,
            rhythm=recommended_rhythm,
            freq=recommended_frequency.title(),
            target=float(target_amount or 0),
            years=years,
        )

    objection_response = ""
    if objection and objection in OBJECTION_SCRIPTS:
        objection_data = OBJECTION_SCRIPTS[objection]
        if staff_assisted:
            objection_response = objection_data["staff_script"]
        else:
            objection_response = objection_data["response"]

    country_lower = str(country).lower()
    if country_lower in ("uganda", "ug"):
        country_band = "uganda"
    elif country_lower in ("kenya", "tanzania", "rwanda", "burundi", "south sudan", "drc"):
        country_band = "east_africa"
    else:
        country_band = "diaspora"

    analytics_labels = {
        "segment": segment,
        "goal_category": goal,
        "frequency": frequency,
        "staff_assisted": "yes" if staff_assisted else "no",
        "country_band": country_band,
        "source_category": str(source_of_income)[:50] if source_of_income else "unknown",
        "industry_category": str(industry)[:50] if industry else "unknown",
    }

    return {
        "hero_copy": hero_copy,
        "goal_copy": goal_copy,
        "recommended_frequency": recommended_frequency,
        "recommended_rhythm": recommended_rhythm,
        "next_best_action": next_best_action,
        "staff_script": staff_script,
        "objection_response": objection_response,
        "cta_label": cta_label,
        "cta_color": cta_color,
        "segment_label": segment_data["label"],
        "goal_label": goal_data["label"],
        "analytics_labels": analytics_labels,
        "demo_notice": "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data.",
    }
