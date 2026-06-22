# Anti-Gravity Full Phase Execution Pack — NSSF SmartLife Flexi
# Phases 3 through 8

**Prepared for:** Google Anti-Gravity  
**Prepared by:** Claude Code (Anthropic)  
**Date:** 2026-06-22  
**Branch:** `claude/cool-bell-t7n0hs`  
**Repository:** `sebunya/nssf_smart_savers`

---

## SECTION 1 — Current Repository State and Readiness Gate

### 1.1 Branch and Commit State

| Item | Value |
|---|---|
| Working branch | `claude/cool-bell-t7n0hs` |
| Production branch | `phase-1-smartlife-onboarding` |
| Latest commit | `12f3561 Add Anti-Gravity handover specs for SmartLife remaining phases` |
| Server path | `/home/frappe/frappe-bench/apps/nssf_smart_savers` |
| Site | `https://nssf-smartlifeflexi.nile-gov-demo.com` |

### 1.2 Handover Files Already Created

All ten handover files exist on the branch. Do not recreate them:

```
docs/anti_gravity_handoff.md           — master architecture reference
docs/remaining_build_manifest.md       — phase-by-phase summary
docs/anti_gravity_master_prompt.md     — session bootstrap prompt
docs/anti_gravity_validation_runbook.md — exact validation commands
docs/phase_3_payment_contribution_readiness_spec.md
docs/phase_4_communications_personalisation_spec.md
docs/phase_5_command_centre_analytics_spec.md
docs/phase_6_support_helpdesk_spec.md
docs/phase_7_security_privacy_hardening_spec.md
docs/phase_8_release_pack_spec.md
```

### 1.3 Files Not Modified (application code is unchanged)

Phase 1 and Phase 2 application code was last modified in commit `b327d6a`. The handover pack commits (`12f3561`) are documentation-only. No DocTypes, APIs, routes, frontend files, backend logic, fixtures, migrations, tests or working flows were touched.

### 1.4 Phase Status

| Phase | Status | Notes |
|---|---|---|
| Phase 1 | Complete and live | On `phase-1-smartlife-onboarding` |
| Phase 2 | Complete on branch — merge pending | On `claude/cool-bell-t7n0hs` only |
| Phase 3 | Not started | Must not start until section 1.5 is complete |
| Phase 4 | Not started | Depends on Phase 3 |
| Phase 5 | Not started | Depends on Phase 4 |
| Phase 6 | Not started | Depends on Phase 5 |
| Phase 7 | Not started | Depends on Phases 1–6 |
| Phase 8 | Not started | Depends on Phases 1–7 + human sign-off |

### 1.5 What Must Happen Before Phase 3 Starts

**STOP. Phase 3 must not start until every item in this section is complete.**

#### Human/Server Operator Duties (cannot be done by Anti-Gravity)

```bash
# 1. SSH to server
ssh frappe@nssf-smartlifeflexi.nile-gov-demo.com

# 2. Navigate to bench root
cd /home/frappe/frappe-bench

# 3. Fetch the Claude working branch
git -C apps/nssf_smart_savers fetch origin claude/cool-bell-t7n0hs

# 4. Switch to production branch and merge Phase 2
git -C apps/nssf_smart_savers checkout phase-1-smartlife-onboarding
git -C apps/nssf_smart_savers log --oneline origin/claude/cool-bell-t7n0hs ^HEAD
git -C apps/nssf_smart_savers merge origin/claude/cool-bell-t7n0hs

# 5. Migrate database (required — Phase 2 added staff_notes and lifecycle fields to SmartLife Demo Lead)
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# 6. Build app assets
bench build --app nssf_smart_savers

# 7. Clear all caches
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

# 8. Restart services
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

# 9. Verify services
sudo supervisorctl status frappe-bench-web:

# 10. Run smoke tests on server
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
# Both must show 0 failed before Phase 3 starts

# 11. Create SmartLife Personalisation Team role (Frappe UI)
# Setup → Roles → New → Name: SmartLife Personalisation Team → Save
# Setup → Users → [each authorised staff user] → Roles tab → add SmartLife Personalisation Team → Save

# 12. Confirm sign-off to Anti-Gravity
# Tell Anti-Gravity: "Phase 2 merged, migrated, smoke tests pass. Start Phase 3."
```

#### Anti-Gravity Duties Before Phase 3

```bash
# Run from inside the repo on the working branch
cd /home/frappe/frappe-bench/apps/nssf_smart_savers   # or local checkout

# 1. Check branch
git branch --show-current
# Expected: claude/cool-bell-t7n0hs

# 2. Python compile check
python3 -m compileall nssf_smart_savers -q

# 3. Syntax check smoke tests
bash -n scripts/smoke_test.sh
bash -n scripts/smoke_test_phase_2.sh

# 4. Read architecture before touching files
# docs/anti_gravity_handoff.md — architecture, routes, DocTypes, APIs, PII model
# docs/phase_3_payment_contribution_readiness_spec.md — Phase 3 spec
```

### 1.6 Known Risks at Readiness Gate

| Risk | Description | Mitigation |
|---|---|---|
| Missing `bench migrate` | Phase 2 adds fields to SmartLife Demo Lead. Without migrate, live routes return HTTP 417. | Human operator must migrate before Phase 3. Anti-Gravity cannot run bench commands. |
| Missing role | `SmartLife Personalisation Team` role must exist in Frappe before role-gated views work. | Human operator creates role manually. |
| Network-blocked CI | Cloud CI environments block outbound HTTP. Smoke test HTTP checks warn instead of failing. | Run smoke tests on server for authoritative result. |
| Credentials missing | Pesapal, Phahapa, ZeptoMail credentials not committed. Phase 3+ requires sandbox credentials for end-to-end payment testing. | Human operator configures site config before Phase 3 end-to-end test. |

### 1.7 Stop Conditions at Readiness Gate

- Do not start Phase 3 if either smoke test fails on the server
- Do not start Phase 3 if human has not confirmed Phase 2 server merge is complete
- Do not start Phase 3 if `bench migrate` has not run
- Do not start Phase 3 if Python compile check fails

---

## SECTION 2 — Non-Negotiable Build Rules

### 2.1 Phase discipline

- **One phase at a time.** Complete Phase N fully before starting Phase N+1.
- **No skipping.** Phase 4 depends on Phase 3. Phase 5 depends on Phase 4. Do not implement Phase 5 features during Phase 3.
- **Every change traces to a phase spec.** Do not add features, refactor, or introduce abstractions not required by the current phase spec.
- **Stop on failure.** If any previous-phase smoke test fails after a new phase is implemented, stop immediately. Fix the regression. Do not add Phase N+1 on top of failing Phase N.
- **Human sign-off required after Phase 7.** Do not start Phase 8 without explicit human confirmation.

### 2.2 Credentials

- **Never commit** Pesapal, Phahapa, ZeptoMail, or any other live credential to source code.
- Credentials go in Frappe site config (`frappe.conf`) or environment variables only.
- If credentials are missing, all integration stubs must silently fall back to demo/simulated mode.
- The smoke test scans for credential patterns. If a credential scan fails, you have committed a credential.
- Pattern scan covers: `sk_live`, `pk_live`, `SECRET_KEY`, `PRIVATE_KEY`, `PESAPAL_SECRET`, `PHAHAPA_KEY`, `ZEPTOMAIL_TOKEN`, `API_KEY =`

### 2.3 PII protection (mandatory, every phase)

**Never send to analytics (GTM / GA4 / Clarity / dataLayer):**
`first_name`, `last_name`, `full_name`, `phone`, `primary_phone`, `email`, `nin`, `national_id`, `date_of_birth`, `dob`, `birthday_day`, `birthday_month`, `age_years`, `exact_age`, `staff_notes`, `notes`, `payment_reference`, `otp`, `password`

**Safe analytics dimensions only:**
`saver_type`, `age_band`, `goal_category`, `contribution_band`, `onboarding_stage`, `lead_temperature`, `consent_status`, `source_route`, `staff_view_type`, `gender_category`, `country_category`, `demo_environment`

- `ALLOWED_PARAMS` in `utils/analytics.py` is the authoritative server-side allowlist. Do not add PII to it.
- `PII_KEYS` in `public/js/analytics_helper.js` is the authoritative frontend block list. Do not remove keys from it.
- Public routes must return zero raw PII.
- URLs must never contain raw PII (no phone/email/name/NIN in query strings).
- Internal logs should log document name and action type — not raw PII field values.

### 2.4 DocType discipline

- **Never remove a field** from `SmartLife Demo Lead` or any existing DocType.
- **Only add** fields to existing DocTypes.
- **Never change existing API endpoint signatures.** Add new endpoints only (append to `api.py`).
- Every new DocType must have: JSON definition, Python controller, permissions model, PII classification for each field.

### 2.5 Migration discipline

- Any phase that adds a new DocType requires `bench migrate` on the server before the new routes depending on it will work.
- Phases requiring migration: Phase 3 (SmartLife Contribution Intent), Phase 4 (SmartLife Communication Log), Phase 6 (SmartLife Support Request).
- Phase 5 requires no migration (no new DocTypes).
- Phase 7 requires no migration.
- Phase 8 requires no migration.

### 2.6 Smoke test discipline

- Run all prior smoke tests before starting each phase.
- Run all prior smoke tests after completing each phase.
- Never remove a check from an existing smoke test script.
- Never comment out a failing check. Fix the cause.
- If a check is flaky, make the check more reliable — do not remove it.
- Smoke tests run in CI may show `NETWORK UNAVAILABLE` warnings for HTTP route checks. These are acceptable. Zero `failed` is required. Warnings are not failures.

### 2.7 Preservation rules

Do not modify these files unless the current phase spec explicitly requires it:
- `scripts/smoke_test.sh`
- `scripts/smoke_test_phase_2.sh`
- `nssf_smart_savers/api.py` — existing endpoint bodies and signatures
- `nssf_smart_savers/utils/analytics.py` — ALLOWED_PARAMS
- `nssf_smart_savers/public/js/analytics_helper.js` — PII_KEYS
- `nssf_smart_savers/lead_scoring.py`
- All Phase 1 route HTML/JS/Python files
- `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json`

### 2.8 Rollback considerations

- Phase 3: If Contribution Intent DocType or checkout changes break things, revert the DocType JSON and api.py additions. Run `bench migrate` after revert.
- Phase 4: If Communication Log or send functions break things, revert DocType and api.py additions. No route changes to revert (staff queue enhancements only).
- Phase 5: If Command Centre route breaks things, delete `www/smartlife-command-centre.html` and `.py`. No migration needed.
- Phase 6: If Support Request DocType breaks things, revert DocType JSON and api.py additions. Run `bench migrate` after revert.
- Phase 7: No new DocTypes or routes. Revert any Python file changes if they break existing tests.
- Phase 8: Documentation only. Revert or delete any incorrect doc files.

---

## SECTION 3 — Master Phase Dependency Map

```
Phase 2 (branch) — PENDING HUMAN MERGE
    │
    ▼  [Human: merge → bench migrate → smoke tests pass → confirm to Anti-Gravity]
    │
Phase 3 — Payment and Contribution Readiness
    │  Depends on: Phase 2 merged, migrated, smoke tests green
    │  Unlocks: Phase 4
    │  Credentials required: Pesapal sandbox (for end-to-end test; demo fallback if absent)
    │  New DocType: SmartLife Contribution Intent → bench migrate required
    │  Smoke test: smoke_test_phase_3.sh (runs after 1+2 pass)
    │  Human approval: confirm Phase 3 smoke pass before Phase 4
    │
    ▼
Phase 4 — Communications and Personalisation
    │  Depends on: Phase 3 complete
    │  Unlocks: Phase 5
    │  Credentials required: Phahapa SMS, ZeptoMail (demo fallback if absent)
    │  New DocType: SmartLife Communication Log → bench migrate required
    │  Smoke test: smoke_test_phase_4.sh (runs after 1+2+3 pass)
    │  Human approval: confirm Phase 4 smoke pass before Phase 5
    │
    ▼
Phase 5 — Command Centre and Analytics
    │  Depends on: Phase 4 complete
    │  Unlocks: Phase 6
    │  Credentials required: None (aggregate reads only)
    │  New DocType: None → no bench migrate needed
    │  New route: /smartlife-command-centre
    │  Smoke test: smoke_test_phase_5.sh (runs after 1+2+3+4 pass)
    │  Human approval: confirm Phase 5 smoke pass before Phase 6
    │
    ▼
Phase 6 — Support and Helpdesk
    │  Depends on: Phase 5 complete
    │  Unlocks: Phase 7
    │  Credentials required: None
    │  New DocType: SmartLife Support Request → bench migrate required
    │  Smoke test: smoke_test_phase_6.sh (runs after 1+2+3+4+5 pass)
    │  Human approval: confirm Phase 6 smoke pass before Phase 7
    │
    ▼
Phase 7 — Security and Privacy Hardening
    │  Depends on: Phases 1–6 complete
    │  Unlocks: Phase 8 (only with human sign-off)
    │  Credentials required: None (audit and fix only)
    │  New DocType: None → no bench migrate needed
    │  New doc: docs/security_privacy_review.md
    │  Smoke test: smoke_test_phase_7.sh (runs after 1+2+3+4+5+6 pass)
    │  Human sign-off: MANDATORY before Phase 8
    │
    ▼  [STOP — do not start Phase 8 without explicit human approval]
    │
Phase 8 — Release Pack and Production Readiness
       Depends on: Phases 1–7 complete + human sign-off on Phase 7
       Terminal phase
       Credentials required: None (documentation only)
       New DocType: None
       New files: 7 release documents
       Smoke test: all prior smoke tests (no new smoke test)
       Human sign-off: NSSF Technical Lead + NSSF DPO + system integrator
```

### 3.1 Dependency table

| Phase | Depends on | Unlocks | Migrate | Credentials | Human sign-off |
|---|---|---|---|---|---|
| 3 | Phase 2 merged + migrated | Phase 4 | Yes | Pesapal sandbox (optional) | Confirm before Phase 4 |
| 4 | Phase 3 complete | Phase 5 | Yes | Phahapa + ZeptoMail (optional) | Confirm before Phase 5 |
| 5 | Phase 4 complete | Phase 6 | No | None | Confirm before Phase 6 |
| 6 | Phase 5 complete | Phase 7 | Yes | None | Confirm before Phase 7 |
| 7 | Phases 1–6 complete | Phase 8 | No | None | Mandatory — sign-off before Phase 8 |
| 8 | Phase 7 + sign-off | Terminal | No | None | NSSF DPO + Technical Lead |

---

## SECTION 4 — Phase 3 Full Execution Detail: Payment and Contribution Readiness

### 4.1 Phase Objective

Create a proper payment lifecycle tracker for SmartLife Flexi. Currently, `simulate_payment` on the checkout page marks a flag (`payment_simulated`) on the lead — there is no real payment record, no state machine, and no Pesapal integration. Phase 3 introduces `SmartLife Contribution Intent` as the payment record, wires up the Pesapal sandbox adapter (stubs already exist), and enhances the checkout page UX with a plan summary and safe demo fallback.

### 4.2 Business Purpose

NSSF needs to demonstrate to regulators and management that the SmartLife Flexi platform can receive mobile money or card contributions through Pesapal, track payment state from initiation to completion, reconcile failed payments, and integrate with NSSF's payment pipeline. Phase 3 proves this in sandbox mode. No real money moves.

### 4.3 User Journeys Affected

- Self-serve onboarding: after projection, user selects plan, proceeds to checkout, initiates Pesapal sandbox payment, receives confirmation
- Staff-assisted onboarding: staff guides prospect through checkout and initiates payment on their behalf
- Personalisation Team: views contribution intent status on lead record to track conversion

### 4.4 Existing Flows to Preserve

- `/smartlife-checkout-demo` currently renders a checkout page with `simulate_payment` API call. Do not remove this. Enhance around it.
- The existing `payment_completed` journey flag on SmartLife Demo Lead is set by `update_journey_flag`. Do not remove.
- Phase 1 smoke test must still pass after Phase 3.

### 4.5 New DocType: SmartLife Contribution Intent

**File location:** `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_contribution_intent/`

**Files to create:**
- `smartlife_contribution_intent.json` — DocType definition
- `smartlife_contribution_intent.py` — Python controller (can be empty class initially)

#### Field-by-field table

| Field | Type | Mandatory | Validation | PII? | Audit | Downstream use |
|---|---|---|---|---|---|---|
| `lead` | Link → SmartLife Demo Lead | Yes | Must exist | No (link) | Yes | Join to lead record |
| `session_id` | Data | Yes | Non-empty | No | Yes | Anonymous session correlation |
| `saver_type` | Data | No | Copy from lead | No | No | Analytics dimension (safe) |
| `contribution_amount` | Currency | Yes | > 0 | No | Yes | Plan tracking |
| `contribution_frequency` | Select | Yes | Monthly/Weekly/Daily/Semi-annually/Annually/One-off | No | No | Plan tracking |
| `payment_method` | Select | Yes | Mobile Money/Card/Bank Transfer/Other | No | No | Pesapal channel |
| `payment_status` | Select | Yes | Draft/Checkout Started/Pending/Completed/Failed/Cancelled/Reconciled | No | Yes | State machine |
| `payment_reference` | Data | No | Internal only | **PII — never analytics, never public** | Yes | Reconciliation |
| `checkout_started_on` | Datetime | No | Auto-set | No | Yes | Funnel analytics |
| `payment_completed_on` | Datetime | No | Auto-set | No | Yes | Conversion analytics |
| `pesapal_tracking_id` | Data | No | From Pesapal response | No | Yes | Pesapal correlation |
| `pesapal_merchant_reference` | Data | No | Merchant-generated | No | Yes | Reconciliation |
| `callback_status` | Data | No | Raw Pesapal callback code | No | Yes | Debug |
| `ipn_status` | Data | No | Raw IPN verification status | No | Yes | Reconciliation |
| `reconciliation_status` | Select | No | Pending/Matched/Discrepancy/Reconciled | No | Yes | Finance ops |
| `created_by_channel` | Select | No | Self-serve/Staff-assisted/Other | No | No | Analytics |
| `demo_mode` | Check | Yes | Default 1 | No | Yes | Always 1 in prototype |
| `failure_reason` | Data | No | Human-readable | No | Yes | Support |

#### Status lifecycle

```
Draft
  → Checkout Started  (when initiate_pesapal_checkout called)
  → Pending           (when Pesapal IPN received, payment processing)
  → Completed         (when Pesapal confirms successful payment)
  → Failed            (when Pesapal reports failure)
  → Cancelled         (when user cancels)
  → Reconciled        (when finance team reconciles)
```

#### Permissions model

| Role | Read | Write | Notes |
|---|---|---|---|
| Guest | No | Via `create_payment_intent` and callbacks only | No direct DocType access |
| SmartLife Personalisation Team | Yes | Yes | Via `get_contribution_intent` API |
| NSSF Staff | Yes | Yes | |
| System Manager | Yes | Yes | |

### 4.6 API Inventory — Phase 3

#### `create_payment_intent(session_id, amount, frequency, payment_method)`

- **Access:** `allow_guest=True`
- **Purpose:** Creates a `SmartLife Contribution Intent` record at checkout start
- **Request:** `session_id` (string), `amount` (float), `frequency` (string), `payment_method` (string)
- **Response success:** `{"success": true, "intent_name": "SCINT-00001", "session_id": "..."}`
- **Response failure:** `{"success": false, "message": "Session not found"}` — never traceback
- **Side effects:** Sets `payment_status = Draft`, copies `saver_type` from lead, links lead
- **Error cases:** Lead not found by session_id → return success=false with message; database error → log to SmartLife Integration Event, return success=false
- **PII exposure:** None — returns intent_name and session_id only

#### `initiate_pesapal_checkout(intent_name)`

- **Access:** `allow_guest=True`
- **Purpose:** Calls Pesapal API to create order, returns redirect URL
- **Request:** `intent_name` (string)
- **Response success:** `{"success": true, "redirect_url": "https://pay.pesapal.com/...", "tracking_id": "..."}`
- **Response demo fallback:** `{"success": false, "demo_mode": true, "message": "Sandbox credentials not configured — demo fallback active", "simulated_redirect_url": "/smartlife-thank-you?status=simulated"}`
- **Side effects:** Updates intent `payment_status = Checkout Started`, stores `pesapal_tracking_id`
- **Error cases:** Credentials missing → demo fallback (never traceback); Pesapal API error → log to SmartLife Integration Event, return structured error
- **PII exposure:** None — redirect URL only

#### `handle_pesapal_callback(OrderTrackingId, OrderMerchantReference)`

- **Access:** `allow_guest=True` (Pesapal redirects user browser to this endpoint after payment)
- **Purpose:** Receives Pesapal redirect, updates callback_status, redirects user to thank-you page
- **Request:** Pesapal GET parameters `OrderTrackingId`, `OrderMerchantReference`
- **Response:** HTTP redirect to `/smartlife-thank-you?status=pending` or `/smartlife-thank-you?status=unknown`
- **Side effects:** Updates `callback_status` on intent
- **Error cases:** Intent not found → redirect to `/smartlife-thank-you?status=unknown`; never show traceback
- **PII exposure:** None — never put name/phone/email in redirect URL

#### `handle_pesapal_ipn(OrderTrackingId, OrderMerchantReference, OrderNotificationType)`

- **Access:** `allow_guest=True` (Pesapal posts server-to-server to this endpoint)
- **Purpose:** Receives IPN, verifies payment with Pesapal API, updates payment_status
- **Request:** POST from Pesapal servers
- **Response:** Must return HTTP 200 to Pesapal regardless of internal outcome
- **Side effects:** Calls `verify_payment_status`, updates `ipn_status`, updates `payment_status` to Completed/Failed
- **Error cases:** Any internal error must be caught, logged to SmartLife Integration Event, and HTTP 200 returned to Pesapal. Never return 5xx to Pesapal.
- **PII exposure:** None

#### `verify_payment_status(intent_name)`

- **Access:** `@frappe.whitelist()` — authenticated staff only (not allow_guest)
- **Purpose:** Queries Pesapal API for current payment status of an intent
- **Request:** `intent_name` (string)
- **Response:** `{"status": "Completed", "pesapal_status": "...", "updated": true}`
- **Side effects:** Updates `payment_status` on intent if changed
- **Error cases:** Credentials missing → return simulated Completed in demo mode; API failure → return current DB status
- **PII exposure:** None

#### `get_contribution_intent(intent_name)`

- **Access:** `@frappe.whitelist()` — authenticated staff; full payment_reference field requires `_require_personalisation_access()`
- **Purpose:** Returns contribution intent details for staff view
- **Request:** `intent_name` (string)
- **Response:** All intent fields (see DocType table). `payment_reference` is masked for non-personalisation staff.
- **Error cases:** Not found → return structured error; permission denied → `frappe.throw` with PermissionError
- **PII exposure:** `payment_reference` is internal PII — mask in list views; expose only in full PII staff view

### 4.7 Pesapal Integration Design

**Adapter file:** `integrations/pesapal_adapter.py` (stub exists — Phase 3 activates it)

**Credential location:** `frappe.conf` keys (to confirm exact key names from existing adapter):
- Sandbox: `to confirm from existing pesapal_adapter.py`
- Never commit actual values

**Sandbox credential requirements:** Human operator must configure Pesapal sandbox credentials in Frappe site config before end-to-end checkout testing. Anti-Gravity can implement and test with demo fallback without credentials.

**Demo fallback rule:** If `frappe.conf.get("pesapal_consumer_key")` is absent or empty, all Pesapal calls return a simulated success with `demo_mode=true`. The user never sees a traceback.

**IPN signature validation:** Pesapal IPN payloads must be validated. Check existing `pesapal_adapter.py` for validation logic — do not bypass.

### 4.8 Checkout UX Enhancements

File: `nssf_smart_savers/www/smartlife-checkout-demo.html`

**Add (do not remove existing content):**
- Plan summary card: saver type, goal, goal label, target amount, years to goal
- Contribution details section: amount (UGX), frequency, payment method selector
- Projection summary: maturity value from `get_projection`
- Sandbox/prototype notice: "This is a demo environment. No real payment will be processed." — always visible, never hideable
- Payment status display: updates after callback
- Continue/Retry button: enabled on Completed, retry option on Failed
- Demo fallback notice: shown when Pesapal credentials are absent

### 4.9 Backend Files Affected

| File | Change |
|---|---|
| `api.py` | Append 6 new endpoints — do not modify existing |
| `integrations/pesapal_adapter.py` | Activate sandbox implementation |
| `www/smartlife-checkout-demo.html` | Enhance UX (add, do not remove) |
| `www/smartlife-checkout-demo.py` | May need session_id context |
| `nssf_smart_savers/doctype/smartlife_contribution_intent/` | New — create both files |

### 4.10 Migration Commands

```bash
# Run on server after Phase 3 DocType creation
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload
```

### 4.11 Smoke Test Requirements

Script: `scripts/smoke_test_phase_3.sh`

Must verify:
- Phase 1 and Phase 2 smoke tests pass (baseline)
- `smartlife_contribution_intent.json` DocType exists
- Required fields present: `lead`, `session_id`, `payment_status`, `demo_mode`, `pesapal_tracking_id`
- All 6 APIs defined in `api.py`: `create_payment_intent`, `initiate_pesapal_checkout`, `handle_pesapal_callback`, `handle_pesapal_ipn`, `verify_payment_status`, `get_contribution_intent`
- `verify_payment_status` is NOT `allow_guest=True`
- `get_contribution_intent` is NOT `allow_guest=True`
- `handle_pesapal_ipn` IS `allow_guest=True`
- `handle_pesapal_callback` IS `allow_guest=True`
- `pesapal_adapter.py` exists and compiles
- No live Pesapal credentials in source (`PESAPAL_SECRET`, `sk_live`, etc.)
- Checkout HTML contains sandbox notice text
- `payment_reference` not in `ALLOWED_PARAMS`
- All Phase 3 Python files compile
- `/smartlife-checkout-demo` returns HTTP 200 (warn if network unavailable)

### 4.12 Acceptance Criteria

- SmartLife Contribution Intent DocType JSON exists with all 18 fields
- All 6 Phase 3 APIs are defined and not `allow_guest` where specified
- Checkout page renders with sandbox notice — never a traceback
- Demo fallback fires when Pesapal credentials are absent
- Phase 1 smoke test: ≥140 passed, 0 failed
- Phase 2 smoke test: ≥99 passed, 0 failed
- Phase 3 smoke test: 0 failed

### 4.13 Stop Conditions

- Stop after Phase 3 smoke test passes
- Do not start Phase 4 without human confirmation
- If Phase 1 or Phase 2 smoke test fails after Phase 3 implementation, stop and fix the regression

### 4.14 Regression Checks

After Phase 3, verify:
- `/smartlife-flexi-demo` still returns 200
- `/smartlife-self-serve` still accepts `submit_demo_lead`
- `get_staff_queue` still returns masked queue
- `get_staff_queue_full` still requires approved role
- Lead scoring still works via `score_lead`

### 4.15 Risks and Mitigations

| Risk | Mitigation |
|---|---|
| IPN endpoint must return HTTP 200 always | Wrap entire IPN handler in try/except; log errors internally |
| Payment reference is PII | Never add to ALLOWED_PARAMS; mask in all list views |
| Pesapal callback URL must be configured in Pesapal dashboard | Human operator configures callback URL in Pesapal sandbox account |
| bench migrate may fail if DocType JSON is malformed | Validate JSON before committing; check Frappe DocType schema |
| Checkout enhancements may break existing `simulate_payment` flow | Test existing flow after enhancements |

---

## SECTION 5 — Phase 4 Full Execution Detail: Communications and Personalisation

### 5.1 Phase Objective

Build consent-gated lifecycle messaging across SMS (Phahapa) and email (ZeptoMail) channels, with WhatsApp copy ready but API not connected unless explicitly configured. Create an audit log for every outbound communication attempt. Integrate "Send message" action into the staff queue view.

### 5.2 Business Purpose

NSSF's Personalisation Team needs to send timely, relevant messages to prospects at key lifecycle moments: welcome, abandoned checkout reminder, birthday, dormancy reactivation, diaspora-specific follow-up, and informal sector follow-up. All sends must be consent-gated and fully auditable.

### 5.3 User Journeys Affected

- Personalisation Team staff: views lead, selects template, previews message, sends via SMS or email
- Automated triggers (future): send on lifecycle stage change (implementation of trigger scheduling is out of scope for Phase 4 unless spec explicitly includes it — confirm from spec)
- Lead: receives SMS or email; no UI change for lead-facing routes
- Staff-assisted onboarding: staff may trigger welcome message on behalf of prospect

### 5.4 Existing Flows to Preserve

- All Phase 1–3 routes and APIs unchanged
- `send_demo_message` is new — do not replace any existing `request_support` or `submit_demo_lead` functions
- `SmartLife Demo Notification` DocType exists as a stub — Phase 4 may use it or create `SmartLife Communication Log` separately; use `SmartLife Communication Log` as the authoritative Phase 4 DocType per spec

### 5.5 Communication Channels

| Channel | Provider | Adapter file | Status |
|---|---|---|---|
| SMS | Phahapa | `integrations/phahapa_sms_adapter.py` | Stub — Phase 4 activates |
| Email | ZeptoMail | `integrations/zeptomail_adapter.py` | Stub — Phase 4 activates |
| WhatsApp | TBD | None | Copy only — no API unless explicitly configured |

### 5.6 Message Template Table

All 11 templates required. Store in `SmartLife Personalisation Rule` DocType or a static Python dict/file — confirm from existing `SmartLife Personalisation Rule` stub structure.

| Template Name | Channel | Trigger Stage | Consent Required | Segment |
|---|---|---|---|---|
| `welcome_personal_details` | SMS + Email | Personal Details Captured | Yes | All |
| `projection_viewed_reminder` | SMS | Projection Viewed (no checkout after 24h) | Yes | All |
| `checkout_abandoned_reminder` | SMS + Email | Checkout Started (no payment after 2h) | Yes | All |
| `initial_deposit_reminder` | Email | Payment Pending (after 48h) | Yes | All |
| `birthday_message` | SMS | birthday_day = today | Yes | All |
| `staff_followup_message` | SMS | Staff Follow-up Required | Yes | All |
| `savings_milestone_message` | SMS + Email | Payment Completed | Yes | All |
| `dormant_lead_reactivation` | SMS + Email | Dormant (after 30 days) | Yes | All |
| `consent_education_content` | Email | No consent — education only | **No — educational send only** | No-consent leads |
| `diaspora_saver_followup` | Email | Any | Yes | segment = diaspora_ugandan |
| `informal_sector_followup` | SMS | Any | Yes | segment = informal_sector |

#### Template field structure (per template)

```python
{
    "template_name": "welcome_personal_details",
    "channel": ["SMS", "Email"],
    "subject": "Welcome to NSSF SmartLife Flexi",  # email only
    "body_sms": "Dear {first_name}, welcome to SmartLife Flexi...",
    "body_email": "Dear {first_name},\n\nThank you for...",
    "placeholders": ["first_name", "goal_label", "saver_type_label"],
    "trigger_stage": "Personal Details Captured",
    "consent_required": True
}
```

#### Template placeholder rules

**Allowed:** `{first_name}`, `{goal_label}`, `{contribution_amount}`, `{frequency}`, `{next_follow_up_on}`, `{saver_type_label}`

**Never use:** `{email}`, `{phone}`, `{nin}`, `{dob}`, `{age}`, `{primary_phone}`, `{date_of_birth}`, `{birthday_day}`, `{birthday_month}`

### 5.7 Consent Rules (enforced in code, not just policy)

Before any outbound send, ALL conditions must be true:
1. `consent_to_contact = true` on the lead record
2. `preferred_contact_channel` is set and matches the send channel
3. The contact field exists: `primary_phone` for SMS, `email_address` for email
4. The send is logged to `SmartLife Communication Log` before and after

If any condition fails:
- Log failure to `SmartLife Communication Log` with `message_status = Failed`, `failure_reason = "Consent not given"` or similar
- Return structured error — never raise to browser
- Never silently drop without logging

**Special case — `consent_education_content`:** This template is for leads with `consent_to_contact = false`. It must not include a commercial ask. It is educational content only. Anti-Gravity must implement this template with a consent_required=False flag and separate handling logic.

### 5.8 New DocType: SmartLife Communication Log

**File location:** `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_communication_log/`

#### Field-by-field table

| Field | Type | Mandatory | PII? | Notes |
|---|---|---|---|---|
| `lead` | Link → SmartLife Demo Lead | Yes | No | Link |
| `channel` | Select | Yes | No | SMS, Email, WhatsApp |
| `template_name` | Data | Yes | No | Template identifier |
| `recipient_masked` | Data | Yes | **Masked only** | `070****545` or `ro***@domain.com` — never raw |
| `message_status` | Select | Yes | No | Draft/Sent/Delivered/Failed/Simulated |
| `provider` | Data | No | No | phahapa, zeptomail |
| `provider_reference` | Data | No | No | Provider message ID |
| `sent_on` | Datetime | No | No | Auto-set |
| `failure_reason` | Data | No | No | |
| `consent_snapshot` | Check | Yes | No | Value of consent_to_contact at send time |
| `staff_owner` | Data | No | No | Staff user who triggered |
| `triggered_by_stage` | Data | No | No | Lead stage at trigger |
| `demo_mode` | Check | Yes | No | Always 1 in prototype |

**Critical rule:** `recipient_masked` stores masked value only. Raw phone/email must never appear in this field. Masking logic: phone `070****545` (first 3, asterisks, last 3); email `ro***@domain.com` (first 2 chars, asterisks, @domain).

#### Permissions model

| Role | Read | Write | Notes |
|---|---|---|---|
| Guest | No | No | No direct access |
| SmartLife Personalisation Team | Yes | Via APIs only | |
| NSSF Staff | Yes | Via APIs only | |
| System Manager | Yes | Yes | |

### 5.9 API Inventory — Phase 4

#### `get_message_templates(channel=None)`

- **Access:** `allow_guest=True`
- **Purpose:** Returns template list (metadata only — no lead PII)
- **Request:** Optional `channel` filter (SMS/Email/WhatsApp)
- **Response:** `{"templates": [{"template_name": "...", "channel": [...], "trigger_stage": "..."}]}`
- **PII exposure:** None

#### `preview_message(template_name, session_id)`

- **Access:** `@frappe.whitelist()` — staff only
- **Purpose:** Renders personalised message body for staff to review before send
- **Request:** `template_name`, `session_id` (resolves to lead)
- **Response:** `{"body": "Dear Jane, welcome to SmartLife Flexi...", "channel": "SMS"}`
- **PII exposure:** Yes — first_name in preview body. Staff access only. Role guard via standard authenticated check. Full PII preview requires `_require_personalisation_access()`.
- **Error cases:** Lead not found → return error; template not found → return error

#### `send_demo_message(lead_name, template_name, channel)`

- **Access:** `@frappe.whitelist()` — requires `_require_personalisation_access()`
- **Purpose:** Sends message via provider; creates Communication Log
- **Request:** `lead_name`, `template_name`, `channel`
- **Response:** `{"success": true, "log_name": "SCOMLOG-00001", "status": "Sent"}`
- **Demo fallback:** If provider credentials missing → log as `demo_mode=true`, `message_status=Simulated`
- **Consent gate:** Check `consent_to_contact` before sending; log and abort if not consented
- **Error cases:** Consent not given → log + return structured error; provider error → log + return structured error; never traceback

#### `log_communication(lead_name, channel, template_name, message_status, provider_reference=None, failure_reason=None)`

- **Access:** `@frappe.whitelist()` — internal
- **Purpose:** Creates Communication Log record
- **Request:** As listed in signature
- **Response:** `{"log_name": "SCOMLOG-00001"}`
- **Side effects:** Creates SmartLife Communication Log record with masked recipient

#### `get_communication_history(lead_name, limit=20)`

- **Access:** `@frappe.whitelist()` — requires `_require_personalisation_access()`
- **Purpose:** Returns communication history for a lead
- **Request:** `lead_name`, optional `limit`
- **Response:** `{"history": [{"template_name": "...", "channel": "...", "recipient_masked": "070****545", "message_status": "Sent", "sent_on": "..."}]}`
- **PII exposure:** `recipient_masked` only — never raw phone/email

### 5.10 Provider Credential Requirements

| Provider | Config key (to confirm from adapter) | Where | Who |
|---|---|---|---|
| Phahapa SMS | `to confirm from phahapa_sms_adapter.py` | `frappe.conf` or env var | Human operator |
| ZeptoMail | `to confirm from zeptomail_adapter.py` | `frappe.conf` or env var | Human operator |

If credentials are absent, all sends return `demo_mode=true`, `message_status=Simulated`. No error raised to user.

### 5.11 Diaspora and Informal Sector Considerations

- **Diaspora leads** (`segment = diaspora_ugandan`): prefer email. Phahapa SMS may not reach international numbers. Use `diaspora_saver_followup` email template.
- **Informal sector leads** (`segment = informal_sector`): prefer SMS. Lower email engagement expected. Use `informal_sector_followup` SMS template.
- Template routing logic must check `segment` and `preferred_contact_channel` before send.

### 5.12 Migration Commands

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload
```

### 5.13 Smoke Test Requirements

Script: `scripts/smoke_test_phase_4.sh`

Must verify:
- Phase 1, 2, 3 smoke tests pass (baseline)
- `smartlife_communication_log.json` DocType exists
- Required fields: `lead`, `channel`, `recipient_masked`, `consent_snapshot`, `demo_mode`
- Template store exists with at least `welcome_personal_details` and `checkout_abandoned_reminder`
- All 5 APIs defined: `get_message_templates`, `preview_message`, `send_demo_message`, `log_communication`, `get_communication_history`
- `send_demo_message` is NOT `allow_guest=True`
- `preview_message` is NOT `allow_guest=True`
- `get_communication_history` is NOT `allow_guest=True`
- `send_demo_message` calls `_require_personalisation_access`
- `send_demo_message` checks `consent_to_contact` before send
- `recipient_masked` field exists in Communication Log (not `recipient` or `phone`)
- No Phahapa API key committed
- No ZeptoMail API key committed
- All Phase 4 Python files compile
- `/smartlife-staff-queue-full` returns HTTP 200 (warn if network unavailable)

### 5.14 Acceptance Criteria

- SmartLife Communication Log DocType with all 13 fields
- All 11 templates defined
- All 5 APIs defined with correct access guards
- No send without consent (enforced in code)
- Demo fallback fires when credentials absent
- Phase 1–4 smoke tests: 0 failed

### 5.15 Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Birthday trigger needs scheduled task | Phase 4 builds the send function; scheduled task setup is a production item (document in Phase 8) |
| Over-sending (multiple sends to same lead) | Communication Log allows deduplication check before send |
| consent_education_content sent to consented leads | Implement separate logic flag; never send as a standard template |
| Raw PII in Communication Log | Enforce masking in `log_communication` before storing recipient |

---

## SECTION 6 — Phase 5 Full Execution Detail: Command Centre and Analytics

### 6.1 Phase Objective

Create `/smartlife-command-centre` — a management-facing analytics dashboard showing aggregate programme metrics with zero raw PII. Authentication-gated (any signed-in staff). No new DocTypes.

### 6.2 Business Purpose

NSSF programme managers and senior leadership need a live view of SmartLife Flexi onboarding performance: how many leads are in the funnel, where they drop off, what the conversion rate is, and which segments and campaigns are performing. All data is aggregate — no individual member data is displayed.

### 6.3 Why Aggregate-Only Matters

The Command Centre is the single place where NSSF leadership views programme health. If individual records appeared here, it would become a second full-PII access point, bypassing the role guard on `/smartlife-staff-queue-full`. Aggregate-only enforces the principle that management analytics are separated from operational PII access.

### 6.4 New Route

| Item | Detail |
|---|---|
| Route | `/smartlife-command-centre` |
| HTML file | `nssf_smart_savers/www/smartlife-command-centre.html` |
| Python file | `nssf_smart_savers/www/smartlife-command-centre.py` |
| Access | Authentication required — guest sees sign-in gate |
| PII | None — aggregate only |

**Python controller pattern (same as `smartlife-staff-queue-full.py`):**
```python
def get_context(context):
    context.title = "SmartLife Command Centre"
    context.is_demo = True
    context.no_breadcrumbs = True
    context.is_guest = frappe.session.user == "Guest"
    # Any authenticated user can view aggregates — no role check needed
    context.is_authenticated = not context.is_guest
```

### 6.5 Dashboard Sections and Metrics

#### Summary strip

| Metric | Formula | Data source |
|---|---|---|
| Total Leads | COUNT all SmartLife Demo Lead | SmartLife Demo Lead |
| Personal Details Completed | COUNT WHERE lead_status IN ('Personal Details Captured', ...) | SmartLife Demo Lead |
| Projections Viewed | COUNT WHERE projection_viewed = 1 | SmartLife Demo Lead |
| Checkout Started | COUNT WHERE checkout_started = 1 | SmartLife Demo Lead |
| Payment Pending | COUNT WHERE lead_status = 'Payment Pending' | SmartLife Demo Lead |
| Payment Completed | COUNT WHERE payment_completed = 1 | SmartLife Demo Lead |
| Conversion Rate | (Payment Completed / Total Leads) × 100 | Computed |

#### Follow-up queue summary

| Metric | Formula |
|---|---|
| Staff Follow-up Required | COUNT WHERE lead_status = 'Staff Follow-up Required' |
| Unassigned | COUNT WHERE assigned_staff IS NULL AND lead_status = 'Staff Follow-up Required' |
| Overdue | COUNT WHERE next_follow_up_on < today AND lead_status NOT IN ('Converted', 'Closed') |

#### Distribution sections (aggregate counts only)

- Leads by saver type (`segment` field)
- Leads by savings goal (`goal` field)
- Leads by age band (`age_band` field — safe dimension)
- Leads by preferred contact channel
- Lead temperature distribution (Hot/Warm/Cold counts)
- Birthday month distribution (count per month 1–12 — never individual birthday)
- Campaign source performance (count per `campaign_source`)
- Contribution intent summary (if Phase 3 deployed): total intents, completed, pending, failed

#### Funnel section

Stage order: Goal Selected → Personal Details → Projection → Checkout → Payment  
For each stage: count and percentage of total leads

### 6.6 API Inventory — Phase 5

All Phase 5 APIs are `@frappe.whitelist()` (not `allow_guest`). All return aggregates only.

#### `get_command_centre_summary()`

- **Returns:** `{total, personal_details, projections_viewed, checkout_started, payment_pending, payment_completed, conversion_rate, staff_followup_required, unassigned, overdue}`
- **PII:** None

#### `get_conversion_funnel()`

- **Returns:** `{stages: [{stage: "Goal Selected", count: 120, pct_of_total: 100}, ...]}`
- **PII:** None

#### `get_dropoff_by_stage()`

- **Returns:** `{by_stage: {"Goal Selected": 10, "Projection Viewed": 22, ...}}`
- **PII:** None

#### `get_lead_distribution(dimension)`

- **Allowed dimensions:** `segment`, `goal`, `age_band`, `preferred_contact_channel`, `lead_temperature`, `gender`, `country`, `frequency`
- **Rejected dimensions:** Must reject `first_name`, `email`, `primary_phone`, `nin`, `date_of_birth` — return error if requested
- **Returns:** `{dimension: "segment", distribution: {"self_employed": 42, "salaried": 31, ...}}`
- **PII:** None — dimension values are safe analytics dimensions only

#### `get_campaign_performance()`

- **Returns:** `{by_source: {"google": 40, "facebook": 20}, by_medium: {"cpc": 35, "organic": 25}}`
- **PII:** None

#### `get_birth_month_distribution()`

- **Returns:** `{months: {"1": 8, "2": 12, ..., "12": 5}}`
- **PII:** None — month count only, never individual birthday or birthday_day

### 6.7 Access and PII Model

- Guest → sees "Staff sign-in required" gate with login link. No data rendered.
- Any authenticated user → full aggregate dashboard. No PII in aggregate data so no role check needed beyond authentication.
- The dashboard never queries or returns: `first_name`, `last_name`, `primary_phone`, `email_address`, `nin`, `date_of_birth`, `birthday_day`, individual `birthday_month` values, `staff_notes`, or `payment_reference`.

### 6.8 No Migration Required

Phase 5 reads from existing DocTypes. No new DocType. No `bench migrate` needed.

### 6.9 Smoke Test Requirements

Script: `scripts/smoke_test_phase_5.sh`

Must verify:
- Phase 1–4 smoke tests pass (baseline)
- `smartlife-command-centre.html` exists
- `smartlife-command-centre.py` exists
- Route HTML contains brand shell include
- Route HTML contains guest gate logic
- All 6 APIs defined: `get_command_centre_summary`, `get_conversion_funnel`, `get_dropoff_by_stage`, `get_lead_distribution`, `get_campaign_performance`, `get_birth_month_distribution`
- All 6 APIs are NOT `allow_guest=True`
- `get_birth_month_distribution` does NOT return `birthday_day` or `primary_phone` (inspect function body)
- `get_lead_distribution` does NOT allow `first_name` or `email` as dimension
- No new PII added to `ALLOWED_PARAMS`
- `analytics_helper.js` PII_KEYS unchanged
- All Phase 5 Python files compile
- `/smartlife-command-centre` returns HTTP 200 (warn if network unavailable)

### 6.10 Acceptance Criteria

- Route renders with guest gate for unauthenticated users
- All 6 aggregate APIs defined and not `allow_guest`
- No individual records in any API response
- Birthday distribution returns month counts only
- Phase 1–5 smoke tests: 0 failed

### 6.11 Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `get_lead_distribution` called with PII dimension | Validate dimension against allowlist in function body; reject unknown dimensions |
| Birthday month data indirectly identifies individuals | Aggregate counts only; minimum group size not enforced in prototype but document as production consideration |
| Command Centre performance on large datasets | Use Frappe `frappe.db.count()` and `frappe.db.sql()` with GROUP BY — not Python loops |

---

## SECTION 7 — Phase 6 Full Execution Detail: Support and Helpdesk

### 7.1 Phase Objective

Replace the basic `/smartlife-support-demo` placeholder with a structured support request form and staff assignment workflow. Create `SmartLife Support Request` DocType.

### 7.2 Business Purpose

Prospects who get stuck during onboarding need a way to request help without abandoning the journey. Staff need to track, assign, and resolve support requests. The system must link support requests to leads to provide context for follow-up.

### 7.3 New DocType: SmartLife Support Request

**File location:** `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_support_request/`

#### Field-by-field table

| Field | Type | Mandatory | PII? | Notes |
|---|---|---|---|---|
| `lead` | Link → SmartLife Demo Lead | No | No | Optional link via session_id lookup |
| `session_id` | Data | Yes | No | Anonymous session ID |
| `support_category` | Select | Yes | No | One of 7 categories |
| `preferred_contact_channel` | Select | No | No | SMS, Email, Phone call |
| `message` | Small Text | No | **Sanitised** | Max 500 chars; run through `sanitise_demo_text()` before storage |
| `status` | Select | Yes | No | New/Assigned/In Progress/Resolved/Closed |
| `assigned_staff` | Data | No | No | Staff name |
| `created_on` | Datetime | Yes | No | Auto-set |
| `resolved_on` | Datetime | No | No | |
| `resolution_notes` | Small Text | No | **Internal only** | Never returned in public API |
| `consent_snapshot` | Check | Yes | No | consent_to_contact at time of request |
| `demo_mode` | Check | Yes | No | Always 1 in prototype |

#### 7 Support Categories

| Category | Purpose |
|---|---|
| I need help joining SmartLife Flexi | General onboarding help |
| I need help understanding projections | Projection calculator confusion |
| I need help making a contribution | Payment/checkout help |
| I am already an NSSF member | Existing member reconciliation |
| I am in the diaspora | Diaspora-specific flow |
| I want staff to call me | Callback request |
| Other | Catch-all |

#### Status lifecycle

```
New → Assigned → In Progress → Resolved → Closed
```

#### Priority model

No automated priority in Phase 6. Staff assign based on category. Escalation is manual. Document as a production enhancement.

#### Permissions model

| Role | Read | Write | Notes |
|---|---|---|---|
| Guest | No | Via `create_support_request` only | No direct DocType access |
| SmartLife Personalisation Team | Yes | Via APIs | |
| NSSF Staff | Yes | Via APIs | |
| System Manager | Yes | Yes | |

### 7.4 Form Enhancements to `/smartlife-support-demo`

Replace placeholder support form with:
- Support category (radio or select — required)
- Message textarea (max 500 chars — optional)
- Preferred contact channel (optional)
- Session ID (hidden — pre-filled from URL/localStorage)
- Submit button → calls `create_support_request`
- Success state: shows reference number (`SSREQ-XXXXX`)
- Failure state: shows retry message — never traceback
- Anonymous: no name/email required at this stage

### 7.5 API Inventory — Phase 6

#### `create_support_request(session_id, support_category, message, preferred_contact_channel="")`

- **Access:** `allow_guest=True`
- **Purpose:** Creates SmartLife Support Request from public form
- **Request:** As listed in signature
- **Response success:** `{"success": true, "request_name": "SSREQ-00001"}`
- **Side effects:** Sanitises message with `sanitise_demo_text(message, 500)`; checks PII with `_check_pii(message)`; looks up lead by session_id and links if found; sets `consent_snapshot` from lead
- **Error cases:** Never traceback; invalid category → structured error; PII detected in message → sanitise or reject
- **PII exposure:** None — returns reference only

#### `get_support_requests(status=None, limit=50)`

- **Access:** `@frappe.whitelist()` — authenticated staff
- **Purpose:** Returns paginated support queue for staff
- **Request:** Optional `status` filter, optional `limit`
- **Response:** `{"requests": [{"name": "SSREQ-00001", "support_category": "...", "status": "New", "assigned_staff": null, "created_on": "..."}]}`
- **PII exposure:** None — no raw message, no resolution_notes, no phone/email

#### `assign_support_request(request_name, staff_name)`

- **Access:** `@frappe.whitelist()` — requires `_require_authenticated_staff()`
- **Purpose:** Assigns staff to request, sets status to Assigned
- **Request:** `request_name`, `staff_name`
- **Response:** `{"success": true}`
- **Side effects:** Sets `assigned_staff`, `status = Assigned`
- **PII exposure:** None

#### `update_support_status(request_name, new_status, resolution_notes="")`

- **Access:** `@frappe.whitelist()` — requires `_require_authenticated_staff()`
- **Purpose:** Updates status; optionally adds resolution notes (internal)
- **Request:** `request_name`, `new_status`, optional `resolution_notes`
- **Allowed statuses:** New, Assigned, In Progress, Resolved, Closed
- **Response:** `{"success": true}`
- **PII exposure:** `resolution_notes` never returned in any public response

### 7.6 Linkage to Other DocTypes

- Linked to `SmartLife Demo Lead` via `lead` field (optional — proceeds without link if session_id not found)
- `session_id` → lead lookup via `frappe.db.get_value("SmartLife Demo Lead", {"created_session_id": session_id})`
- If Phase 3 deployed: consider linking to `SmartLife Contribution Intent` if support category is payment-related (optional enhancement — only if spec supports it)
- If Phase 4 deployed: may trigger staff follow-up communication via `send_demo_message` (optional — only if spec supports it)

### 7.7 Migration Commands

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload
```

### 7.8 Smoke Test Requirements

Script: `scripts/smoke_test_phase_6.sh` (already defined in `docs/phase_6_support_helpdesk_spec.md`)

Must verify:
- Phase 1–5 smoke tests pass (baseline)
- `smartlife-support-demo.html` contains support category options
- `smartlife-support-demo.html` contains 'I need help joining SmartLife Flexi'
- `smartlife-support-demo.html` calls `create_support_request`
- SmartLife Support Request JSON exists
- Required fields: `lead`, `session_id`, `support_category`, `status`, `consent_snapshot`, `demo_mode`
- All 4 APIs defined: `create_support_request`, `get_support_requests`, `assign_support_request`, `update_support_status`
- `create_support_request` IS `allow_guest=True`
- `get_support_requests` is NOT `allow_guest=True`
- `assign_support_request` is NOT `allow_guest=True`
- `update_support_status` is NOT `allow_guest=True`
- `assign_support_request` calls `_require_authenticated_staff`
- `update_support_status` calls `_require_authenticated_staff`
- `create_support_request` calls `sanitise_demo_text`
- `resolution_notes` not returned in any public API response
- All Phase 6 Python files compile
- `/smartlife-support-demo` returns HTTP 200 (warn if network unavailable)

### 7.9 Acceptance Criteria

- SmartLife Support Request DocType with all 12 fields
- All 7 support categories in form
- All 4 APIs with correct access guards
- Message sanitised before storage
- `resolution_notes` never public
- Phase 1–6 smoke tests: 0 failed

### 7.10 Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Free-text message may contain PII | `_check_pii()` and `sanitise_demo_text()` before storage |
| Frappe Helpdesk integration may not be installed | `helpdesk_adapter.py` must silently skip if not installed |
| resolution_notes exposure | Never include in any public API return |

---

## SECTION 8 — Phase 7 Full Execution Detail: Security and Privacy Hardening

### 8.1 Phase Objective

Audit and harden the full SmartLife Flexi prototype for NSSF review and to prepare a safer production path. No new features. No new DocTypes. No new routes. Fix security gaps found during audit.

### 8.2 Business Purpose

Before NSSF presents the demo to regulators, DPO, or potential production partners, the system must pass a structured security and privacy review. Phase 7 produces `docs/security_privacy_review.md` as evidence.

### 8.3 14-Item Hardening Checklist

#### 1. CSRF handling

- Verify Frappe's built-in CSRF protection is active on all mutation endpoints
- `@frappe.whitelist()` endpoints (non-guest) require a valid CSRF token by Frappe default
- Guest endpoints (`allow_guest=True`) do not require CSRF — document this as acceptable for demo, note for production
- Document finding in `security_privacy_review.md`

#### 2. Rate limiting

- Review guest-open endpoints for abuse potential:
  - `submit_demo_lead` — max 10 per IP per hour
  - `submit_personal_details` — max 10 per IP per hour
  - `request_support` — max 5 per IP per hour
  - `create_support_request` — max 5 per IP per hour
  - `log_analytics_event` — max 100 per IP per hour
- Frappe v15 has `frappe.rate_limiter` — check if available and implement if so
- If not available in this version, document as a production TODO with Nginx rate limit recommendation

#### 3. Guest endpoint audit

For every `allow_guest=True` endpoint:
- Returns no raw PII → verify
- Runs `_check_pii()` on free-text inputs → verify
- Has no traceback path to browser → verify all are wrapped in try/except
- Sanitises free text via `sanitise_demo_text()` → verify

#### 4. Role guard audit

For every full-PII and write endpoint:
- Is NOT `allow_guest=True` → verify
- Calls `_require_authenticated_staff()` or `_require_personalisation_access()` → verify
- `_require_personalisation_access()` calls `_has_allowed_personalisation_role()` which calls `frappe.get_roles()` → verify call chain
- No "any authenticated user" bypass for full-PII data → verify

#### 5. Analytics PII block audit

- Re-verify `ALLOWED_PARAMS` in `utils/analytics.py` contains no PII keys
- Re-verify `PII_KEYS` in `analytics_helper.js` covers all required keys: `first_name`, `last_name`, `primary_phone`, `email`, `date_of_birth`, `birthday_day`, `birthday_month`, `age_years`, `nin`
- Re-verify `sanitise_event_params()` drops unlisted keys
- Document double-enforcement architecture in `security_privacy_review.md`

#### 6. Credential audit

- Scan all source files for patterns: `sk_live`, `pk_live`, `SECRET_KEY`, `PRIVATE_KEY`, `API_KEY`, `PESAPAL_`, `PHAHAPA_`, `ZEPTOMAIL_`
- Scan `.env` files if any are present
- Verify `.gitignore` excludes credential files
- Expected result: zero hits in source

#### 7. Traceback exposure

- Verify no Frappe error tracebacks visible to guest users in any route
- Verify all exception handlers return structured JSON errors, not HTML tracebacks
- Test by sending malformed requests to guest endpoints

#### 8. PII in URLs

- Audit all routes and API responses for URL patterns containing PII
- Verify thank-you page URL does not contain name, phone, email, session detail
- Verify checkout redirect does not put PII in query parameters
- Verify Pesapal callback URL does not expose raw PII

#### 9. PII in logs

- Audit `frappe.log_error` calls — verify they log document names and action types, not raw PII fields
- Verify `log_analytics_event` sanitises before storage
- Review `SmartLife Integration Event` payloads for PII leakage

#### 10. Page-level route protection

- `/smartlife-staff-queue-full`: verify guest sees clean gate, not data
- `/smartlife-command-centre`: verify guest sees clean gate
- Verify no PII visible in HTML source of any public route
- `curl` public routes and grep for phone/email/name patterns

#### 11. No live payment credentials committed

- Verify `pesapal_adapter.py` reads credentials from `frappe.conf` or env — not hardcoded
- Verify sandbox/demo fallback fires correctly when credentials absent

#### 12. Consent enforcement

- Audit `send_demo_message` and all Phase 4 communication functions for consent gate
- Verify no outbound message path bypasses `consent_to_contact` check
- Document consent enforcement in `security_privacy_review.md`

#### 13. Staff role assignment reminder

- Document in `security_privacy_review.md`: the `SmartLife Personalisation Team` role must be manually created in Frappe
- Include exact Frappe admin steps

#### 14. Data retention notes

- Document: all data is demo data, no real member data
- Production deployment requires NSSF DPO sign-off on data retention periods
- Recommend periodic purge script for demo data (implementation is a production item)

### 8.4 New Document: `docs/security_privacy_review.md`

Create this document with:
- CSRF status and findings
- Rate limiting status and gaps (including production TODO)
- Guest endpoint inventory with risk rating (Low/Medium/High)
- Role guard confirmation
- Analytics PII block confirmation
- Credential handling approach
- PII in URLs/logs status
- Consent enforcement confirmation
- Open TODOs for production

### 8.5 Smoke Test Requirements

Script: `scripts/smoke_test_phase_7.sh`

Must verify:
- Phase 1–6 smoke tests pass (baseline)
- Credential safety: no `sk_live`, `PESAPAL_SECRET`, `PHAHAPA_KEY`, `ZEPTOMAIL_TOKEN`, `SECRET_KEY` in source
- Role guard: `_require_personalisation_access` calls `_has_allowed_personalisation_role`; `_has_allowed_personalisation_role` calls `frappe.get_roles`
- `get_staff_queue_full` is not `allow_guest`
- `get_lead_full_detail` is not `allow_guest`
- ALLOWED_PARAMS contains no PII keys (Python AST check using `e.value` not `e.s`)
- PII_KEYS in `analytics_helper.js` covers: `first_name`, `last_name`, `primary_phone`, `email`, `date_of_birth`, `birthday_day`, `birthday_month`, `age_years`, `nin`
- Thank-you page HTML does not contain `primary_phone` or raw email in URL attributes
- `submit_demo_lead` calls `sanitise_demo_text` or `_check_pii`
- `request_support` calls `sanitise_demo_text`
- `create_support_request` calls `sanitise_demo_text`
- `docs/security_privacy_review.md` exists
- All Python files compile (full app)
- All public routes return HTTP 200 (warn if network unavailable)
- `/smartlife-staff-queue-full` returns 200 (guest gate rendered)
- `/smartlife-command-centre` returns 200 (guest gate rendered)

### 8.6 Acceptance Criteria

- `security_privacy_review.md` exists with all 14 items addressed
- All prior smoke tests pass
- Phase 7 smoke test passes
- No credentials in source
- No PII in analytics
- No traceback to guest users
- Human sign-off received before Phase 8

### 8.7 Stop Conditions

- Stop after Phase 7 smoke test passes
- **Do not start Phase 8 without explicit human sign-off**
- If any prior smoke test fails during Phase 7 hardening, fix the regression before declaring Phase 7 done

---

## SECTION 9 — Phase 8 Full Execution Detail: Release Pack and Production Readiness

### 9.1 Phase Objective

Create the full technical, business and demo handover package for NSSF Uganda. Documentation only — no application code changes.

### 9.2 Business Purpose

NSSF needs a complete package to: (a) hand over to their technical team; (b) present to DPO and legal for privacy sign-off; (c) use for internal staff training; (d) present to management and funders as a demo-ready system; (e) guide the production deployment team.

### 9.3 Non-Negotiables

- Do not create documents with real PII as examples
- Do not modify application code
- All documents must reflect actual current app state
- Production readiness checklist must include NSSF DPO sign-off item

### 9.4 Seven Release Documents

#### `docs/phase_2_to_8_release_notes.md`
- Audience: Technical staff
- Summary of changes per phase (2 through 8)
- New DocTypes, routes, APIs per phase
- Migration requirements per phase
- Breaking changes (none — all phases are additive)
- Known issues and limitations

#### `docs/nssf_smartlife_demo_walkthrough.md`
- Audience: NSSF product and technical stakeholders
- Full journey narrative from landing to conversion
- What each screen demonstrates
- What data is captured at each step
- How Personalisation Team uses the system
- How analytics works without PII

#### `docs/admin_user_guide.md`
- Audience: NSSF system administrators
- How to access Frappe desk
- How to view SmartLife Demo Lead records
- How to run `bench migrate` after update
- How to create roles and assign them
- How to configure Pesapal, Phahapa, ZeptoMail credentials (env vars)
- How to clear cache and restart services
- How to run smoke tests
- How to check error logs

#### `docs/staff_user_guide.md`
- Audience: NSSF Personalisation Team staff
- How to sign in to Frappe
- How to access `/smartlife-staff-queue` (masked view)
- How to access `/smartlife-staff-queue-full` (full PII — requires role)
- How to update follow-up status
- How to assign a lead
- How to send a demo message (Phase 4)
- How to view communication history
- How to access support requests
- PII handling responsibilities

#### `docs/demo_script.md`
- Audience: NSSF demo presenters
- 15-step sequence covering all phases:
  1. Landing page (`/smartlife-flexi-demo`) — goal selection, saver type, NSSF brand
  2. Self-serve onboarding (`/smartlife-self-serve`) — DOB, goal, contribution
  3. DOB-based personalisation — age band computed server-side
  4. Projection (`/smartlife-projection-demo`) — calculation, goal vs. timeline
  5. Checkout (`/smartlife-checkout-demo`) — plan summary, payment method, sandbox notice
  6. Thank-you (`/smartlife-thank-you`) — confirmation, next steps
  7. Staff-assisted flow (`/smartlife-staff-assist`) — same journey, staff controls
  8. Staff queue masked view (`/smartlife-staff-queue`) — masked contacts, lead metrics
  9. Personalisation Team full PII view (`/smartlife-staff-queue-full`) — role gate demo
  10. Contribution intent (Phase 3) — Pesapal sandbox checkout demo
  11. Communications (Phase 4) — demo message send, consent enforcement, comms log
  12. Command Centre (Phase 5) — funnel metrics, distribution charts, no PII
  13. Support flow (Phase 6) — structured support request, assignment workflow
  14. Privacy and PII protection — show `analytics_helper.js` PII block list, `ALLOWED_PARAMS`, role guard code
  15. What's next — production requirements, DPO sign-off, role setup

#### `docs/known_limitations.md`
- Demo environment — no real member data
- No live Pesapal payments without production credentials
- Rate limiting not active at app layer — must configure at Nginx/infrastructure
- WhatsApp copy-ready only — API not connected
- Role assignment is manual — no automated provisioning
- `bench migrate` required after every DocType change
- Birthday-based outreach requires scheduled task setup
- No multi-tenancy — single site deployment
- No Frappe role audit log by default — recommend enabling for production

#### `docs/production_readiness_checklist.md`
- Full checklist per Phase 8 spec (see `docs/phase_8_release_pack_spec.md` for exact items)
- Must include NSSF DPO sign-off item

### 9.5 Sign-off Matrix

| Sign-off | Who | Blocking |
|---|---|---|
| Phase 7 complete | Human operator / project lead | Blocks Phase 8 start |
| Phase 8 documentation complete | Anti-Gravity | Blocks project close |
| Technical handover | NSSF Technical Lead | Required for production |
| PII/privacy approval | NSSF DPO | Required for production |
| System integrator sign-off | System integrator | Required for production |

### 9.6 Acceptance Criteria

- All 7 documents created
- Demo script covers all 15 steps
- No real PII in any example
- Production readiness checklist includes DPO sign-off item
- All prior smoke tests pass one final time
- Human/NSSF sign-off received

---

## SECTION 10 — Consolidated API Inventory (Phases 3–8)

| Phase | API name | Access | Purpose | New PII? | DocType | Migration |
|---|---|---|---|---|---|---|
| 3 | `create_payment_intent` | `allow_guest=True` | Create Contribution Intent | No | SmartLife Contribution Intent | Yes |
| 3 | `initiate_pesapal_checkout` | `allow_guest=True` | Start Pesapal order, get redirect URL | No | SmartLife Contribution Intent | Yes |
| 3 | `handle_pesapal_callback` | `allow_guest=True` | Receive Pesapal browser redirect | No | SmartLife Contribution Intent | Yes |
| 3 | `handle_pesapal_ipn` | `allow_guest=True` | Receive Pesapal IPN (server-to-server) | No | SmartLife Contribution Intent | Yes |
| 3 | `verify_payment_status` | `@frappe.whitelist()` | Query Pesapal status | No | SmartLife Contribution Intent | Yes |
| 3 | `get_contribution_intent` | `@frappe.whitelist()` | Staff view of intent | payment_reference (internal) | SmartLife Contribution Intent | Yes |
| 4 | `get_message_templates` | `allow_guest=True` | List templates | No | SmartLife Personalisation Rule | Yes |
| 4 | `preview_message` | `@frappe.whitelist()` | Render personalised preview | first_name in preview (staff only) | SmartLife Demo Lead | — |
| 4 | `send_demo_message` | `@frappe.whitelist()` + `_require_personalisation_access()` | Send via provider | No (masked log) | SmartLife Communication Log | Yes |
| 4 | `log_communication` | `@frappe.whitelist()` | Create comms log record | No (masked) | SmartLife Communication Log | Yes |
| 4 | `get_communication_history` | `@frappe.whitelist()` + `_require_personalisation_access()` | Lead comms history | No (masked) | SmartLife Communication Log | Yes |
| 5 | `get_command_centre_summary` | `@frappe.whitelist()` | All summary counts | No | SmartLife Demo Lead | No |
| 5 | `get_conversion_funnel` | `@frappe.whitelist()` | Stage counts | No | SmartLife Demo Lead | No |
| 5 | `get_dropoff_by_stage` | `@frappe.whitelist()` | Dropoff counts | No | SmartLife Demo Lead | No |
| 5 | `get_lead_distribution` | `@frappe.whitelist()` | Distribution by safe dimension | No | SmartLife Demo Lead | No |
| 5 | `get_campaign_performance` | `@frappe.whitelist()` | Campaign counts | No | SmartLife Demo Lead | No |
| 5 | `get_birth_month_distribution` | `@frappe.whitelist()` | Month counts (not individual) | No | SmartLife Demo Lead | No |
| 6 | `create_support_request` | `allow_guest=True` | Create support request from form | No | SmartLife Support Request | Yes |
| 6 | `get_support_requests` | `@frappe.whitelist()` | Staff support queue | No | SmartLife Support Request | Yes |
| 6 | `assign_support_request` | `@frappe.whitelist()` + `_require_authenticated_staff()` | Assign staff to request | No | SmartLife Support Request | Yes |
| 6 | `update_support_status` | `@frappe.whitelist()` + `_require_authenticated_staff()` | Update status/resolution | No | SmartLife Support Request | Yes |
| 7 | (none — audit and fix only) | — | — | — | — | No |
| 8 | (none — documentation only) | — | — | — | — | No |

---

## SECTION 11 — Consolidated DocType Inventory (Phases 3–8)

### SmartLife Contribution Intent (Phase 3)

| Item | Detail |
|---|---|
| Phase | 3 |
| Purpose | Track payment lifecycle from checkout to reconciliation |
| Migration | Required |
| Linked DocTypes | SmartLife Demo Lead (via `lead` field) |
| PII fields | `payment_reference` — internal only, never analytics, never public |
| Non-PII fields | All others |
| Audit trail | payment_status changes, timestamps |

Fields: 18 — see Section 4.5 for full table.

### SmartLife Communication Log (Phase 4)

| Item | Detail |
|---|---|
| Phase | 4 |
| Purpose | Audit trail for all outbound communication attempts |
| Migration | Required |
| Linked DocTypes | SmartLife Demo Lead (via `lead` field) |
| PII fields | `recipient_masked` — stored as masked value only; never raw phone/email |
| Non-PII fields | All others |
| Audit trail | Every send attempt — pre-send and post-send |

Fields: 13 — see Section 5.8 for full table.

### SmartLife Support Request (Phase 6)

| Item | Detail |
|---|---|
| Phase | 6 |
| Purpose | Track support requests from prospects |
| Migration | Required |
| Linked DocTypes | SmartLife Demo Lead (via `lead` field, optional) |
| PII fields | `message` (sanitised before storage), `resolution_notes` (internal only) |
| Non-PII fields | All others |
| Audit trail | status changes, assignment changes |

Fields: 12 — see Section 7.3 for full table.

### Existing DocTypes (not new in Phases 3–8, may be enhanced)

| DocType | Phase | Change |
|---|---|---|
| SmartLife Demo Lead | 3–7 | No new fields in Phase 3–7 (payment_completed flag already exists in Phase 2) |
| SmartLife Demo Payment | 3 | May be superseded by SmartLife Contribution Intent — check if still needed |
| SmartLife Demo Notification | 4 | May be superseded by SmartLife Communication Log — check stub usage |
| SmartLife Personalisation Rule | 4 | Used for template storage — check existing stub fields |
| SmartLife Integration Event | 3–7 | Used for error/event logging across phases |

---

## SECTION 12 — Route and UI Touchpoint Inventory (Phases 3–8)

| Phase | Route | Current state | Enhancement | User type | Backend dependency | Regression check |
|---|---|---|---|---|---|---|
| 3 | `/smartlife-checkout-demo` | Basic checkout with `simulate_payment` | Add plan summary, contribution details, Pesapal integration, demo fallback | Public | `create_payment_intent`, `initiate_pesapal_checkout`, Pesapal adapter | Phase 1 smoke test must still pass |
| 3 | `/smartlife-thank-you` | Static thank-you page | May need status query param handling (`?status=pending`) | Public | None | Phase 1 smoke test |
| 4 | `/smartlife-staff-queue-full` | Full PII table | Add "Send message" action → calls `send_demo_message`, shows comms history | SmartLife Personalisation Team | `send_demo_message`, `get_communication_history` | Phase 2 smoke test |
| 5 | `/smartlife-command-centre` | Does not exist | Create new route — aggregate dashboard | Authenticated staff | All 6 command centre APIs | New route — must return 200 |
| 6 | `/smartlife-support-demo` | Basic placeholder form | Replace with structured 7-category support form | Public | `create_support_request` | Phase 1 smoke test |
| 7 | All routes | Existing | Audit only — no UI changes unless hardening requires | N/A | N/A | All smoke tests |
| 8 | All routes | Final state | Documentation only | N/A | N/A | All smoke tests |

---

## SECTION 13 — Credentials, Secrets and Environment Configuration

### 13.1 Pesapal

| Item | Detail |
|---|---|
| Required keys | To confirm from `integrations/pesapal_adapter.py` — expected: `pesapal_consumer_key`, `pesapal_consumer_secret`, `pesapal_ipn_id` or similar |
| Where to store | `frappe.conf` (site config) or environment variable |
| Where never to store | Source code, committed `.env` files, any tracked file |
| Sandbox vs production | Sandbox for Phase 3; production credentials require separate NSSF approval |
| Who provides | Human operator / NSSF team |
| Without credentials | Demo fallback fires; checkout renders simulated success |
| Cannot test without | End-to-end Pesapal redirect, IPN delivery, real payment status |
| Stop condition | If end-to-end payment test required, stop and wait for sandbox credentials from operator |

### 13.2 Phahapa SMS

| Item | Detail |
|---|---|
| Required keys | To confirm from `integrations/phahapa_sms_adapter.py` |
| Where to store | `frappe.conf` or environment variable |
| Where never to store | Source code |
| Without credentials | Demo fallback: `message_status = Simulated`, `demo_mode = true` |
| Cannot test without | Real SMS delivery to phone number |
| Stop condition | Phase 4 smoke tests pass without credentials (simulated); end-to-end SMS requires operator setup |

### 13.3 ZeptoMail

| Item | Detail |
|---|---|
| Required keys | To confirm from `integrations/zeptomail_adapter.py` |
| Where to store | `frappe.conf` or environment variable |
| Where never to store | Source code |
| Without credentials | Demo fallback: `message_status = Simulated`, `demo_mode = true` |
| Cannot test without | Real email delivery |
| Stop condition | Phase 4 smoke tests pass without credentials |

### 13.4 Credential audit command

```bash
grep -rEn "sk_live|pk_live|SECRET_KEY|PRIVATE_KEY|PESAPAL_SECRET|PHAHAPA_KEY|ZEPTOMAIL_TOKEN|API_KEY\s*=" \
  nssf_smart_savers/ scripts/ docs/ 2>/dev/null
# Expected: no output

git ls-files | grep -E "\.env$|credentials"
# Expected: no output
```

---

## SECTION 14 — Migration and Server Operations Plan

### 14.1 Phase-by-phase server operations

#### After Phase 3 (SmartLife Contribution Intent)

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

cd /home/frappe/frappe-bench/apps/nssf_smart_savers
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
# All must show 0 failed
```

**Expected success:** All smoke tests pass. `/smartlife-checkout-demo` returns 200.  
**Common failure symptom:** HTTP 417 on checkout route.  
**Likely cause:** `bench migrate` not run after Phase 3 DocType creation.  
**Recovery:** Run migrate command above.

#### After Phase 4 (SmartLife Communication Log)

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
```

#### After Phase 5 (no new DocType — no migrate needed)

```bash
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
bash scripts/smoke_test_phase_5.sh
```

#### After Phase 6 (SmartLife Support Request)

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
bash scripts/smoke_test_phase_5.sh
bash scripts/smoke_test_phase_6.sh
```

#### After Phase 7 (no new DocType — no migrate needed)

```bash
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
bash scripts/smoke_test_phase_5.sh
bash scripts/smoke_test_phase_6.sh
bash scripts/smoke_test_phase_7.sh
```

#### After Phase 8 (documentation only — no server changes)

Run all prior smoke tests one final time to confirm the app is in a clean state:

```bash
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
bash scripts/smoke_test_phase_5.sh
bash scripts/smoke_test_phase_6.sh
bash scripts/smoke_test_phase_7.sh
```

### 14.2 Route proof commands

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

for ROUTE in /smartlife-flexi-demo /smartlife-self-serve /smartlife-staff-assist \
             /smartlife-projection-demo /smartlife-checkout-demo \
             /smartlife-thank-you /smartlife-support-demo \
             /smartlife-staff-queue /smartlife-staff-queue-full \
             /smartlife-command-centre; do
  CODE=$(curl -ksS -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$ROUTE")
  echo "$CODE $ROUTE"
done
# Expected: all 200
```

---

## SECTION 15 — Smoke Testing and Validation Matrix

| Smoke test | Proves | When to run | Expected result | Failure meaning | Stop condition |
|---|---|---|---|---|---|
| `smoke_test.sh` | Phase 1 baseline — 7 routes, PII safety, brand shell, DOB logic | Before every phase; after every phase | ≥140 passed, 0 failed | Phase 1 regression | Stop immediately. Fix before continuing. |
| `smoke_test_phase_2.sh` | Role guard, lead scoring, staff queue, analytics safety, masked queue | Before Phase 3+; after every phase | ≥99 passed, 0 failed | Phase 2 regression | Stop immediately. Fix before continuing. |
| `smoke_test_phase_3.sh` | Contribution Intent DocType, 6 APIs, Pesapal fallback, credential safety | After Phase 3 complete | 0 failed | Phase 3 gap or regression | Stop. Do not start Phase 4. |
| `smoke_test_phase_4.sh` | Comms Log DocType, 5 APIs, consent enforcement, credential safety | After Phase 4 complete | 0 failed | Phase 4 gap or regression | Stop. Do not start Phase 5. |
| `smoke_test_phase_5.sh` | Command Centre route, 6 APIs, aggregate-only, no PII | After Phase 5 complete | 0 failed | Phase 5 gap or regression | Stop. Do not start Phase 6. |
| `smoke_test_phase_6.sh` | Support Request DocType, 4 APIs, sanitisation, access control | After Phase 6 complete | 0 failed | Phase 6 gap or regression | Stop. Do not start Phase 7. |
| `smoke_test_phase_7.sh` | Credential audit, role guard audit, PII audit, consent audit, security review doc | After Phase 7 complete | 0 failed | Security gap | Stop. Fix before human sign-off. |
| All smoke tests (Phase 8) | Full system green before release | Final run at Phase 8 end | All 0 failed | Any regression | Stop. Fix and re-run all before declaring done. |

---

## SECTION 16 — Cross-Phase Risk Register

| Risk | Phase | Likelihood | Impact | Early warning | Mitigation | Owner | Stop condition |
|---|---|---|---|---|---|---|---|
| Missing `bench migrate` after new DocType phase | 3, 4, 6 | High | High — HTTP 417 errors on new routes | 417 responses on affected routes | Human operator must run migrate after each DocType phase; Anti-Gravity must document this in acceptance format | Human operator | Stop deployment; run migrate; re-test |
| Missing `SmartLife Personalisation Team` role | 2–7 | Medium | High — full-PII view blocked for all staff | Staff reports "Access restricted" on staff-queue-full | Human operator must create role in Frappe UI; document in Phase 8 admin guide | Human operator | Not a code stop — operational issue |
| Missing Pesapal sandbox credentials | 3 | High | Medium — end-to-end checkout untestable; demo fallback covers UI | Checkout shows demo fallback notice | Implement demo fallback first; document credential requirement | Human operator | Stop end-to-end test; proceed with demo fallback |
| Missing Phahapa/ZeptoMail credentials | 4 | High | Medium — real sends untestable; simulated sends work | All sends logged as Simulated | Demo fallback; document for production | Human operator | Stop real send test; smoke test passes with Simulated |
| Network-blocked CI | 2–7 | High (cloud CI) | Low — HTTP checks warn not fail | Smoke test shows NETWORK UNAVAILABLE | Run smoke tests on server for authoritative result | Anti-Gravity | Not a code stop |
| PII exposure in new API | 3–6 | Medium | High — data breach risk | PII fields in API response | Audit every new API response shape before committing; smoke test checks | Anti-Gravity | Stop. Remove PII before committing. |
| Payment reference in analytics | 3 | Low | High | ALLOWED_PARAMS check fails | Never add `payment_reference` to ALLOWED_PARAMS | Anti-Gravity | Stop. Remove from ALLOWED_PARAMS. |
| Consent bypass in message send | 4 | Medium | High — compliance risk | Message sent without consent flag | Enforce consent check in code, not just documentation; smoke test checks | Anti-Gravity | Stop. Implement consent gate. |
| Message over-sending | 4 | Medium | Medium — prospect annoyance | Multiple Simulated entries in Comms Log for same template | Check Comms Log before send; dedup by (lead, template_name, created_on date) | Anti-Gravity | Not a stop — implement dedup |
| Command Centre exposing individual data | 5 | Low | High | Smoke test finds individual record in response | All APIs must aggregate; dimension allowlist enforced | Anti-Gravity | Stop. Remove individual records. |
| Support message containing PII | 6 | Medium | Medium | `_check_pii` not called on message | `sanitise_demo_text()` and `_check_pii()` before storage | Anti-Gravity | Stop. Add sanitisation. |
| Resolution notes exposed publicly | 6 | Low | Medium | Notes in `get_support_requests` response | Never include `resolution_notes` in public API | Anti-Gravity | Stop. Remove from response. |
| Traceback visible to guest user | 3–7 | Medium | Medium | Guest sees Frappe error page with stack trace | Wrap all guest endpoints in try/except; return structured JSON errors | Anti-Gravity | Stop. Add error handling. |
| Breaking Phase 1 onboarding flows | 3–7 | Medium | High | Phase 1 smoke test fails | Run Phase 1 smoke test before AND after each phase | Anti-Gravity | Stop. Fix regression. |
| Breaking Phase 2 staff queue or role guard | 3–7 | Low | High | Phase 2 smoke test fails | Do not modify existing API signatures or role guard logic | Anti-Gravity | Stop. Fix regression. |
| Pesapal IPN returning non-200 | 3 | Medium | High — Pesapal may stop sending IPN | Pesapal marks IPN as failed; stops retrying | IPN handler must always return HTTP 200; wrap in try/except | Anti-Gravity | Fix IPN handler before Phase 3 complete |
| Incomplete release pack | 8 | Low | Medium | Missing documents in Phase 8 | Checklist-driven; 7 documents required | Anti-Gravity | Stop. Complete all 7 documents. |

---

## SECTION 17 — Anti-Gravity Session-by-Session Instructions

### Session: Phase 3

**Read first:**
1. `docs/anti_gravity_master_prompt.md` — copy-paste at session start
2. `docs/anti_gravity_handoff.md` — architecture context
3. `docs/phase_3_payment_contribution_readiness_spec.md` — full spec
4. `docs/anti_gravity_validation_runbook.md` — exact validation commands

**Do not touch:**
- `scripts/smoke_test.sh`, `scripts/smoke_test_phase_2.sh`
- `nssf_smart_savers/api.py` existing endpoint bodies
- Any Phase 1 or Phase 2 route files
- `utils/analytics.py` ALLOWED_PARAMS
- `public/js/analytics_helper.js` PII_KEYS
- `lead_scoring.py`

**Build:**
1. `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_contribution_intent/smartlife_contribution_intent.json`
2. `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_contribution_intent/smartlife_contribution_intent.py`
3. Append 6 endpoints to `nssf_smart_savers/api.py`
4. Enhance `nssf_smart_savers/www/smartlife-checkout-demo.html`
5. Update `nssf_smart_savers/integrations/pesapal_adapter.py`
6. Create `scripts/smoke_test_phase_3.sh`

**Test:**
```bash
python3 -m compileall nssf_smart_savers -q
bash -n scripts/smoke_test_phase_3.sh
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
```

**Document:** Phase 3 acceptance format (per `docs/anti_gravity_master_prompt.md`)

**Return to human:**
```
Phase 3 complete.
Files changed: ...
DocTypes changed: SmartLife Contribution Intent: created with 18 fields
Routes added: None (checkout-demo enhanced)
APIs added: create_payment_intent, initiate_pesapal_checkout, handle_pesapal_callback, handle_pesapal_ipn, verify_payment_status, get_contribution_intent
Tests added: scripts/smoke_test_phase_3.sh: N checks
Smoke tests: Phase 1: X | Phase 2: X | Phase 3: X
Commit: <hash>
Risks: bench migrate required on server; Pesapal sandbox credentials needed for end-to-end
```

**Stop condition:** Stop after Phase 3 smoke test passes. Do not implement Phase 4.

---

### Session: Phase 4

**Read first:** `docs/phase_4_communications_personalisation_spec.md`, `docs/sms_architecture_phahapa.md`, `docs/email_architecture_zeptomail.md`

**Do not touch:** All Phase 1–3 code.

**Build:**
1. `smartlife_communication_log` DocType (JSON + Python)
2. Message template store (in `SmartLife Personalisation Rule` or static file)
3. Append 5 endpoints to `api.py`
4. Update `phahapa_sms_adapter.py` and `zeptomail_adapter.py`
5. Create `scripts/smoke_test_phase_4.sh`

**Test:** Smoke tests 1–4. All must pass.

**Stop condition:** Stop after Phase 4 smoke test passes.

---

### Session: Phase 5

**Read first:** `docs/phase_5_command_centre_analytics_spec.md`

**Do not touch:** All Phase 1–4 code.

**Build:**
1. `www/smartlife-command-centre.html`
2. `www/smartlife-command-centre.py`
3. Append 6 endpoints to `api.py`
4. Create `scripts/smoke_test_phase_5.sh`
5. No `bench migrate` needed

**Test:** Smoke tests 1–5. All must pass.

**Stop condition:** Stop after Phase 5 smoke test passes.

---

### Session: Phase 6

**Read first:** `docs/phase_6_support_helpdesk_spec.md`

**Do not touch:** All Phase 1–5 code. Do not break existing `request_support` endpoint.

**Build:**
1. `smartlife_support_request` DocType (JSON + Python)
2. Enhance `www/smartlife-support-demo.html`
3. Append 4 endpoints to `api.py`
4. Create `scripts/smoke_test_phase_6.sh`

**Test:** Smoke tests 1–6. All must pass.

**Stop condition:** Stop after Phase 6 smoke test passes.

---

### Session: Phase 7

**Read first:** `docs/phase_7_security_privacy_hardening_spec.md`, `docs/anti_gravity_handoff.md`

**Do not touch:** Do not add features. Do not modify unrelated modules. Only audit and fix.

**Build:**
1. Work through 14-item hardening checklist
2. Create `docs/security_privacy_review.md`
3. Fix any gaps found
4. Create `scripts/smoke_test_phase_7.sh`

**Test:** Smoke tests 1–7. All must pass.

**Return to human:** Full security audit findings in acceptance format. Wait for explicit human sign-off before Phase 8.

**Stop condition:** Stop after Phase 7. Do not start Phase 8 without human sign-off.

---

### Session: Phase 8

**Read first:** `docs/phase_8_release_pack_spec.md`

**Do not touch:** No application code. Documentation only.

**Build:**
1. `docs/phase_2_to_8_release_notes.md`
2. `docs/nssf_smartlife_demo_walkthrough.md`
3. `docs/admin_user_guide.md`
4. `docs/staff_user_guide.md`
5. `docs/demo_script.md`
6. `docs/known_limitations.md`
7. `docs/production_readiness_checklist.md`

**Test:** Run all prior smoke tests one final time.

**Return to human:** Phase 8 complete. Project complete pending human sign-off. List all checklist items requiring human/infrastructure action.

---

## SECTION 18 — Human/Server Operator Checklist

### Before Phase 3 starts

```
[ ] SSH to server confirmed working
[ ] git fetch origin claude/cool-bell-t7n0hs — completed
[ ] git checkout phase-1-smartlife-onboarding — completed
[ ] git merge origin/claude/cool-bell-t7n0hs — completed (no merge conflicts)
[ ] bench --site ... migrate — completed (0 errors)
[ ] bench build --app nssf_smart_savers — completed
[ ] bench --site ... clear-cache — completed
[ ] bench --site ... clear-website-cache — completed
[ ] supervisorctl restart frappe-bench-web: — completed
[ ] supervisorctl restart frappe-bench-workers: — completed
[ ] service nginx reload — completed
[ ] supervisorctl status frappe-bench-web: — all RUNNING
[ ] bash scripts/smoke_test.sh — 0 failed on server
[ ] bash scripts/smoke_test_phase_2.sh — 0 failed on server
[ ] SmartLife Personalisation Team role created in Frappe UI
[ ] Role assigned to at least one test staff user
[ ] Confirmed to Anti-Gravity: "Phase 2 merged, migrated, smoke tests pass. Start Phase 3."
```

### After Phase 3 implementation (on server)

```
[ ] Pull latest from claude/cool-bell-t7n0hs
[ ] bench migrate — completed
[ ] bench build — completed
[ ] clear-cache and clear-website-cache — completed
[ ] restart services — completed
[ ] bash scripts/smoke_test.sh — 0 failed
[ ] bash scripts/smoke_test_phase_2.sh — 0 failed
[ ] bash scripts/smoke_test_phase_3.sh — 0 failed
[ ] /smartlife-checkout-demo returns 200 and shows sandbox notice
[ ] (Optional) Configure Pesapal sandbox credentials in frappe.conf for end-to-end test
[ ] Confirmed to Anti-Gravity: "Phase 3 merged and smoke tests pass. Start Phase 4."
```

### After Phase 4 implementation (on server)

```
[ ] Pull latest
[ ] bench migrate — completed
[ ] bench build, clear-cache, restart — completed
[ ] bash scripts/smoke_test.sh through smoke_test_phase_4.sh — all 0 failed
[ ] (Optional) Configure Phahapa and ZeptoMail credentials for real send test
[ ] Confirmed to Anti-Gravity: "Phase 4 smoke tests pass. Start Phase 5."
```

### After Phase 5 implementation (on server)

```
[ ] Pull latest
[ ] bench build, clear-cache, restart — completed (no migrate needed)
[ ] bash scripts/smoke_test.sh through smoke_test_phase_5.sh — all 0 failed
[ ] /smartlife-command-centre returns 200 for authenticated user
[ ] Confirmed to Anti-Gravity: "Phase 5 smoke tests pass. Start Phase 6."
```

### After Phase 6 implementation (on server)

```
[ ] Pull latest
[ ] bench migrate — completed
[ ] bench build, clear-cache, restart — completed
[ ] bash scripts/smoke_test.sh through smoke_test_phase_6.sh — all 0 failed
[ ] /smartlife-support-demo renders structured form with 7 categories
[ ] Confirmed to Anti-Gravity: "Phase 6 smoke tests pass. Start Phase 7."
```

### After Phase 7 implementation

```
[ ] Pull latest
[ ] bench build, clear-cache, restart (no migrate)
[ ] bash scripts/smoke_test.sh through smoke_test_phase_7.sh — all 0 failed
[ ] Review docs/security_privacy_review.md
[ ] Confirm CSRF posture is acceptable
[ ] Confirm rate limiting approach
[ ] Confirm credential audit found nothing
[ ] **Explicit sign-off to Anti-Gravity: "Phase 7 accepted. Start Phase 8."**
```

### Before demo / production readiness review

```
[ ] All smoke tests pass on server
[ ] All routes return 200
[ ] SmartLife Personalisation Team role exists and assigned
[ ] No live credentials in source
[ ] NSSF Technical Lead has reviewed demo
[ ] NSSF DPO has reviewed PII handling
[ ] System integrator has reviewed deployment
[ ] production_readiness_checklist.md items addressed
```

---

## SECTION 19 — Acceptance Criteria by Phase

### Phase 3

| Category | Criteria |
|---|---|
| Functional | SmartLife Contribution Intent DocType with 18 fields; all 6 APIs defined; checkout renders sandbox notice; demo fallback fires without credentials |
| Security/privacy | No Pesapal credentials committed; payment_reference not in ALLOWED_PARAMS; IPN handler returns HTTP 200 always |
| Data | payment_status state machine correct (Draft → Completed/Failed); intent linked to lead via session_id |
| UI/route | /smartlife-checkout-demo returns 200 and shows plan summary |
| Test | Phase 1–3 smoke tests: 0 failed |
| Documentation | Phase 3 acceptance format returned to human |
| Human sign-off | Confirmation from human before Phase 4 starts |

### Phase 4

| Category | Criteria |
|---|---|
| Functional | SmartLife Communication Log DocType with 13 fields; all 11 templates defined; all 5 APIs defined; consent enforced in code |
| Security/privacy | No Phahapa/ZeptoMail credentials committed; recipient_masked never raw; no outbound without consent |
| Data | Every send attempt logged; consent_snapshot recorded; message_status reflects actual outcome |
| UI/route | Staff queue full view has "Send message" action |
| Test | Phase 1–4 smoke tests: 0 failed |
| Human sign-off | Confirmation before Phase 5 |

### Phase 5

| Category | Criteria |
|---|---|
| Functional | /smartlife-command-centre route exists; all 6 APIs aggregate-only; guest gate renders |
| Security/privacy | No individual records in any API response; birthday = month count only; dimension allowlist enforced |
| Data | Counts accurate; conversion rate correct |
| UI/route | Route returns 200; guest sees gate |
| Test | Phase 1–5 smoke tests: 0 failed |
| Human sign-off | Confirmation before Phase 6 |

### Phase 6

| Category | Criteria |
|---|---|
| Functional | SmartLife Support Request DocType with 12 fields; 7 categories in form; all 4 APIs defined; form submits and returns reference |
| Security/privacy | Message sanitised before storage; resolution_notes internal only; create_support_request is allow_guest |
| Data | Support request linked to lead if session_id found; consent_snapshot recorded |
| UI/route | /smartlife-support-demo returns 200 with structured form |
| Test | Phase 1–6 smoke tests: 0 failed |
| Human sign-off | Confirmation before Phase 7 |

### Phase 7

| Category | Criteria |
|---|---|
| Functional | All 14 hardening items reviewed and documented |
| Security/privacy | security_privacy_review.md exists; credential scan clean; role guard verified; PII audit clean; consent audit clean |
| Data | No PII in logs, URLs, or analytics |
| UI/route | Guest gate renders on all restricted routes |
| Test | Phase 1–7 smoke tests: 0 failed |
| Documentation | security_privacy_review.md complete with all sections |
| Human sign-off | **Mandatory before Phase 8 starts** |

### Phase 8

| Category | Criteria |
|---|---|
| Functional | All 7 release documents created |
| Security/privacy | No real PII in any document example |
| Data | All documents reflect actual current app state |
| UI/route | N/A — documentation only |
| Test | All prior smoke tests: 0 failed |
| Documentation | 7 documents cover all required sections; 15-step demo script complete; production checklist includes DPO sign-off |
| Human sign-off | NSSF Technical Lead + NSSF DPO + system integrator |

---

## SECTION 20 — Final Executive Summary

### What has been prepared

Phases 1 and 2 of the NSSF SmartLife Flexi platform are complete and tested. Phase 2 is on the working branch and awaits server merge and migration. Ten handover documentation files have been created to give Anti-Gravity everything needed to implement Phases 3 through 8 safely.

This execution pack expands those files into a full implementation manual covering: 21 new API endpoints, 3 new DocTypes, 2 new routes, 11 message templates, 14 security hardening items, 7 release documents, and a 15-step demo script — all specified without guessing, without starting implementation, and without modifying a single line of application code.

### What remains

Phases 3 through 8 are not started. Anti-Gravity must implement them one phase at a time, in order, with smoke tests and human confirmation at each gate.

### Why Phase 3 must not start before server sign-off

Phase 2 added fields to `SmartLife Demo Lead`. Without `bench migrate`, the live site returns HTTP 417 on Phase 2 routes. Phase 3 adds another DocType. Building Phase 3 on top of an unmigrated Phase 2 will compound the problem and make it impossible to attribute errors to the right cause. The server merge, migration, build, cache clear, restart, and smoke test sequence in Section 1.5 must complete first.

### Why one-phase-at-a-time discipline matters

Each phase depends on the previous one being stable. A bug introduced in Phase 3 that is not caught until Phase 5 is three times harder to debug. Smoke tests exist precisely to catch regressions immediately. Running all prior smoke tests before and after each phase is the only way to guarantee the baseline is clean.

### What Anti-Gravity should do next

1. Confirm this execution pack has been read
2. Wait for human sign-off that Phase 2 is merged, migrated, and smoke tests pass on the server
3. Begin Phase 3 using the implementation prompt in `docs/phase_3_payment_contribution_readiness_spec.md`
4. Run smoke tests and return Phase 3 acceptance format

### What the human/server operator must do next

1. Complete all items in the Phase 3 pre-start checklist (Section 18)
2. Confirm to Anti-Gravity when done
3. After each phase is implemented by Anti-Gravity: pull, migrate if required, build, restart, run smoke tests on server, confirm before next phase

### Biggest risks

1. **Missing bench migrate** — most common cause of 417 errors. Phases 3, 4, and 6 each add a new DocType.
2. **Missing credentials** — Phase 3 end-to-end checkout and Phase 4 real message sends require sandbox credentials. Demo fallbacks cover the gap but end-to-end testing requires human action.
3. **PII exposure in new APIs** — each new API must be audited for PII before committing. Payment reference, resolution notes, and message content must never appear in public responses.
4. **Consent bypass** — Phase 4's consent enforcement must be in code, not just documented. Any path that sends a message without checking `consent_to_contact` is a compliance failure.

### Safest path forward

- One phase per Anti-Gravity session
- Run all prior smoke tests before and after each session
- Human confirms on server before Anti-Gravity starts next phase
- Never commit credentials
- Never skip migration
- Fix regressions before proceeding

---

## SECTION 21 — Self-Review

Checking this document against the required questions:

| Question | Answer |
|---|---|
| Does it cover every phase from 3 to 8? | Yes — Sections 4–9 cover each phase in full |
| Does it give Anti-Gravity enough detail to execute without guessing? | Yes — field tables, API shapes, access rules, migration commands, smoke test requirements all specified |
| Does it avoid starting implementation? | Yes — no application code created or modified |
| Does it protect working Phase 1 and Phase 2 flows? | Yes — preservation rules in Section 2.7, regression checks in each phase section |
| Does it clearly separate human/server operator duties from Anti-Gravity duties? | Yes — Sections 1.5, 17, 18 make the distinction explicit |
| Does it identify migrations, smoke tests and stop conditions? | Yes — every phase section includes migration commands, smoke test requirements, and stop conditions |
| Does it avoid secrets? | Yes — no credentials invented or included; Section 13 documents where to store them |
| Does it protect PII? | Yes — PII classification for every DocType field; PII rules in Section 2.3; risk register entry for PII exposure |
| Does it clearly document risks? | Yes — Section 16 risk register with 16 entries |
| Does it give exact acceptance criteria? | Yes — Section 19 acceptance criteria table per phase |
| Does it avoid vague placeholders? | Yes — where exact values are not confirmed from existing code, it explicitly says "to confirm from existing adapter/spec" rather than inventing values |
