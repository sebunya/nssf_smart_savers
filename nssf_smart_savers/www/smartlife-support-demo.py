import frappe


def get_context(context):
    context.title = "SmartLife Flexi - Support"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.demo_notice = "SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data."
    context.faqs = [
        {
            "q": "What is SmartLife Flexi?",
            "a": "SmartLife Flexi is NSSF Uganda's voluntary savings product that lets you save on your own schedule toward personal goals.",
        },
        {
            "q": "How do I join?",
            "a": "You can join as a voluntary NSSF member at any branch or online. This demo shows the onboarding experience.",
        },
        {
            "q": "What is the minimum contribution?",
            "a": "The minimum contribution is UGX 5,000 per period.",
        },
        {
            "q": "What return can I expect?",
            "a": "Projections use 10% indicative annual return. Actual returns may vary based on NSSF fund performance.",
        },
        {
            "q": "Is my money safe?",
            "a": "NSSF is a government-mandated institution regulated by Uganda's Ministry of Finance. Your savings are protected.",
        },
    ]
