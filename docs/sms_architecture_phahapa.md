# SMS Architecture — Phahapa (Phase 1 Demo)

## Status: SIMULATED in Phase 1

## What Exists Now
- SmartLife Demo Notification DocType logs SMS intent
- Channel: "Phahapa SMS" (label only)
- Status: "Simulated" (no real delivery)

## What Phahapa Provides (Phase 2)
- HTTP API for SMS delivery
- Sender ID: NSSF_SMARTLIFE (requires approval)
- Unicode support for local languages
- Delivery reports via callback

## Templates Planned (Phase 2)
1. `plan_confirmation` — "Your SmartLife Flexi plan is set up. Goal: {goal}. Start: {frequency}."
2. `payment_received` — "Payment of UGX {amount} received. Reference: {ref}."
3. `follow_up_reminder` — "Your SmartLife savings reminder. Due: {date}."
4. `staff_follow_up` — Staff-initiated outreach message.

## Credentials Required (NOT in Phase 1)
- PHAHAPA_API_KEY
- PHAHAPA_SENDER_ID (NSSF-approved)
- PHAHAPA_BASE_URL

## What Requires NSSF/Regulatory Approval
- Sender ID registration
- Template content approval
- Opt-in/opt-out compliance
- Data retention for phone numbers

## Deferred to Phase 2
- Real SMS delivery
- Delivery status tracking
- Opt-out handling
