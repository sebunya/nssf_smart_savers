# SmartLife Flexi — Remaining Build Manifest (Phases 3–8)

**Anti-Gravity must work one phase at a time. Stop after each phase. Do not start the next phase until the previous phase's smoke test passes and a human approves.**

---

## Phase 3 — Payment and Contribution Readiness

| Item | Detail |
|---|---|
| **Objective** | Contribution intent DocType, Pesapal sandbox checkout, payment status lifecycle |
| **New routes** | Enhance `/smartlife-checkout-demo` (no new route needed) |
| **New DocTypes** | `SmartLife Contribution Intent` |
| **New APIs** | `create_payment_intent`, `initiate_pesapal_checkout`, `handle_pesapal_callback`, `handle_pesapal_ipn`, `verify_payment_status`, `get_contribution_intent` |
| **New scripts** | `scripts/smoke_test_phase_3.sh` |
| **Docs to update** | `docs/phase_3_payment_contribution_readiness_spec.md`, `docs/payment_architecture_pesapal.md` |
| **Dependencies** | Phase 2 merged + migrated on server; Pesapal sandbox credentials (do not commit) |
| **PII/privacy** | Payment reference is PII — never analytics; Pesapal tracking ID stays internal |
| **Smoke test required** | Phase 1 + Phase 2 + Phase 3 must all pass |
| **Acceptance criteria** | Contribution Intent DocType exists; payment APIs exist; checkout returns 200; no credentials committed; demo fallback if credentials missing |
| **Stop condition** | Stop after Phase 3 smoke passes. Do not start Phase 4. |

---

## Phase 4 — Communications and Personalisation

| Item | Detail |
|---|---|
| **Objective** | Consent-gated SMS/email/WhatsApp-ready lifecycle messaging |
| **New routes** | None (staff queue may gain "Send message" action) |
| **New DocTypes** | `SmartLife Communication Log` |
| **New APIs** | `get_message_templates`, `preview_message`, `send_demo_message`, `log_communication`, `get_communication_history` |
| **New scripts** | `scripts/smoke_test_phase_4.sh` |
| **Docs to update** | `docs/phase_4_communications_personalisation_spec.md`, `docs/sms_architecture_phahapa.md`, `docs/email_architecture_zeptomail.md` |
| **Dependencies** | Phase 3 complete; Phahapa SMS credentials (env var only); ZeptoMail credentials (env var only) |
| **PII/privacy** | Recipient must be masked in log list views; consent_to_contact must be true; no outbound unless consent confirmed |
| **Smoke test required** | Phase 1 + 2 + 3 + 4 |
| **Acceptance criteria** | Templates exist; no send without consent; Communication Log DocType exists; credentials not committed |
| **Stop condition** | Stop after Phase 4 smoke passes. Do not start Phase 5. |

---

## Phase 5 — Command Centre and Analytics

| Item | Detail |
|---|---|
| **Objective** | Management dashboard for NSSF — aggregate analytics, no raw PII |
| **New routes** | `/smartlife-command-centre` |
| **New DocTypes** | None (reads from existing DocTypes) |
| **New APIs** | `get_command_centre_summary`, `get_conversion_funnel`, `get_dropoff_by_stage`, `get_lead_distribution`, `get_campaign_performance`, `get_birth_month_distribution` |
| **New scripts** | `scripts/smoke_test_phase_5.sh` |
| **Docs to update** | `docs/phase_5_command_centre_analytics_spec.md`, `docs/analytics_event_dictionary.md` |
| **Dependencies** | Phase 4 complete |
| **PII/privacy** | Aggregates only; birthday_month only as distribution count; no individual records; no PII labels rendered |
| **Smoke test required** | Phase 1 + 2 + 3 + 4 + 5 |
| **Acceptance criteria** | Route returns 200; all dashboard API endpoints exist; no PII in any API response; no analytics PII leakage |
| **Stop condition** | Stop after Phase 5 smoke passes. Do not start Phase 6. |

---

## Phase 6 — Support and Helpdesk

| Item | Detail |
|---|---|
| **Objective** | Usable support flow for prospects needing onboarding help |
| **New routes** | Enhance `/smartlife-support-demo` (no new route needed) |
| **New DocTypes** | `SmartLife Support Request` |
| **New APIs** | `create_support_request`, `get_support_requests`, `assign_support_request`, `update_support_status` |
| **New scripts** | `scripts/smoke_test_phase_6.sh` |
| **Docs to update** | `docs/phase_6_support_helpdesk_spec.md`, `docs/crm_helpdesk_operating_model.md` |
| **Dependencies** | Phase 5 complete; Frappe Helpdesk only if safe and low-risk |
| **PII/privacy** | Support messages sanitised before storage; no PII in API responses; consent_snapshot recorded |
| **Smoke test required** | Phase 1 + 2 + 3 + 4 + 5 + 6 |
| **Acceptance criteria** | Support Request DocType exists; all APIs exist; route returns 200; no PII leakage |
| **Stop condition** | Stop after Phase 6 smoke passes. Do not start Phase 7. |

---

## Phase 7 — Security, Privacy and Production Hardening

| Item | Detail |
|---|---|
| **Objective** | Audit and harden for serious NSSF review and production path |
| **New routes** | None |
| **New DocTypes** | None |
| **New APIs** | None |
| **New scripts** | `scripts/smoke_test_phase_7.sh` |
| **Docs to update** | `docs/phase_7_security_privacy_hardening_spec.md`, `docs/demo_safety_rules.md`, create `docs/security_privacy_review.md` |
| **Dependencies** | All previous phases complete |
| **PII/privacy** | Full audit of all endpoints, routes, logs, analytics |
| **Smoke test required** | Phase 1 through 7 |
| **Acceptance criteria** | All prior smoke tests green; no traceback exposure; no PII in URLs/logs; role guard verified; no credentials in source |
| **Stop condition** | Stop after Phase 7. Do not start Phase 8 without human sign-off. |

---

## Phase 8 — Release Pack and Final Handover

| Item | Detail |
|---|---|
| **Objective** | Full demo and production handover documentation |
| **New routes** | None |
| **New DocTypes** | None |
| **New APIs** | None |
| **New scripts** | None |
| **Docs to create** | `docs/phase_2_to_8_release_notes.md`, `docs/nssf_smartlife_demo_walkthrough.md`, `docs/admin_user_guide.md`, `docs/staff_user_guide.md`, `docs/demo_script.md`, `docs/known_limitations.md`, `docs/production_readiness_checklist.md` |
| **Dependencies** | All phases complete; human sign-off on Phase 7 |
| **PII/privacy** | All docs must respect PII rules — no real data in examples |
| **Smoke test required** | All phase smoke tests |
| **Acceptance criteria** | All docs created; demo script covers full journey; production checklist approved by NSSF DPO |
| **Stop condition** | Terminal phase — project complete. |
