# NSSF SmartLife Flexi — Final Technical Inventory

A complete list of registered routes, whitelisted APIs, DocTypes, and validation tests.

---

## 1. Registered Website Routes (`hooks.py`)
- `/smartlife-flexi-demo` -> Landing view
- `/smartlife-self-serve` -> Public self-serve onboarding
- `/smartlife-staff-assist` -> Staff-assisted onboarding
- `/smartlife-projection-demo` -> Projections savings calculator
- `/smartlife-checkout-demo` -> Payment method checkout
- `/smartlife-thank-you` -> Confirmation page
- `/smartlife-support-demo` -> Customer support request form
- `/smartlife-staff-queue` -> Public masked staff priorities queue
- `/smartlife-staff-queue-full` -> Authenticated full unmasked PII staff priority view
- `/smartlife-messaging-demo` -> Communications preview dashboard
- `/smartlife-command-centre` -> Aggregate analytics dashboard

---

## 2. Whitelisted API Endpoints (`api.py`)

### Guest-Open (`allow_guest=True`)
- `get_projection`: Projections calculations
- `get_personalised_plan_api`: Personalised advisors
- `submit_demo_lead`: Captures lead name, phone, email, and DOB
- `submit_personal_details`: Appends secondary personalization detail fields
- `update_demo_lead`: Lead updates handler
- `log_analytics_event`: Generic telemetry logs
- `create_payment_intent`: Contribution intent register
- `initiate_pesapal_checkout`: Sandbox transaction checkout
- `handle_pesapal_callback`: Checkout success redirection landing
- `handle_pesapal_ipn`: Transaction status listener
- `get_message_templates`: Lifecycle SMS/email template details
- `create_support_request`: Customer support ticket creations

### Staff-Only (`allow_guest=False`)
- `get_lead_summary` & `get_staff_queue`: Masked staff lists
- `get_staff_queue_full` & `get_lead_full_detail`: Unmasked PII lead data (Requires Role)
- `update_follow_up_status` & `assign_lead` & `update_journey_flag`: Leads queue management writes
- `verify_payment_status` & `get_contribution_intent`: Payment transaction lookups
- `preview_smartlife_message` & `send_smartlife_demo_message`: Notification previews and triggers
- `get_communication_history` & `get_messaging_config_status`: Communications histories
- `get_command_centre_summary` & `get_conversion_funnel` & `get_dropoff_by_stage` & `get_lead_distribution` & `get_campaign_performance` & `get_birth_month_distribution`: Command Centre metrics
- `get_support_requests` & `assign_support_request` & `update_support_status`: Support requests management queue

---

## 3. Registered DocTypes
- `SmartLife Demo Lead` (Onboarding database)
- `SmartLife Contribution Intent` (Payment transactions)
- `SmartLife Communication Log` (Notification logs)
- `SmartLife Support Request` (Customer queries)

---

## 4. Automation Tests & Scripts
- `scripts/smoke_test.sh` — Phase 1 validation
- `scripts/smoke_test_phase_2.sh` — Phase 2 validation
- `scripts/smoke_test_phase_3.sh` — Phase 3 validation
- `scripts/smoke_test_phase_4.sh` — Phase 4 validation
- `scripts/smoke_test_phase_5.sh` — Phase 5 validation
- `scripts/smoke_test_phase_6.sh` — Phase 6 validation
- `scripts/smoke_test_phase_7.sh` — Phase 7 validation
- `scripts/smoke_test_phase_8.sh` — Phase 8 validation
