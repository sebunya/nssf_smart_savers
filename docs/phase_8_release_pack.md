# SmartLife Flexi — Phase 8 Release Pack

## 1. Release Overview
- **Release Title**: SmartLife Flexi Voluntary Saving Growth System (Phases 1–8)
- **Release Purpose**: Deliver the complete voluntary growth prototype for NSSF Uganda, including self-serve/staff-assisted onboarding, DOB personalization, payment integration, suppression messaging, aggregate analytics, and member support workflows.
- **Product Scope**: Handover documentation, validation suites, and deployment assets.
- **Current Local Status**: `Phase 8 release pack complete / server validation pending`

## 2. Commit & Phase Register
- **Handover commit**: `2c22e04` — Anti-Gravity handover and execution documentation pack
- **Phase 3 commit**: `d0e2786` — Payment and Contribution Readiness
- **Phase 4 commit**: `4339a7f` — Communications & Personalisation
- **Phase 5 commit**: `24d9b75` — Command Centre & Analytics
- **Phase 6 commit**: `f4e522a` — Support & Helpdesk
- **Phase 7 commit**: `5ab1b69` — Security and Privacy Hardening
- **Phase 8 commit**: [Present Commit Hash] — Release Pack and Production Readiness

---

## 3. Product Inventory

### New DocTypes
1. `SmartLife Demo Lead` (Onboarding database)
2. `SmartLife Contribution Intent` (Payment intents and reconciliation statuses)
3. `SmartLife Communication Log` (Notification logs and masked recipients)
4. `SmartLife Support Request` (Customer queries and triage metadata)

### Website Routes
- `/smartlife-flexi-demo` — Landing view
- `/smartlife-self-serve` — Public onboarding
- `/smartlife-staff-assist` — Staff-assisted onboarding
- `/smartlife-projection-demo` — Savings calculator
- `/smartlife-checkout-demo` — Payment selector & Sandbox intent
- `/smartlife-thank-you` — Confirmation and onboarding summary
- `/smartlife-support-demo` — Customer support submit form
- `/smartlife-staff-queue` — Masked staff follow-up priority list
- `/smartlife-staff-queue-full` — Full unmasked PII staff priority list
- `/smartlife-command-centre` — Operational dashboard

---

## 4. Operational Sign-Off Gates
Before production deployment can proceed:
1. **Server Operator Runbook Execution**: Successful git pulls, bench migrations, cache purges, and service restarts.
2. **Sequential Smoke Testing**: All 8 smoke validation suites (`scripts/smoke_test*.sh`) must return `0 failed`.
3. **Manual Role setup**: Create the `SmartLife Personalisation Team` role and assign it to support agents.
4. **NSSF DPO Sign-Off**: Verification of PII analytics double-enforcement masks and database fields.
