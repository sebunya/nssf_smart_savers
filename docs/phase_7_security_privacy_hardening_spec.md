# Phase 7 — Security, Privacy and Production Hardening

**Status:** Not started  
**Depends on:** All Phases 1–6 complete and smoke tests passing  
**Human sign-off required** before Phase 8

---

## Objective

Audit and harden the SmartLife Flexi demo for serious NSSF review and to prepare a safer production path. This is a review-and-fix phase — no new features, no new DocTypes, no new routes unless strictly required for hardening.

---

## Non-Negotiables

- Do not break any existing functionality
- Do not remove PII access from the Personalisation Team — hardening means tightening access, not removing authorised access
- Any live credentials must remain in env vars or Frappe site config — never source code
- All smoke tests (Phases 1–6) must pass at the end of Phase 7

---

## Hardening Checklist

### 1. CSRF handling
- Verify Frappe's built-in CSRF protection is active on all mutation endpoints
- Confirm `@frappe.whitelist()` endpoints (non-guest) require a valid CSRF token
- Document in `docs/security_privacy_review.md`

### 2. Rate limiting
- Review guest-open endpoints for abuse potential
- Implement simple in-app rate limiting on high-risk guest endpoints:
  - `submit_demo_lead` — max 10 per IP per hour
  - `submit_personal_details` — max 10 per IP per hour
  - `request_support` — max 5 per IP per hour
  - `create_support_request` — max 5 per IP per hour
  - `log_analytics_event` — max 100 per IP per hour
- Use Frappe rate limiting primitives or Redis-backed counter if available
- If not available in this Frappe version, document as a production TODO

### 3. Guest endpoint audit
Verify every `allow_guest=True` endpoint:
- Returns no raw PII
- Runs `_check_pii` on user-supplied text where applicable
- Has no traceback path to the browser
- Sanitises all free-text inputs via `sanitise_demo_text`

### 4. Role guard audit
Verify every full-PII and write endpoint:
- Is NOT `allow_guest=True`
- Calls either `_require_authenticated_staff()` or `_require_personalisation_access()`
- `_require_personalisation_access()` calls `_has_allowed_personalisation_role()` which calls `frappe.get_roles()`
- No "any authenticated user" bypass remains for full-PII data

### 5. Analytics PII block audit
- Re-verify `ALLOWED_PARAMS` in `utils/analytics.py` contains no PII keys
- Re-verify `PII_KEYS` in `analytics_helper.js` covers all required keys
- Re-verify `sanitise_event_params()` drops unlisted keys
- Document the double-enforcement architecture

### 6. Credential audit
- Scan all source files for patterns: `sk_live`, `pk_live`, `SECRET_KEY`, `PRIVATE_KEY`, `API_KEY`, `PESAPAL_`, `PHAHAPA_`, `ZEPTOMAIL_`
- Scan `.env` files if any are present
- Verify `.gitignore` excludes credential files
- Document: all credentials must use Frappe `frappe.conf` or environment variables

### 7. Traceback exposure
- Verify no Frappe error tracebacks are visible to guest users in any route
- Verify all exception handlers return structured JSON errors, not HTML tracebacks
- Test by sending malformed requests to guest endpoints

### 8. PII in URLs
- Audit all routes and API responses for URL patterns containing PII
- Verify thank-you page URL does not contain name, phone, email, session detail
- Verify checkout redirect does not put PII in query parameters
- Verify callback URL for Pesapal does not expose raw PII

### 9. PII in logs
- Audit `frappe.log_error` calls — verify they log document names and action types, not raw PII fields
- Verify `log_analytics_event` sanitises before storage
- Review `SmartLife Integration Event` payloads for PII leakage

### 10. Page-level route protection
- `/smartlife-staff-queue-full`: verify guest sees clean gate, not data
- `/smartlife-command-centre`: verify guest sees clean gate
- Verify no PII visible in HTML source of any public route
- Run `curl` against public routes and grep for phone/email/name patterns

### 11. No live payment credentials committed
- Verify `pesapal_adapter.py` reads credentials from `frappe.conf` or env — not hardcoded
- Verify sandbox/demo fallback fires correctly when credentials absent

### 12. Consent enforcement
- Audit `send_demo_message` and all communication functions for consent gate
- Verify no outbound message path bypasses `consent_to_contact` check
- Document consent enforcement in `docs/security_privacy_review.md`

### 13. Staff role assignment reminder
- Document in `docs/security_privacy_review.md`: the `SmartLife Personalisation Team` role must be manually created in Frappe and assigned to authorised users before the full-PII view works
- Include Frappe admin steps

### 14. Data retention notes
- Document demo-safe data retention: all data is demo data, no real member data
- Note that a production deployment requires NSSF DPO sign-off on data retention periods
- Recommended: implement a periodic purge script for demo data

---

## New Document: `docs/security_privacy_review.md`

Create this document covering:
- CSRF status
- Rate limiting status and gaps
- Guest endpoint inventory with risk rating
- Role guard confirmation
- Analytics PII block confirmation
- Credential handling approach
- PII in URLs/logs status
- Consent enforcement confirmation
- Open TODOs for production

---

## Smoke Test: `scripts/smoke_test_phase_7.sh`

Must check:

```bash
# Baseline
Phase 1–6 smoke tests pass

# Credential safety
No live Pesapal credentials in source
No Phahapa API key in source
No ZeptoMail API key in source
No generic SECRET_KEY/PRIVATE_KEY in source

# Role guard completeness
_require_personalisation_access calls _has_allowed_personalisation_role
_has_allowed_personalisation_role calls frappe.get_roles
get_staff_queue_full is not allow_guest
get_lead_full_detail is not allow_guest
All write endpoints are not allow_guest

# Analytics PII block
ALLOWED_PARAMS contains no PII keys (Python AST check)
PII_KEYS in analytics_helper.js covers: first_name, last_name, primary_phone, email,
  date_of_birth, birthday_day, birthday_month, age_years, nin

# PII in URLs
thank-you page HTML does not contain primary_phone or email patterns in URL attributes
No PII keys in href or action attributes of any public route

# Guest endpoint input sanitisation
submit_demo_lead calls sanitise_demo_text or _check_pii
request_support calls sanitise_demo_text
create_support_request calls sanitise_demo_text

# Security review doc
docs/security_privacy_review.md exists

# Python compile
All Phase 7 Python files compile (full app)

# Live routes
All public routes return HTTP 200
staff-queue-full returns 200 (guest gate rendered, not blocked)
command-centre returns 200 (guest gate rendered, not blocked)
```

---

## Anti-Gravity Implementation Prompt

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 7 — Security, Privacy and Production Hardening — exactly as specified in docs/phase_7_security_privacy_hardening_spec.md.

STOP CONDITIONS:
- Stop after Phase 7. Do not start Phase 8 without explicit human approval.
- Do not remove PII access from the Personalisation Team.
- Do not break any existing functionality.
- This is a review-and-fix phase — add no new features.

BEFORE YOU START:
1. Run all six smoke tests — all must pass.
2. Review docs/phase_7_security_privacy_hardening_spec.md completely.
3. Review docs/anti_gravity_handoff.md for PII access model.

IMPLEMENTATION ORDER:
1. Work through the hardening checklist in order (1–14).
2. Create docs/security_privacy_review.md documenting findings and fixes.
3. Fix any gaps found during audit.
4. Create scripts/smoke_test_phase_7.sh.
5. Run all seven smoke tests.
6. Report: explicitly state any hardening items that require production infrastructure (rate limiting, etc.) and cannot be implemented at the app layer.

HUMAN SIGN-OFF REQUIRED before Phase 8.

ACCEPTANCE FORMAT:
Phase 7 complete.
[use standard format from anti_gravity_master_prompt.md]

Include an additional section:
Security audit findings:
- CSRF: ...
- Rate limiting: ...
- PII in URLs: ...
- PII in logs: ...
- Credential handling: ...
- Open production TODOs: ...
```
