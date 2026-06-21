# Phase 1 Preservation Audit

**Date:** 2026-06-21  
**Branch:** claude/cool-bell-t7n0hs  
**Checkpoint branch:** safeguard-before-nssf-ui-pii-pass-20260621

## Working routes (must remain functional)
- /smartlife-flexi-demo — landing page, GTM present
- /smartlife-self-serve — 5-step self-serve onboarding (expanding to 6)
- /smartlife-staff-assist — staff-guided prospect session
- /smartlife-projection-demo — savings projection calculator
- /smartlife-checkout-demo — checkout summary
- /smartlife-thank-you — confirmation page
- /smartlife-support-demo — support / helpdesk

## Working assets (must remain at 200)
- /assets/nssf_smart_savers/css/smartlife.css
- /assets/nssf_smart_savers/js/smartlife.js
- /assets/nssf_smart_savers/js/analytics_helper.js

## Working APIs (must remain functional)
- submit_self_serve_step (whitelist)
- get_savings_projection (whitelist)
- submit_staff_session (whitelist)
- submit_checkout (whitelist)

## Integration adapters (do not break)
- integrations/pesapal_adapter.py
- integrations/phahapa_sms_adapter.py
- integrations/zeptomail_adapter.py
- integrations/crm_adapter.py
- integrations/helpdesk_adapter.py

## DocTypes (do not delete, only extend)
- Demo Lead, Onboarding Session, Savings Plan, Projection Result,
  Staff Session Log, Demo Notification, Smart Savers Settings,
  Demo Checkout Session, Demo Payment Log, Demo Analytics Event

## Safety invariants (non-negotiable)
- Every public page shows "Prototype environment" notice
- Projection pages show indicative disclaimer
- PII NEVER reaches GTM/GA4/Clarity/URL query strings/logs
- analytics_helper.js blocks: name, phone, email, nin keys

## Phase 5 changes
- CSS variables renamed to --nssf-* brand palette
- Asset cache-bust: ?v=nssf-brand-pii-safe-20260622
- Self-serve expanded to 6 steps (Personal Details as Step 2)
- Staff-assist gets PII fields + output enhancements
- analytics_helper.js PII block-list made explicit
