# NSSF SmartLife Flexi — Phase 2 to 8 Release Notes

## 1. Summary of Changes
This release delivers the complete voluntary growth prototype for NSSF Uganda.

### Phase 2: Staff-Assist Queue
- Created `SmartLife Demo Lead` DocType fields.
- Implemented authenticated staff authentication checks (`_require_personalisation_access()`).
- Added masked staff priorities view (`/smartlife-staff-queue`) and unmasked PII view (`/smartlife-staff-queue-full`).

### Phase 3: Payment Readiness
- Created `SmartLife Contribution Intent` DocType.
- Integrated Pesapal Adapter (`pesapal_adapter.py`) Supporting Sandbox integration.
- Added `/smartlife-checkout-demo` route.

### Phase 4: Communications & Personalisation
- Created `SmartLife Communication Log` DocType.
- Integrated ZeptoMail API adapter (`zeptomail.py`) and Phahapa SMS adapter (`phahapa_sms.py`).
- Integrated double-enforcement consent gates checking `consent_to_contact`.

### Phase 5: Command Centre & Analytics
- Added `/smartlife-command-centre` aggregate dashboard.
- Configured whitelisted aggregate analytics APIs in `api.py`.

### Phase 6: Support & Helpdesk
- Created `SmartLife Support Request` DocType.
- Structured support forms inside `/smartlife-support-demo` mapping to 7 spec topics.
- Setup Helpdesk Adapter fallback mechanisms.

### Phase 7: Security Hardening
- Completed security reviews covering CSRF configurations, secrets safety, log hygiene, and PII double-enforcement.

### Phase 8: Handover & Readiness
- Finalized technical documentation, runbooks, rollback plans, and technical inventories.

---

## 2. New DocTypes
- `SmartLife Demo Lead`
- `SmartLife Contribution Intent`
- `SmartLife Communication Log`
- `SmartLife Support Request`

---

## 3. Migration Requirements
Rebuilding schemas requires the operator to execute:
`bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate`
`bench build --app nssf_smart_savers`
