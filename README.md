# SmartLife Flexi Demo

Demo growth, onboarding and staff-assist system for SmartLife Flexi.

## Source of Truth

GitHub repository: sebunya/nssf_smart_savers

Production/demo site: nssf-smartlifeflexi.nile-gov-demo.com

Bench path: /home/frappe/frappe-bench

Frappe app name: nssf_smart_savers

## Demo Safety Notice

This is a prototype/demo environment.

Do not enter real NSSF member data, real NINs, real phone numbers, real emails, real payment credentials, or any other personally identifiable information.

Public demo pages must clearly display:

SmartLife Flexi Demo. Prototype environment. Do not enter real NSSF member data.

Projection pages must clearly display:

Projection is indicative for demo purposes only. Actual returns may vary.

## Expected Installed Apps

frappe  
telephony  
helpdesk  
nssf_smart_savers

Check installed apps:

cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com list-apps

## First-Time Install

cd /home/frappe/frappe-bench
bench get-app github-nssf:sebunya/nssf_smart_savers.git --branch main
bench --site nssf-smartlifeflexi.nile-gov-demo.com install-app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

## Repeat Deployment

cd /home/frappe/frappe-bench/apps/nssf_smart_savers
scripts/deploy_production.sh

## Smoke Test

cd /home/frappe/frappe-bench/apps/nssf_smart_savers
scripts/smoke_test.sh

## Analytics Context

Google Tag Manager: GTM-PZRV3MQL

GA4 Measurement ID: G-3QNFS6QHW4

Microsoft Clarity Project ID: uvlttflnbt

No PII should be sent to analytics events.

Do not send NIN, phone number, email, full name, member number, payment contact, payment reference, OTP, or free-text personal identifiers.

## Rollback

1. Identify the previous good commit.
2. Check out that commit in /home/frappe/frappe-bench/apps/nssf_smart_savers.
3. Run migrate.
4. Build assets.
5. Clear cache.
6. Restart supervisor workers and web.
7. Reload nginx.
8. Run the smoke test.

If database migrations are not safely reversible, restore from the bench backup created before deployment.

## Known Limitations

This is a demo environment.

Production-only integrations are not enabled:
- live NSSF member data
- live NIRA verification
- live payment rails
- real OTP delivery
- real notifications
- real contribution posting

---

## Phase 1 Implementation Status

### Routes Implemented
| Route | Status |
|-------|--------|
| /smartlife-flexi-demo | ✅ Live |
| /smartlife-self-serve | ✅ Live (5-step journey) |
| /smartlife-staff-assist | ✅ Live |
| /smartlife-projection-demo | ✅ Live |
| /smartlife-checkout-demo | ✅ Live (simulated) |
| /smartlife-thank-you | ✅ Live |
| /smartlife-support-demo | ✅ Live |

### DocTypes Created (10)
- SmartLife Demo Lead
- SmartLife Demo Plan
- SmartLife Projection Scenario
- SmartLife Staff Assist Session
- SmartLife Demo Payment
- SmartLife Demo Notification
- SmartLife Integration Event
- SmartLife Personalisation Rule
- SmartLife Follow Up Task
- SmartLife Dropoff Event

### APIs Available
- `nssf_smart_savers.api.get_projection` — compound interest projection
- `nssf_smart_savers.api.get_personalised_plan_api` — personalised plan copy
- `nssf_smart_savers.api.submit_demo_lead` — log demo journey
- `nssf_smart_savers.api.submit_staff_assist` — log staff session
- `nssf_smart_savers.api.simulate_payment` — simulate Pesapal payment
- `nssf_smart_savers.api.log_analytics_event` — GTM event logging
- `nssf_smart_savers.api.request_support` — support request
- `nssf_smart_savers.api.log_dropoff` — dropoff tracking

### Analytics
- GTM Container: GTM-PZRV3MQL
- 10 event types, all PII-safe

### Known Limitations
- All payments are simulated (no real Pesapal integration)
- SMS not delivered (Phahapa not configured)
- Email not delivered (ZeptoMail not configured)
- No real member authentication
- No NIN verification
- No real helpdesk ticket creation

### Next Phase Recommendations
1. Wire Pesapal sandbox (credentials required)
2. Wire Phahapa SMS (sender ID approval required)
3. Wire ZeptoMail email (from address verification required)
4. Add NSSF member authentication
5. Frappe Helpdesk integration for real ticket creation
6. Compliance review before any real member data collection
