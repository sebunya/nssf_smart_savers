"""
SmartLife Flexi - UAT Demo Seed Data Module
Fictional personas and event logs for visual validation, dashboard previews, and walkthrough scenarios.
Strictly UAT/demo-only. Never auto-run in production.
"""
import frappe
from datetime import datetime, timedelta

SCENARIOS = [
    {
        "id": "DEMO-SMARTLIFE-001",
        "first_name": "Demo Saver",
        "last_name": "001",
        "gender": "Female",
        "segment": "Salaried",
        "goal": "Education",
        "goal_label": "Children's University Fund",
        "target_amount": 15000000.0,
        "years": 10,
        "frequency": "Monthly",
        "initial_deposit": 250000.0,
        "source_of_income": "Salary",
        "industry": "Education",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 1,
        "lead_stage": "Onboarded",
        "lead_status": "Payment Completed",
        "lead_temperature": "Hot",
        "lead_score": 90,
        "next_best_action": "Schedule nursery check-in at Day 30",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Email",
        "email_address": "demo.saver001@example.test",
        "primary_phone": "+256700000001",
        "projection_viewed": 1,
        "checkout_started": 1,
        "payment_completed": 1,
        "staff_notes": "Board demo success case. Voluntary savings onboarding completed fully and first deposit received via simulated mobile money.",
        "intent": {
            "amount": 250000.0,
            "frequency": "Monthly",
            "method": "Mobile Money",
            "status": "Completed",
            "reference": "DEMO-PAY-001",
            "tracking_id": "PPL-TRK-001",
            "merchant_ref": "DEMO-MERCH-001"
        },
        "comms": [
            {
                "channel": "Email",
                "template": "welcome_after_personal_details",
                "status": "Sent",
                "recipient": "d***1@example.test"
            }
        ]
    },
    {
        "id": "DEMO-SMARTLIFE-002",
        "first_name": "Demo Saver",
        "last_name": "002",
        "gender": "Male",
        "segment": "Salaried",
        "goal": "Retirement",
        "goal_label": "Supplementary Retirement Fund",
        "target_amount": 50000000.0,
        "years": 20,
        "frequency": "Monthly",
        "initial_deposit": 500000.0,
        "source_of_income": "Salary",
        "industry": "Financial Services",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Checkout Started",
        "lead_status": "Payment Pending",
        "lead_temperature": "Hot",
        "lead_score": 75,
        "next_best_action": "Send checkout-abandoned reminder SMS",
        "consent_to_contact": 1,
        "preferred_contact_channel": "SMS",
        "email_address": "demo.saver002@example.test",
        "primary_phone": "+256700000002",
        "projection_viewed": 1,
        "checkout_started": 1,
        "payment_completed": 0,
        "staff_notes": "Payment recovery scenario. Cart abandoned at checkout. Auto-reminders scheduled.",
        "intent": {
            "amount": 500000.0,
            "frequency": "Monthly",
            "method": "Mobile Money",
            "status": "Pending",
            "reference": "DEMO-PAY-002",
            "tracking_id": "PPL-TRK-002",
            "merchant_ref": "DEMO-MERCH-002"
        },
        "comms": [
            {
                "channel": "SMS",
                "template": "checkout_abandoned_reminder",
                "status": "Sent",
                "recipient": "+25670******02"
            }
        ]
    },
    {
        "id": "DEMO-SMARTLIFE-003",
        "first_name": "Demo Saver",
        "last_name": "003",
        "gender": "Female",
        "segment": "Diaspora",
        "goal": "Land",
        "goal_label": "Kampala Property Purchase Fund",
        "target_amount": 80000000.0,
        "years": 5,
        "frequency": "Quarterly",
        "initial_deposit": 2000000.0,
        "source_of_income": "Salary",
        "industry": "Healthcare",
        "country": "United Kingdom",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 1,
        "lead_stage": "Onboarded",
        "lead_status": "Payment Completed",
        "lead_temperature": "Hot",
        "lead_score": 95,
        "next_best_action": "Confirm receipt of international card payment",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Email",
        "email_address": "demo.saver003@example.test",
        "primary_phone": "+447000000003",
        "projection_viewed": 1,
        "checkout_started": 1,
        "payment_completed": 1,
        "staff_notes": "Diaspora segment scenario. International card payment processed. Support query submitted and resolved.",
        "intent": {
            "amount": 2000000.0,
            "frequency": "Quarterly",
            "method": "Card",
            "status": "Completed",
            "reference": "DEMO-PAY-003",
            "tracking_id": "PPL-TRK-003",
            "merchant_ref": "DEMO-MERCH-003"
        },
        "comms": [
            {
                "channel": "Email",
                "template": "welcome_after_personal_details",
                "status": "Sent",
                "recipient": "d***3@example.test"
            }
        ],
        "support": {
            "category": "I am in the diaspora",
            "message": "Can I set up standing instructions from my UK card?",
            "status": "Resolved",
            "resolution_notes": "Informed user that card tokenisation and recurring billing is pending Phase 8 production approval."
        }
    },
    {
        "id": "DEMO-SMARTLIFE-004",
        "first_name": "Demo Saver",
        "last_name": "004",
        "gender": "Male",
        "segment": "Informal",
        "goal": "Business",
        "goal_label": "Agricultural Shop Capital",
        "target_amount": 5000000.0,
        "years": 3,
        "frequency": "Weekly",
        "initial_deposit": 50000.0,
        "source_of_income": "Business",
        "industry": "Agriculture",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 0,
        "payment_simulated": 0,
        "lead_stage": "Profile Incomplete",
        "lead_status": "New",
        "lead_temperature": "Cold",
        "lead_score": 10,
        "next_best_action": "Follow up via SMS for profile completion",
        "consent_to_contact": 1,
        "preferred_contact_channel": "SMS",
        "email_address": "demo.saver004@example.test",
        "primary_phone": "+256700000004",
        "projection_viewed": 0,
        "checkout_started": 0,
        "payment_completed": 0,
        "staff_notes": "Onboarding drop-off scenario. Lead stopped at step 1. SMS follow-up sent.",
        "comms": [
            {
                "channel": "SMS",
                "template": "consent_missing_education",
                "status": "Sent",
                "recipient": "+25670******04"
            }
        ]
    },
    {
        "id": "DEMO-SMARTLIFE-005",
        "first_name": "Demo Saver",
        "last_name": "005",
        "gender": "Female",
        "segment": "Salaried",
        "goal": "Retirement",
        "goal_label": "Extra Voluntary Pension",
        "target_amount": 30000000.0,
        "years": 15,
        "frequency": "Monthly",
        "initial_deposit": 150000.0,
        "source_of_income": "Salary",
        "industry": "Government",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Projection Viewed",
        "lead_status": "Projection Viewed",
        "lead_temperature": "Warm",
        "lead_score": 50,
        "next_best_action": "Offer call via staff console to answer questions",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Email",
        "email_address": "demo.saver005@example.test",
        "primary_phone": "+256700000005",
        "projection_viewed": 1,
        "checkout_started": 0,
        "payment_completed": 0,
        "staff_notes": "Projection-to-checkout leakage scenario. Calculated projection but did not press 'Proceed to Checkout'. Warm lead.",
        "comms": [
            {
                "channel": "Email",
                "template": "projection_viewed_reminder",
                "status": "Sent",
                "recipient": "d***5@example.test"
            }
        ]
    },
    {
        "id": "DEMO-SMARTLIFE-006",
        "first_name": "Demo Saver",
        "last_name": "006",
        "gender": "Male",
        "segment": "Informal",
        "goal": "Education",
        "goal_label": "Secondary School Fees",
        "target_amount": 10000000.0,
        "years": 6,
        "frequency": "Monthly",
        "initial_deposit": 200000.0,
        "source_of_income": "Business",
        "industry": "Retail",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Checkout Started",
        "lead_status": "Checkout Started",
        "lead_temperature": "Hot",
        "lead_score": 60,
        "next_best_action": "Support agent to call and verify mobile money status",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Phone call",
        "email_address": "demo.saver006@example.test",
        "primary_phone": "+256700000006",
        "projection_viewed": 1,
        "checkout_started": 1,
        "payment_completed": 0,
        "staff_notes": "Payment and support friction scenario. Mobile money payment failed due to network timeout. Support request created.",
        "intent": {
            "amount": 200000.0,
            "frequency": "Monthly",
            "method": "Mobile Money",
            "status": "Failed",
            "reference": "DEMO-PAY-006",
            "tracking_id": "PPL-TRK-006",
            "merchant_ref": "DEMO-MERCH-006",
            "failure_reason": "Insufficient balance / user cancelled prompt"
        },
        "comms": [
            {
                "channel": "SMS",
                "template": "checkout_abandoned_reminder",
                "status": "Sent",
                "recipient": "+25670******06"
            }
        ],
        "support": {
            "category": "I need help making a contribution",
            "message": "My Mobile Money prompt popped up but timed out before I could enter my PIN.",
            "status": "In Progress"
        }
    },
    {
        "id": "DEMO-SMARTLIFE-007",
        "first_name": "Demo Saver",
        "last_name": "007",
        "gender": "Female",
        "segment": "Informal",
        "goal": "Land",
        "goal_label": "Family Plot Fund",
        "target_amount": 12000000.0,
        "years": 4,
        "frequency": "Monthly",
        "initial_deposit": 300000.0,
        "source_of_income": "Business",
        "industry": "Hospitality",
        "country": "Uganda",
        "staff_assisted": 1,
        "journey_type": "staff-assisted",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Goal Selected",
        "lead_status": "Staff Follow-up Required",
        "lead_temperature": "Warm",
        "lead_score": 40,
        "next_best_action": "Call lead to assist with mobile checkout",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Phone call",
        "email_address": "demo.saver007@example.test",
        "primary_phone": "+256700000007",
        "projection_viewed": 1,
        "checkout_started": 0,
        "payment_completed": 0,
        "staff_notes": "Staff-assisted scenario. Guided via telephone, projection computed. Awaiting follow-up call to complete setup.",
        "comms": [
            {
                "channel": "SMS",
                "template": "staff_follow_up_message",
                "status": "Sent",
                "recipient": "+25670******07"
            }
        ],
        "support": {
            "category": "I want staff to call me",
            "message": "Assisted session requested to clarify the monthly payment options.",
            "status": "Assigned",
            "assigned_staff": "NSSF Advisor"
        }
    },
    {
        "id": "DEMO-SMARTLIFE-008",
        "first_name": "Demo Saver",
        "last_name": "008",
        "gender": "Male",
        "segment": "Salaried",
        "goal": "Retirement",
        "goal_label": "Additional NSSF Savings",
        "target_amount": 40000000.0,
        "years": 12,
        "frequency": "Monthly",
        "initial_deposit": 400000.0,
        "source_of_income": "Salary",
        "industry": "Manufacturing",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Onboarded",
        "lead_status": "Contacted",
        "lead_temperature": "Warm",
        "lead_score": 45,
        "next_best_action": "Explain voluntary top-ups vs standard 15% contribution",
        "consent_to_contact": 1,
        "preferred_contact_channel": "Email",
        "email_address": "demo.saver008@example.test",
        "primary_phone": "+256700000008",
        "projection_viewed": 1,
        "checkout_started": 0,
        "payment_completed": 0,
        "staff_notes": "Product comprehension friction scenario. Saver already has a standard NSSF number, wants to confirm if SmartLife Flexi is separate.",
        "comms": [
            {
                "channel": "Email",
                "template": "welcome_after_personal_details",
                "status": "Sent",
                "recipient": "d***8@example.test"
            }
        ],
        "support": {
            "category": "I am already an NSSF member",
            "message": "I already save with my employer. How do I link this new voluntary account to my current number?",
            "status": "New"
        }
    },
    {
        "id": "DEMO-SMARTLIFE-009",
        "first_name": "Demo Saver",
        "last_name": "009",
        "gender": "Female",
        "segment": "Salaried",
        "goal": "Education",
        "goal_label": "Daughter's College Fund",
        "target_amount": 20000000.0,
        "years": 8,
        "frequency": "Monthly",
        "initial_deposit": 300000.0,
        "source_of_income": "Salary",
        "industry": "Technology",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Onboarded",
        "lead_status": "Contacted",
        "lead_temperature": "Cold",
        "lead_score": 0,
        "next_best_action": "None - marketing consent denied",
        "consent_to_contact": 0,
        "preferred_contact_channel": "SMS",
        "email_address": "demo.saver009@example.test",
        "primary_phone": "+256700000009",
        "projection_viewed": 1,
        "checkout_started": 0,
        "payment_completed": 0,
        "staff_notes": "Marketing consent suppression scenario. Consent is denied; no auto-messages allowed. Score forced to 0.",
        "comms": [
            {
                "channel": "SMS",
                "template": "welcome_after_personal_details",
                "status": "Skipped - No Consent",
                "recipient": "+25670******09"
            }
        ]
    },
    {
        "id": "DEMO-SMARTLIFE-010",
        "first_name": "Demo Saver",
        "last_name": "010",
        "gender": "Female",
        "segment": "Informal",
        "goal": "Business",
        "goal_label": "Poultry Expansion Fund",
        "target_amount": 8000000.0,
        "years": 2,
        "frequency": "Weekly",
        "initial_deposit": 100000.0,
        "source_of_income": "Business",
        "industry": "Agriculture",
        "country": "Uganda",
        "staff_assisted": 0,
        "journey_type": "self-serve",
        "plan_generated": 1,
        "payment_simulated": 0,
        "lead_stage": "Onboarded",
        "lead_status": "Dormant",
        "lead_temperature": "Cold",
        "lead_score": 15,
        "next_best_action": "Send dormant reactivation SMS template",
        "consent_to_contact": 1,
        "preferred_contact_channel": "SMS",
        "email_address": "demo.saver010@example.test",
        "primary_phone": "+256700000010",
        "projection_viewed": 1,
        "checkout_started": 1,
        "payment_completed": 0,
        "staff_notes": "Retention and dormancy scenario. Onboarded over 60 days ago. Started checkout once, never completed. Overdue for engagement.",
        "comms": [
            {
                "channel": "SMS",
                "template": "dormant_lead_reactivation",
                "status": "Sent",
                "recipient": "+25670******10"
            }
        ]
    }
]


def get_demo_seed_preview():
    """Return scenarios preview without writing to the database."""
    return SCENARIOS


def seed_demo_data():
    """
    Idempotently write exactly 10 fictional scenarios to the database.
    Only touches records matching the 'DEMO-SMARTLIFE-' pattern.
    """
    summary = {
        "status": "completed",
        "mode": "demo_seed",
        "primary_demo_records": len(SCENARIOS),
        "leads_created": 0,
        "leads_updated": 0,
        "contribution_intents_created": 0,
        "contribution_intents_updated": 0,
        "communication_logs_created": 0,
        "communication_logs_updated": 0,
        "support_requests_created": 0,
        "support_requests_updated": 0,
        "skipped": [],
        "errors": []
    }

    for item in SCENARIOS:
        try:
            lead_name = item["id"]
            
            # 1. Lead Record
            lead_data = {
                "doctype": "SmartLife Demo Lead",
                "naming_series": "SL-LEAD-.YYYY.-.####",
                "first_name": item["first_name"],
                "last_name": item["last_name"],
                "gender": item["gender"],
                "segment": item["segment"],
                "goal": item["goal"],
                "goal_label": item["goal_label"],
                "target_amount": item["target_amount"],
                "years": item["years"],
                "frequency": item["frequency"],
                "initial_deposit": item["initial_deposit"],
                "source_of_income": item["source_of_income"],
                "industry": item["industry"],
                "country": item["country"],
                "staff_assisted": item["staff_assisted"],
                "journey_type": item["journey_type"],
                "plan_generated": item["plan_generated"],
                "payment_simulated": item["payment_simulated"],
                "lead_stage": item["lead_stage"],
                "lead_status": item["lead_status"],
                "lead_temperature": item["lead_temperature"],
                "lead_score": item["lead_score"],
                "next_best_action": item["next_best_action"],
                "consent_to_contact": item["consent_to_contact"],
                "preferred_contact_channel": item["preferred_contact_channel"],
                "email_address": item["email_address"],
                "primary_phone": item["primary_phone"],
                "projection_viewed": item["projection_viewed"],
                "checkout_started": item["checkout_started"],
                "payment_completed": item["payment_completed"],
                "staff_notes": item["staff_notes"],
                "created_session_id": f"sess-{item['id'].lower()}"
            }

            if frappe.db.exists("SmartLife Demo Lead", lead_name):
                doc = frappe.get_doc("SmartLife Demo Lead", lead_name)
                doc.update(lead_data)
                doc.save(ignore_permissions=True)
                summary["leads_updated"] += 1
            else:
                lead_data["name"] = lead_name
                doc = frappe.get_doc(lead_data)
                doc.insert(ignore_permissions=True)
                if doc.name != lead_name:
                    frappe.rename_doc("SmartLife Demo Lead", doc.name, lead_name, force=True)
                    doc.name = lead_name
                summary["leads_created"] += 1

            # 2. Linked Contribution Intent
            if "intent" in item:
                intent_name = f"SL-INTENT-{item['id']}"
                intent_data = {
                    "doctype": "SmartLife Contribution Intent",
                    "lead": lead_name,
                    "session_id": f"sess-{item['id'].lower()}",
                    "saver_type": item["segment"],
                    "contribution_amount": item["intent"]["amount"],
                    "contribution_frequency": item["intent"]["frequency"],
                    "payment_method": item["intent"]["method"],
                    "payment_status": item["intent"]["status"],
                    "payment_reference": item["intent"]["reference"],
                    "pesapal_tracking_id": item["intent"]["tracking_id"],
                    "pesapal_merchant_reference": item["intent"]["merchant_ref"],
                    "created_by_channel": "Self-Serve" if item["journey_type"] == "self-serve" else "Staff-Assisted",
                    "demo_mode": 1,
                    "failure_reason": item["intent"].get("failure_reason", "")
                }
                
                if frappe.db.exists("SmartLife Contribution Intent", intent_name):
                    idoc = frappe.get_doc("SmartLife Contribution Intent", intent_name)
                    idoc.update(intent_data)
                    idoc.save(ignore_permissions=True)
                    summary["contribution_intents_updated"] += 1
                else:
                    intent_data["name"] = intent_name
                    idoc = frappe.get_doc(intent_data)
                    idoc.insert(ignore_permissions=True)
                    summary["contribution_intents_created"] += 1

            # 3. Linked Communication Logs
            if "comms" in item:
                for idx, comm in enumerate(item["comms"]):
                    comm_name = f"SCOMLOG-{item['id']}-{idx}"
                    comm_data = {
                        "doctype": "SmartLife Communication Log",
                        "lead": lead_name,
                        "channel": comm["channel"],
                        "template_name": comm["template"],
                        "recipient_masked": comm["recipient"],
                        "recipient_type": "Phone" if comm["channel"] == "SMS" else "Email",
                        "message_status": comm["status"],
                        "provider": "ZeptoMail" if comm["channel"] == "Email" else "Phahapa",
                        "provider_reference": f"prov-ref-{item['id'].lower()}-{idx}",
                        "client_reference": f"client-ref-{item['id'].lower()}-{idx}",
                        "consent_snapshot": item["consent_to_contact"],
                        "demo_mode": 1
                    }
                    
                    if frappe.db.exists("SmartLife Communication Log", comm_name):
                        cdoc = frappe.get_doc("SmartLife Communication Log", comm_name)
                        cdoc.update(comm_data)
                        cdoc.save(ignore_permissions=True)
                        summary["communication_logs_updated"] += 1
                    else:
                        comm_data["name"] = comm_name
                        cdoc = frappe.get_doc(comm_data)
                        cdoc.insert(ignore_permissions=True)
                        summary["communication_logs_created"] += 1

            # 4. Linked Support Requests
            if "support" in item:
                support_name = f"SL-SUPPORT-{item['id']}"
                support_data = {
                    "doctype": "SmartLife Support Request",
                    "lead": lead_name,
                    "session_id": f"sess-{item['id'].lower()}",
                    "support_category": item["support"]["category"],
                    "preferred_contact_channel": item["preferred_contact_channel"],
                    "message": item["support"]["message"],
                    "status": item["support"]["status"],
                    "assigned_staff": item["support"].get("assigned_staff", ""),
                    "resolution_notes": item["support"].get("resolution_notes", ""),
                    "consent_snapshot": item["consent_to_contact"],
                    "demo_mode": 1
                }
                
                if frappe.db.exists("SmartLife Support Request", support_name):
                    sdoc = frappe.get_doc("SmartLife Support Request", support_name)
                    sdoc.update(support_data)
                    sdoc.save(ignore_permissions=True)
                    summary["support_requests_updated"] += 1
                else:
                    support_data["name"] = support_name
                    sdoc = frappe.get_doc(support_data)
                    sdoc.insert(ignore_permissions=True)
                    summary["support_requests_created"] += 1

        except Exception as e:
            summary["errors"].append({"id": item["id"], "error": str(e)})

    return summary


def clear_demo_data():
    """
    Safely delete all demo seed records generated by this module.
    Never touches production user data.
    """
    summary = {
        "status": "completed",
        "mode": "demo_clear",
        "leads_deleted": 0,
        "contribution_intents_deleted": 0,
        "communication_logs_deleted": 0,
        "support_requests_deleted": 0,
        "errors": []
    }

    # 1. Clear contribution intents
    try:
        intents = frappe.get_all("SmartLife Contribution Intent", filters=[["name", "like", "SL-INTENT-DEMO-SMARTLIFE-%"]])
        for intent in intents:
            frappe.delete_doc("SmartLife Contribution Intent", intent.name, ignore_permissions=True)
            summary["contribution_intents_deleted"] += 1
    except Exception as e:
        summary["errors"].append({"doctype": "SmartLife Contribution Intent", "error": str(e)})

    # 2. Clear communication logs
    try:
        logs = frappe.get_all("SmartLife Communication Log", filters=[["name", "like", "SCOMLOG-DEMO-SMARTLIFE-%"]])
        for log in logs:
            frappe.delete_doc("SmartLife Communication Log", log.name, ignore_permissions=True)
            summary["communication_logs_deleted"] += 1
    except Exception as e:
        summary["errors"].append({"doctype": "SmartLife Communication Log", "error": str(e)})

    # 3. Clear support requests
    try:
        requests = frappe.get_all("SmartLife Support Request", filters=[["name", "like", "SL-SUPPORT-DEMO-SMARTLIFE-%"]])
        for req in requests:
            frappe.delete_doc("SmartLife Support Request", req.name, ignore_permissions=True)
            summary["support_requests_deleted"] += 1
    except Exception as e:
        summary["errors"].append({"doctype": "SmartLife Support Request", "error": str(e)})

    # 4. Clear lead records
    try:
        leads = frappe.get_all("SmartLife Demo Lead", filters=[["name", "like", "DEMO-SMARTLIFE-%"]])
        for lead in leads:
            frappe.delete_doc("SmartLife Demo Lead", lead.name, ignore_permissions=True)
            summary["leads_deleted"] += 1
    except Exception as e:
        summary["errors"].append({"doctype": "SmartLife Demo Lead", "error": str(e)})

    return summary
