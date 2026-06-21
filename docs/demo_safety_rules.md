# Demo Safety Rules — SmartLife Flexi

## Non-Negotiable Rules

1. **Every public page** must show the demo notice banner:
   `⚠️ SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data.`

2. **Every projection/calculator page** must show the disclaimer:
   `Projection is indicative for demo purposes only. Actual returns may vary.`

3. **No real NIN** (National Identification Number) must be accepted.
   - Pattern: `^[A-Z]{2}\d{7}[A-Z]{2}$`
   - Rejected server-side in `safe_input.py` and client-side in `smartlife.js`

4. **No real phone numbers** must be accepted.
   - Pattern: `^(\+?256|0)[7][0-9]{8}$`
   - Rejected server-side and client-side

5. **No real email addresses** in demo lead fields.

6. **No real payment** — Pesapal is in `demo` mode only. No IPN endpoint wired.

7. **All DocType records** created in Phase 1 have `is_demo = 1`. These must be purged before production launch.

## Demo Data Hygiene
- Demo records must be cleared before production migration
- Do NOT restore a Phase 1 database backup to a production site
- Analytics events are labelled with `is_simulated = 1`

## What Must NOT Be Committed
- Real Pesapal API credentials
- Real Phahapa SMS credentials
- Real ZeptoMail credentials
- Any real member data from testing
- `.env` files with credentials

## What Requires NSSF/Compliance Approval Before Phase 2
- Real member data collection
- Payment gateway go-live
- SMS/email campaign content
- Data retention policies
- Privacy notice and consent flow
