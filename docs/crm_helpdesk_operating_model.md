# CRM & Helpdesk Operating Model — Phase 1

## Status: PARTIALLY SIMULATED in Phase 1

## What Exists Now
- SmartLife Staff Assist Session — logs prospect sessions
- SmartLife Follow Up Task — logs follow-up actions
- SmartLife Demo Notification — logs helpdesk handoffs
- Support form → logs to SmartLife Demo Notification

## Frappe Helpdesk Integration (Phase 2)
- frappe/helpdesk app must be installed
- Support tickets created via Helpdesk API
- SmartLife staff sessions linked to Helpdesk tickets
- SLA tracking per customer segment

## CRM Stages (Phase 2 Pipeline)
1. New Prospect → Staff session initiated
2. Interested → Plan shown, projection viewed
3. Plan Shown → Personalised plan generated
4. Objection Raised → Objection script delivered
5. Follow-up Scheduled → Follow-up task created
6. Converted → Payment simulated / account registered
7. Lost → Dropoff recorded

## Staff Workflow (Phase 1 Simulated)
1. Staff opens /smartlife-staff-assist
2. Fills session form with prospect details (no real PII)
3. System generates pitch script and objection response
4. Staff copies script for use in real conversation
5. Session logged in SmartLife Staff Assist Session

## What Requires NSSF Approval for Phase 2
- CRM data access policies
- Staff training on real member data handling
- Helpdesk SLA definitions
- Escalation paths to NSSF compliance team
