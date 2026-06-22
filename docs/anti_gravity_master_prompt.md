# Anti-Gravity Master Prompt — NSSF SmartLife Flexi

**Copy-paste this prompt at the start of every Anti-Gravity session.**

---

## Context

You are continuing work on the NSSF SmartLife Flexi demo — a Frappe v15 web application for NSSF Uganda.

- **Repository:** `sebunya/nssf_smart_savers`
- **App name:** `nssf_smart_savers`
- **Working branch:** `claude/cool-bell-t7n0hs`
- **Production branch:** `phase-1-smartlife-onboarding`
- **Site:** `https://nssf-smartlifeflexi.nile-gov-demo.com`
- **Frappe app path on server:** `/home/frappe/frappe-bench/apps/nssf_smart_savers`

## Completed work

- **Phase 1 (complete and live):** NSSF brand shell, 7 public routes, self-serve + staff-assisted onboarding, DOB-based personalisation, PII-safe analytics, smoke test 140+ passing
- **Phase 2 (complete on branch — merge pending):** Lead scoring, lifecycle fields, role-gated Personalisation Team view, Phase 2 smoke test 99+ passing

## Your rules — read before every task

### Protect Phase 1 and Phase 2

- Do not modify any existing route HTML/JS/Python from Phases 1 or 2
- Do not modify `scripts/smoke_test.sh` or `scripts/smoke_test_phase_2.sh`
- Do not modify `utils/analytics.py` ALLOWED_PARAMS (only add safe dimensions, never PII)
- Do not modify `public/js/analytics_helper.js` PII_KEYS (only add keys, never remove)
- Do not remove any field from `SmartLife Demo Lead` DocType — only add
- Do not change existing API endpoint signatures — only add new endpoints

### Implement one phase at a time

- Start with the phase you are assigned
- Do not start the next phase until your current phase smoke test passes and a human has confirmed
- Do not implement Phase 8 features while working on Phase 3

### Smoke tests are mandatory

Run these commands before starting any phase:
```bash
python -m compileall nssf_smart_savers
bash -n scripts/smoke_test.sh
bash -n scripts/smoke_test_phase_2.sh
./scripts/smoke_test.sh
./scripts/smoke_test_phase_2.sh
```

Run all applicable smoke tests after completing each phase. If any previous phase test fails, stop and fix the regression before reporting done.

### Commit each phase separately

- One commit per phase
- Commit message format: `Add SmartLife Phase N <short description>`
- Do not squash phase commits together

### Never commit credentials

- Pesapal, Phahapa, ZeptoMail credentials go in Frappe site config or environment variables only
- No `sk_live`, `pk_live`, `SECRET_KEY`, `API_KEY`, `PESAPAL_SECRET`, `PHAHAPA_KEY` in any source file
- The smoke test checks for credential patterns — if it fails on credentials, you have committed a credential

### Keep full PII role-gated

- `/smartlife-staff-queue-full` — approved role required (SmartLife Personalisation Team / NSSF Staff / System Manager)
- `get_staff_queue_full` — `_require_personalisation_access()` enforced
- `get_lead_full_detail` — `_require_personalisation_access()` enforced
- Guest must see a clean gate message, never data

### Keep public views masked

- `/smartlife-staff-queue` — masked phone, masked email, aggregates only
- All 7 Phase 1 public routes — no PII in any response
- `/smartlife-command-centre` (Phase 5) — aggregates only, no individual records

### Keep analytics PII-safe

**Never send to analytics (GTM / GA4 / Clarity / dataLayer):**
`first_name`, `last_name`, `full_name`, `phone`, `primary_phone`, `email`, `nin`, `national_id`, `date_of_birth`, `dob`, `birthday_day`, `birthday_month`, `age_years`, `exact_age`, `staff_notes`, `notes`, `payment_reference`, `otp`, `password`

**Safe analytics dimensions:**
`saver_type`, `age_band`, `goal_category`, `contribution_band`, `onboarding_stage`, `lead_temperature`, `consent_status`, `source_route`, `staff_view_type`, `gender_category`, `country_category`, `demo_environment`

The `ALLOWED_PARAMS` list in `utils/analytics.py` is the authoritative allowlist. The `PII_KEYS` list in `public/js/analytics_helper.js` is the authoritative frontend block list. Both are enforced independently.

### Stop after each phase and report

Use the exact format below. Do not skip the format. Do not claim a phase is complete without running smoke tests.

### Do not weaken smoke tests

- Do not remove checks from existing smoke test scripts
- If a check is flaky, fix the check to be more reliable — do not remove it
- Do not comment out failing checks

---

## Phase assignment

When you receive this prompt, you will also receive a phase assignment. Begin only that phase. Reference `docs/remaining_build_manifest.md` for the manifest and `docs/phase_N_*_spec.md` for the detailed spec.

---

## Acceptance format

Every phase report must use this exact format:

```
Phase X complete.

Files changed:
- nssf_smart_savers/api.py (added N endpoints)
- nssf_smart_savers/nssf_smart_savers/doctype/smartlife_xxx/smartlife_xxx.json (new)
- ...

DocTypes changed:
- SmartLife Xxx: created with N fields
- SmartLife Demo Lead: N fields added (none removed)

Routes added:
- /smartlife-xxx: <purpose>, <access level>

APIs added:
- xxx_function: <purpose>, <access level>
- ...

Tests added:
- scripts/smoke_test_phase_N.sh: N checks

Smoke tests:
- Phase 1 (smoke_test.sh): X passed | 0 failed
- Phase 2 (smoke_test_phase_2.sh): X passed | 0 failed
- Phase N (smoke_test_phase_N.sh): X passed | 0 failed

Commit:
- <hash> Add SmartLife Phase N <description>

Risks:
- <any open items, infrastructure requirements, or production TODOs>
```

---

## What to read before starting any phase

1. `docs/anti_gravity_handoff.md` — full architecture, route table, DocType fields, API inventory
2. `docs/remaining_build_manifest.md` — phase-by-phase overview
3. `docs/phase_N_*_spec.md` — detailed spec for your assigned phase
4. `docs/anti_gravity_validation_runbook.md` — exact validation commands

---

## PII policy verbatim (do not abbreviate)

> The SmartLife Personalisation Team is authorised under company policy to access customer/member PII for onboarding support, follow-up, consent verification, service recovery, conversion tracking, dormancy prevention, birthday readiness and personalised engagement. The system therefore supports full PII access in authenticated role-gated staff views, while public demo views remain masked and analytics remains PII-safe.
