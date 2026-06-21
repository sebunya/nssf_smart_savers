# Phase 1 Platform Architecture — SmartLife Flexi Growth OS

## Overview

Phase 1 is a fully simulated demo of the SmartLife Flexi voluntary savings onboarding experience. It runs inside a Frappe app on the NSSF demo infrastructure.

## Components

### Frappe App: nssf_smart_savers
- Version: Phase 1 (Demo)
- Module: Nssf Smart Savers
- Branch: claude/cool-bell-t7n0hs → merged to phase-1-smartlife-onboarding

### Routes (www/)
| Route | Purpose |
|-------|---------|
| /smartlife-flexi-demo | Hub / landing page |
| /smartlife-self-serve | 5-step self-serve journey |
| /smartlife-staff-assist | Staff-guided session form |
| /smartlife-projection-demo | Interactive projection calculator |
| /smartlife-checkout-demo | Simulated payment checkout |
| /smartlife-thank-you | Post-submission confirmation |
| /smartlife-support-demo | Support / helpdesk handoff |

### API (api.py)
All methods are `allow_guest=True`. No authentication required in Phase 1 demo.

### DocTypes (10 total)
1. SmartLife Demo Lead — captures self-serve journey data
2. SmartLife Demo Plan — personalised plan output
3. SmartLife Projection Scenario — calculator scenarios
4. SmartLife Staff Assist Session — staff-guided sessions
5. SmartLife Demo Payment — simulated payment records
6. SmartLife Demo Notification — notification logs
7. SmartLife Integration Event — analytics/integration events
8. SmartLife Personalisation Rule — configurable rules
9. SmartLife Follow Up Task — follow-up tasks
10. SmartLife Dropoff Event — dropoff tracking

### Public Assets
- /assets/nssf_smart_savers/css/smartlife.css
- /assets/nssf_smart_savers/js/smartlife.js
- /assets/nssf_smart_savers/js/analytics_helper.js

### Analytics
- GTM Container: GTM-PZRV3MQL
- Events pushed to window.dataLayer
- All params sanitised — no PII ever sent

## What Exists Now (Phase 1)
- All routes return 200
- Projection calculator live
- Personalisation engine (rule-based, Python)
- Staff assist script generator
- Payment simulation (Pesapal demo mode)
- Analytics event logging

## What Is Simulated
- Payment processing (Pesapal IPN not wired)
- SMS (Phahapa not configured)
- Email (ZeptoMail not configured)
- Helpdesk ticket creation (frappe-helpdesk API not wired)

## What Is Deferred to Phase 2
- Real member authentication
- Pesapal sandbox/live payment
- Phahapa SMS delivery
- ZeptoMail email delivery
- NSSF member registration API integration
- Real CRM/helpdesk workflow
