# Anti-Gravity Handover — NSSF SmartLife Flexi

**Prepared for:** Google Anti-Gravity  
**Prepared by:** Claude Code (Anthropic)  
**Date:** 2026-06-22  
**Status:** Phase 2 complete on Claude branch. Phase 3–8 not started.

---

## 1. Project Summary

### What is NSSF SmartLife Flexi?

NSSF SmartLife Flexi is a commissioned Frappe v15 web application for the **National Social Security Fund (NSSF) Uganda**. It is a multi-channel digital onboarding and lead management platform for the SmartLife Flexi voluntary savings product.

The app is a **demo/prototype environment only** — no real member data is collected or stored. It demonstrates the full onboarding lifecycle that NSSF intends to build for production.

### Business problem it solves

Uganda's NSSF SmartLife Flexi product has low digital enrolment. Most onboarding is manual, paper-based, or staff-assisted. The demo shows:

- How members can self-serve their way through goal selection, projection, and contribution planning
- How staff can assist in-branch or over the phone
- How the Personalisation Team can track, score, and follow up on leads
- How analytics can be captured without exposing PII to third-party platforms

### Phase 1 completed

- NSSF brand shell across all 7 public routes (navbar suppression, brand bar, NSSF colour palette)
- Self-serve onboarding journey: goal → projection → checkout → thank-you
- Staff-assisted onboarding journey
- DOB-based age derivation (no manual age entry)
- PII-safe analytics (allowlist-gated, never raw PII)
- Smoke test (`scripts/smoke_test.sh`) — 140 passed, 0 failed

### Phase 2 completed (on Claude branch — not yet merged to production)

- Lead lifecycle tracking on `SmartLife Demo Lead` (17 new fields)
- Deterministic lead scoring engine (`lead_scoring.py`) — score 0–100
- 6 new API endpoints for staff use
- `/smartlife-staff-queue` — masked public staff queue
- `/smartlife-staff-queue-full` — role-gated full PII staff queue
- Three-tier access model (Guest/masked, Approved role/full PII, Analytics/never PII)
- Real role-based guard: `SmartLife Personalisation Team`, `NSSF Staff`, `System Manager`
- Phase 2 smoke test (`scripts/smoke_test_phase_2.sh`) — 99 passed, 0 failed (source checks)

### What remains (Phases 3–8)

| Phase | Name | Summary |
|---|---|---|
| 3 | Payment & Contribution Readiness | Contribution intent DocType, Pesapal sandbox integration, checkout flow |
| 4 | Communications & Personalisation | SMS/email lifecycle messaging with consent enforcement |
| 5 | Command Centre & Analytics | Management dashboard — aggregate only, no PII |
| 6 | Support & Helpdesk | Enhanced support flow, support request DocType |
| 7 | Security & Privacy Hardening | CSRF, rate limiting, credential audit, PII audit |
| 8 | Release Pack | Demo scripts, admin guides, production checklist |

### What Anti-Gravity should do first

1. Confirm Phase 2 is merged and `bench migrate` has run on the server
2. Confirm both smoke tests pass on the live server
3. Begin Phase 3 only — do not jump ahead

### What must not be broken

- Phase 1 routes and smoke test
- Phase 2 DocType fields, API endpoints, role guard, analytics safety
- PII access model — public routes stay masked, analytics stays PII-free
- DOB logic — server computes age, never manual age input
- Credential safety — no live credentials committed

---

## 2. Repository and Branch State

| Item | Value |
|---|---|
| Repository | `sebunya/nssf_smart_savers` |
| App name | `nssf_smart_savers` |
| Frappe app path on server | `/home/frappe/frappe-bench/apps/nssf_smart_savers` |
| Claude working branch | `claude/cool-bell-t7n0hs` |
| Production deployment branch | `phase-1-smartlife-onboarding` |
| Site | `nssf-smartlifeflexi.nile-gov-demo.com` |
| Public URL | `https://nssf-smartlifeflexi.nile-gov-demo.com` |

### Key commits on Claude branch

```
b327d6a  Fix SmartLife Phase 2 role guard and analytics safety
079b438  Add authenticated Personalisation Team PII access model
06e9816  Add SmartLife lead operating system and staff queue
4cada55  Fix thank-you smoke test content pattern
43a5696  Align SmartLife smoke test with brand shell and thank-you content
1258796  Add critical brand shell include and fix smoke test temp-file approach
```

### Merge and migration status

- Phase 2 changes are on `claude/cool-bell-t7n0hs` — **not yet merged to `phase-1-smartlife-onboarding`**
- Phase 2 adds `staff_notes` and other fields to `SmartLife Demo Lead` — **`bench migrate` is required after merge**
- Do not start Phase 3 until merge, migration, and both smoke tests pass on server

### Deployment status

Phase 1 is live on `phase-1-smartlife-onboarding`. Phase 2 is pending merge.

---

## 3. Current Architecture

### Frappe app structure

```
nssf_smart_savers/
├── api.py                          — All whitelisted API endpoints
├── lead_scoring.py                 — Deterministic lead scoring (0–100)
├── hooks.py                        — Frappe app hooks
├── integrations/
│   ├── pesapal_adapter.py          — Pesapal payment stub (sandbox-ready)
│   ├── phahapa_sms_adapter.py      — Phahapa SMS stub
│   ├── zeptomail_adapter.py        — ZeptoMail email stub
│   ├── crm_adapter.py              — CRM stub
│   └── helpdesk_adapter.py         — Helpdesk stub
├── nssf_smart_savers/
│   └── doctype/
│       ├── smartlife_demo_lead/    — Primary DocType (extended in Phase 2)
│       ├── smartlife_demo_payment/
│       ├── smartlife_demo_plan/
│       ├── smartlife_demo_notification/
│       ├── smartlife_dropoff_event/
│       ├── smartlife_follow_up_task/
│       ├── smartlife_integration_event/
│       ├── smartlife_personalisation_rule/
│       ├── smartlife_projection_scenario/
│       └── smartlife_staff_assist_session/
├── public/
│   ├── css/smartlife.css           — NSSF brand stylesheet
│   └── js/
│       ├── smartlife.js            — Main frontend JS
│       └── analytics_helper.js     — PII-safe analytics (PII_KEYS block list)
├── templates/includes/
│   ├── smartlife_brand_shell.html  — Critical CSS + JS include (all routes)
│   └── smartlife_assets.html
├── utils/
│   ├── analytics.py                — ALLOWED_PARAMS allowlist, sanitise_event_params()
│   ├── personalisation.py          — Plan personalisation logic
│   ├── projection.py               — Projection calculation
│   ├── privacy.py                  — is_pii_safe() guard
│   └── safe_input.py               — looks_like_nin/phone/email, sanitise_demo_text()
└── www/
    ├── smartlife-flexi-demo.html/.py
    ├── smartlife-self-serve.html/.py
    ├── smartlife-staff-assist.html/.py
    ├── smartlife-projection-demo.html/.py
    ├── smartlife-checkout-demo.html/.py
    ├── smartlife-thank-you.html/.py
    ├── smartlife-support-demo.html/.py
    ├── smartlife-staff-queue.html/.py      — Phase 2 (masked)
    └── smartlife-staff-queue-full.html/.py — Phase 2 (role-gated full PII)
```

---

## 4. Current Routes

| Route | Purpose | Access Level | PII Status | Expected HTTP | Smoke Coverage |
|---|---|---|---|---|---|
| `/smartlife-flexi-demo` | Landing / goal selection | Public | No PII | 200 | Phase 1 |
| `/smartlife-self-serve` | Self-serve onboarding | Public | No PII in responses | 200 | Phase 1 |
| `/smartlife-staff-assist` | Staff-assisted onboarding | Public | No PII in responses | 200 | Phase 1 |
| `/smartlife-projection-demo` | Projection calculator | Public | No PII | 200 | Phase 1 |
| `/smartlife-checkout-demo` | Checkout simulation | Public | No PII | 200 | Phase 1 |
| `/smartlife-thank-you` | Thank-you / confirmation | Public | No PII | 200 | Phase 1 |
| `/smartlife-support-demo` | Support request | Public | Sanitised before storage | 200 | Phase 1 |
| `/smartlife-staff-queue` | Lead queue (masked) | Public | Masked phone/email only | 200 | Phase 2 |
| `/smartlife-staff-queue-full` | Full PII queue | SmartLife Personalisation Team / NSSF Staff / System Manager | Full PII (role-gated) | 200 (gate rendered for guest/no-role) | Phase 2 |

---

## 5. SmartLife Demo Lead DocType — All Fields

### Personal fields (Phase 1)
| Field | Type | Notes |
|---|---|---|
| `first_name` | Data | PII — never sent to analytics |
| `last_name` | Data | PII |
| `gender` | Select | |
| `primary_phone` | Data | PII — masked in public queue |
| `alt_phone` | Data | PII |
| `email_address` | Data | PII — masked in public queue |
| `preferred_contact_channel` | Select | |
| `consent_to_contact` | Check | Required gate for all comms |

### DOB-derived fields (Phase 1 — server computed)
| Field | Type | Notes |
|---|---|---|
| `date_of_birth` | Date | PII — stored in Frappe only, never analytics |
| `age_years` | Int | Server-computed from DOB — never analytics |
| `age_band` | Data | Safe analytics dimension (e.g. `25-34`) |
| `birthday_month` | Int | PII — never raw to analytics |
| `birthday_day` | Int | PII — never raw to analytics |

### Goal and plan fields (Phase 1)
| Field | Type | Notes |
|---|---|---|
| `segment` | Select | Safe analytics dimension (`saver_type`) |
| `goal` | Select | |
| `goal_label` | Data | |
| `target_amount` | Currency | |
| `years` | Int | |
| `frequency` | Select | |
| `initial_deposit` | Currency | |
| `source_of_income` | Data | |
| `industry` | Data | |
| `country` | Data | |
| `journey_type` | Select | |
| `staff_assisted` | Check | |
| `plan_generated` | Check | |
| `payment_simulated` | Check | |
| `dropoff_step` | Data | |
| `lead_stage` | Data | |

### Session / analytics fields (Phase 1)
| Field | Type | Notes |
|---|---|---|
| `created_session_id` | Data | Anonymous — sent to analytics |
| `analytics_labels` | Small Text | JSON safe dimensions |
| `demo_note` | Small Text | Always set to demo notice |

### Lifecycle fields (Phase 2)
| Field | Type | Notes |
|---|---|---|
| `lead_status` | Select | New → Disqualified (12 values) |
| `onboarding_stage` | Data | |
| `lead_temperature` | Select | Hot / Warm / Cold |
| `lead_score` | Int | 0–100, deterministic |
| `next_best_action` | Data | Staff recommendation |
| `assigned_staff` | Data | Demo staff name |
| `last_contacted_on` | Date | |
| `next_follow_up_on` | Date | |
| `follow_up_outcome` | Data | |
| `drop_off_reason` | Data | |
| `staff_notes` | Small Text | Internal only — never analytics |

### Attribution fields (Phase 2)
| Field | Type | Notes |
|---|---|---|
| `source_route` | Data | URL path |
| `campaign_source` | Data | UTM source |
| `campaign_medium` | Data | UTM medium |
| `campaign_name` | Data | UTM campaign |

### Journey flags (Phase 2)
| Field | Type | Notes |
|---|---|---|
| `projection_viewed` | Check | |
| `checkout_started` | Check | |
| `payment_completed` | Check | |

### Lead status lifecycle values
`New` → `Personal Details Captured` → `Goal Selected` → `Projection Viewed` → `Checkout Started` → `Payment Pending` → `Payment Completed` → `Staff Follow-up Required` → `Contacted` → `Converted` → `Dormant` → `Disqualified`

---

## 6. Proposed Future DocTypes

| DocType | Phase | Purpose |
|---|---|---|
| `SmartLife Contribution Intent` | 3 | Payment intent, Pesapal tracking, reconciliation |
| `SmartLife Communication Log` | 4 | Outbound message history with consent snapshot |
| `SmartLife Support Request` | 6 | Support ticket from prospect |

---

## 7. Existing DocTypes (built in Phase 1, not yet fully used)

| DocType | Notes |
|---|---|
| `SmartLife Demo Lead` | Primary — fully used Phase 1+2 |
| `SmartLife Demo Payment` | Stub — will be expanded Phase 3 |
| `SmartLife Demo Plan` | Stub |
| `SmartLife Demo Notification` | Stub — Phase 4 |
| `SmartLife Dropoff Event` | Used by `log_dropoff` |
| `SmartLife Follow Up Task` | Stub |
| `SmartLife Integration Event` | Used by `log_analytics_event` |
| `SmartLife Personalisation Rule` | Stub — Phase 4 |
| `SmartLife Projection Scenario` | Stub |
| `SmartLife Staff Assist Session` | Used by staff-assist flow |

---

## 8. Current API Endpoints

### Group A — Guest-safe public journey endpoints (`allow_guest=True`)

| Function | Purpose | Returns PII? | Mutates? | Notes |
|---|---|---|---|---|
| `get_projection` | Calculate savings projection | No | No | Pure computation |
| `get_personalised_plan_api` | Return personalised plan | No | No | age_band only |
| `submit_demo_lead` | Create/update lead from landing | No (returns session_id + age_band only) | Yes | Sets lead_status, scores |
| `submit_staff_assist` | Staff-assisted lead creation | No | Yes | |
| `submit_personal_details` | Capture personal details | No | Yes | Sets lead_status |
| `simulate_payment` | Simulate payment (demo) | No | Yes | Demo-safe |
| `log_analytics_event` | Log safe analytics event | No | Yes | PII filtered before storage |
| `request_support` | Create support request | No | Yes | Sanitised |
| `log_dropoff` | Record dropoff event | No | Yes | |

### Group B — Guest-safe masked/aggregate endpoints (`allow_guest=True`)

| Function | Purpose | Returns PII? | Mutates? | Notes |
|---|---|---|---|---|
| `score_lead` | Score by session_id | No (bands only) | No | Returns temperature + NBA |
| `get_lead_summary` | Aggregate counts | No | No | Counts only — no individual records |
| `get_staff_queue` | Paginated masked queue | Masked phone/email only | No | `phone_masked`, `email_masked` |

### Group C — Full PII endpoints (approved role required via `_require_personalisation_access()`)

| Function | Purpose | Returns PII? | Mutates? | Notes |
|---|---|---|---|---|
| `get_staff_queue_full` | Full unmasked queue | Yes — all fields | No | SmartLife Personalisation Team / NSSF Staff / System Manager |
| `get_lead_full_detail` | Single lead full detail | Yes — all fields | No | Same role guard |

### Group D — Authenticated write endpoints (any authenticated session via `_require_authenticated_staff()`)

| Function | Purpose | Returns PII? | Mutates? | Notes |
|---|---|---|---|---|
| `update_follow_up_status` | Record follow-up outcome | No | Yes | Logs outcome, updates status |
| `assign_lead` | Assign lead to staff | No | Yes | Staff name only |
| `update_journey_flag` | Set journey flag | No | Yes | projection_viewed / checkout_started / payment_completed |

---

## 9. PII Access Model

**Policy:**

> The SmartLife Personalisation Team is authorised under company policy to access customer/member PII for onboarding support, follow-up, consent verification, service recovery, conversion tracking, dormancy prevention, birthday readiness and personalised engagement. The system therefore supports full PII access in authenticated role-gated staff views, while public demo views remain masked and analytics remains PII-safe.

**Rules:**

- All public routes (`/smartlife-*`) show zero raw PII
- `/smartlife-staff-queue` shows masked phone (`070****545`) and masked email (`ro***@domain.com`) — aggregates only
- `/smartlife-staff-queue-full` requires approved Frappe role. Guest sees sign-in prompt. Signed-in user without role sees "Access restricted." Approved role sees full PII table.
- **Approved roles:** `SmartLife Personalisation Team`, `NSSF Staff`, `System Manager`
- **Analytics must never receive:** first_name, last_name, phone, email, NIN, DOB, birthday_day, birthday_month, age_years, exact_age, staff_notes, notes, free text
- **Analytics safe dimensions:** saver_type, age_band, goal_category, contribution_band, onboarding_stage, lead_temperature, consent_status, source_route, gender_category, country_category
- URLs must never contain raw PII
- Internal logs should avoid raw PII (log document name + action + staff user, not PII fields)

**Role assignment (manual, per environment):**
1. Sign in as Administrator
2. Setup → Roles → Create `SmartLife Personalisation Team`
3. Setup → Users → [staff user] → Roles → assign role
4. Repeat for each authorised Personalisation Team member

---

## 10. Current Acceptance Gates

Run these in order. Every gate must pass before Phase 3 starts.

```bash
# Source checks (run anywhere)
python -m compileall nssf_smart_savers
bash -n scripts/smoke_test.sh
bash -n scripts/smoke_test_phase_2.sh

# Live checks (run on server after merge + bench migrate)
./scripts/smoke_test.sh
./scripts/smoke_test_phase_2.sh
```

Expected Phase 1: ≥140 passed, 0 failed  
Expected Phase 2: ≥99 passed, 0 failed (live network warnings are acceptable)

---

## 11. Immediate Human/Server Actions Before Phase 3

The following must be done by a human with server access **before Anti-Gravity starts Phase 3**.

```bash
# 1. SSH to server as frappe user
ssh frappe@nssf-smartlifeflexi.nile-gov-demo.com

# 2. Navigate to app
cd /home/frappe/frappe-bench

# 3. Fetch Claude branch
git -C apps/nssf_smart_savers fetch origin claude/cool-bell-t7n0hs

# 4. Switch production branch and merge
git -C apps/nssf_smart_savers checkout phase-1-smartlife-onboarding
git -C apps/nssf_smart_savers merge origin/claude/cool-bell-t7n0hs

# 5. Migrate database (required for Phase 2 DocType fields including staff_notes)
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# 6. Build assets
bench build --app nssf_smart_savers

# 7. Clear cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

# 8. Restart services
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

# 9. Run smoke tests on server
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh

# 10. Assign roles in Frappe UI (if Personalisation Team access needed)
# Setup → Roles → Create 'SmartLife Personalisation Team'
# Setup → Users → [staff user] → Roles → assign
```

**Do not start Phase 3 until both smoke tests pass on the live server.**

---

## 12. Integration Stubs (ready but inactive)

These files exist and have stub implementations. Phase 3–4 will activate them:

| File | Provider | Status |
|---|---|---|
| `integrations/pesapal_adapter.py` | Pesapal (payment) | Stub — sandbox config needed |
| `integrations/phahapa_sms_adapter.py` | Phahapa (SMS) | Stub — credentials needed |
| `integrations/zeptomail_adapter.py` | ZeptoMail (email) | Stub — credentials needed |
| `integrations/crm_adapter.py` | CRM | Stub |
| `integrations/helpdesk_adapter.py` | Frappe Helpdesk | Stub |

---

## 13. Files Anti-Gravity Must Not Modify

Unless explicitly required by the current phase spec:

- `scripts/smoke_test.sh` — Phase 1 baseline
- `scripts/smoke_test_phase_2.sh` — Phase 2 baseline
- `nssf_smart_savers/api.py` — existing endpoint signatures
- `nssf_smart_savers/utils/analytics.py` — ALLOWED_PARAMS allowlist
- `nssf_smart_savers/public/js/analytics_helper.js` — PII_KEYS block list
- `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json` — only add fields, never remove
- `nssf_smart_savers/lead_scoring.py` — scoring logic
- All Phase 1 route HTML/JS/Python files
