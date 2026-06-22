# Phase 8 — Release Pack and Final Handover

**Status:** Not started  
**Depends on:** All Phases 1–7 complete, Phase 7 human sign-off received

---

## Objective

Create the full technical, business and demo handover package for NSSF Uganda. All documentation must be accurate, demo-safe, and readable by both technical staff and business stakeholders.

---

## Non-Negotiables

- Do not create documents with real PII as examples
- Do not modify application code in Phase 8
- All documents must reflect the actual current state of the app
- Production readiness checklist must include NSSF DPO sign-off item

---

## Documents to Create

### `docs/phase_2_to_8_release_notes.md`

**Audience:** Technical staff  
**Content:**
- Summary of changes per phase (2 through 8)
- New DocTypes per phase
- New routes per phase
- New APIs per phase
- Migration requirements per phase
- Breaking changes (none should exist — phases are additive)
- Known issues and limitations

### `docs/nssf_smartlife_demo_walkthrough.md`

**Audience:** NSSF product and technical stakeholders  
**Content:**
- Full journey narrative from landing to conversion
- Screenshots or step descriptions for each screen
- What each screen demonstrates
- What data is captured at each step
- How the Personalisation Team uses the system
- How analytics works without PII
- What the Command Centre shows

### `docs/admin_user_guide.md`

**Audience:** NSSF system administrators  
**Content:**
- How to access Frappe desk
- How to view SmartLife Demo Lead records
- How to run bench migrate after an update
- How to create roles and assign them
- How to configure Pesapal, Phahapa, ZeptoMail credentials (env vars)
- How to clear cache and restart services
- How to run smoke tests
- How to check error logs

### `docs/staff_user_guide.md`

**Audience:** NSSF Personalisation Team staff  
**Content:**
- How to sign in to Frappe
- How to access `/smartlife-staff-queue` (masked demo view)
- How to access `/smartlife-staff-queue-full` (full PII view — requires role)
- How to update follow-up status
- How to assign a lead to staff
- How to update journey flags
- How to send a demo message (Phase 4)
- How to view communication history
- How to access support requests
- PII handling responsibilities

### `docs/demo_script.md`

**Audience:** NSSF demo presenters  
**Content — cover all of the following in sequence:**

1. **Landing page** (`/smartlife-flexi-demo`) — goal selection, saver type, NSSF brand
2. **Self-serve onboarding** (`/smartlife-self-serve`) — personal details with DOB, goal, contribution
3. **DOB-based personalisation** — show age band computed server-side, no manual age
4. **Projection** (`/smartlife-projection-demo`) — projection calculation, goal vs. timeline
5. **Checkout** (`/smartlife-checkout-demo`) — plan summary, payment method, sandbox notice
6. **Thank-you** (`/smartlife-thank-you`) — confirmation, next steps
7. **Staff-assisted flow** (`/smartlife-staff-assist`) — same journey with staff in control
8. **Staff queue masked view** (`/smartlife-staff-queue`) — masked contact demo, lead metrics
9. **Personalisation Team full PII view** (`/smartlife-staff-queue-full`) — role gate demo, full detail
10. **Contribution intent** (Phase 3) — Pesapal sandbox checkout demo
11. **Communications** (Phase 4) — demo message send, consent enforcement, communication log
12. **Command Centre** (Phase 5) — funnel metrics, distribution charts, no PII
13. **Support flow** (Phase 6) — structured support request, assignment workflow
14. **Privacy and PII protection** — show analytics_helper.js PII block list, ALLOWED_PARAMS, role guard code
15. **What's next** — production requirements, DPO sign-off, role setup

### `docs/known_limitations.md`

**Audience:** NSSF technical and product stakeholders  
**Content:**
- Demo environment — no real member data
- No live Pesapal payments without production credentials
- Rate limiting is not active at app layer — must be configured at Nginx/infrastructure level
- WhatsApp integration is copy-ready only — API not connected
- Role assignment is manual — no automated provisioning
- `bench migrate` required after every DocType change
- Birthday-based outreach requires scheduled task setup
- No multi-tenancy — single site deployment
- No Frappe role audit log by default — recommend enabling for production

### `docs/production_readiness_checklist.md`

**Audience:** NSSF technical team, system integrator, NSSF DPO  

**Checklist items:**

```
Infrastructure
[ ] Production server provisioned (separate from demo)
[ ] SSL certificate installed
[ ] Frappe production mode configured
[ ] Backups configured and tested
[ ] Monitoring and alerting set up

Application
[ ] SmartLife Personalisation Team role created and assigned
[ ] NSSF Staff role assigned to authorised users
[ ] Pesapal production credentials configured (env var / site config)
[ ] Phahapa SMS production credentials configured
[ ] ZeptoMail production email credentials configured
[ ] Demo mode disabled or clearly labelled
[ ] Rate limiting configured at Nginx layer
[ ] CORS configured for production domain

Data and Privacy
[ ] NSSF DPO sign-off obtained on PII handling and data retention
[ ] Data retention schedule defined and implemented
[ ] Analytics pipeline reviewed (no PII to GA4/GTM/Clarity)
[ ] Consent workflow reviewed by legal
[ ] Staff PII access documented and authorised

Smoke Tests
[ ] Phase 1 smoke test passes on production server
[ ] Phase 2 smoke test passes on production server
[ ] Phase 3 smoke test passes on production server
[ ] Phase 4 smoke test passes on production server
[ ] Phase 5 smoke test passes on production server
[ ] Phase 6 smoke test passes on production server
[ ] Phase 7 smoke test passes on production server

Sign-off
[ ] NSSF Technical Lead sign-off
[ ] NSSF DPO sign-off on PII
[ ] System integrator sign-off
[ ] Anti-Gravity / build team sign-off
```

---

## Smoke Test: All previous smoke tests

Phase 8 has no new smoke test. The acceptance gate is all previous smoke tests passing.

---

## Anti-Gravity Implementation Prompt

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 8 — Release Pack and Final Handover — exactly as specified in docs/phase_8_release_pack_spec.md.

STOP CONDITIONS:
- This is the terminal phase. No more phases after Phase 8.
- Do not modify application code.
- Do not use real PII in any example.
- Obtain human sign-off before declaring the project complete.

BEFORE YOU START:
1. Run all seven smoke tests — all must pass.
2. Review docs/phase_8_release_pack_spec.md completely.
3. Review the actual current state of every route, API, and DocType before writing docs.

IMPLEMENTATION ORDER:
1. Create docs/phase_2_to_8_release_notes.md (technical).
2. Create docs/nssf_smartlife_demo_walkthrough.md (product stakeholders).
3. Create docs/admin_user_guide.md (sysadmin).
4. Create docs/staff_user_guide.md (Personalisation Team).
5. Create docs/demo_script.md (presenters — cover all 15 steps).
6. Create docs/known_limitations.md (honest inventory of gaps).
7. Create docs/production_readiness_checklist.md (includes DPO sign-off item).
8. Run all smoke tests one final time.
9. Report: explicitly state which checklist items require human/infrastructure action.

ACCEPTANCE FORMAT:
Phase 8 complete. Project complete pending human sign-off.

Files created:
- docs/phase_2_to_8_release_notes.md
- docs/nssf_smartlife_demo_walkthrough.md
- docs/admin_user_guide.md
- docs/staff_user_guide.md
- docs/demo_script.md
- docs/known_limitations.md
- docs/production_readiness_checklist.md

Smoke tests:
- All phases: X passed | 0 failed

Human actions required before production launch:
- ...

Sign-off required from:
- NSSF Technical Lead
- NSSF DPO
- System integrator
```
