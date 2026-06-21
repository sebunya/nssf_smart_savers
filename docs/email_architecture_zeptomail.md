# Email Architecture — ZeptoMail (Phase 1 Demo)

## Status: SIMULATED in Phase 1

## What Exists Now
- SmartLife Demo Notification DocType logs email intent
- Channel: "ZeptoMail Email" (label only)
- Status: "Simulated"

## What ZeptoMail Provides (Phase 2)
- Transactional email via API
- Template management
- Delivery/open/click tracking
- Bounce handling

## Templates Planned (Phase 2)
1. `plan_summary_email` — PDF-style plan summary
2. `payment_confirmation` — Payment receipt
3. `welcome_email` — Post-registration welcome
4. `staff_follow_up_email` — Staff-generated follow-up

## Credentials Required (NOT in Phase 1)
- ZEPTOMAIL_API_TOKEN
- ZEPTOMAIL_FROM_EMAIL (noreply@nssf.ug or similar)
- ZEPTOMAIL_FROM_NAME

## What Requires NSSF/Compliance Approval
- From address verification
- Email content approval
- Unsubscribe mechanism (CAN-SPAM / Uganda compliance)
- Data retention for email addresses
