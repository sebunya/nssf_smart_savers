# Phase 2 — SmartLife Lead Operating System

**Status:** Demo-safe prototype. No real member data.

---

## What Phase 2 adds

Phase 2 turns the Phase 1 public onboarding demo into an internal lead operating system. It adds:

1. Lead lifecycle tracking fields on `SmartLife Demo Lead`
2. A deterministic lead scoring engine (`lead_scoring.py`)
3. Phase 2 API endpoints for staff use
4. A staff-facing queue route (`/smartlife-staff-queue`)
5. Staff queue styles in `smartlife.css`
6. A Phase 2 smoke test (`scripts/smoke_test_phase_2.sh`)

Phase 2 does **not** add: payments, SMS, email, CRM integration, Helpdesk, command centre, or any production auth.

---

## DocTypes changed

### SmartLife Demo Lead (extended — no existing fields removed)

**Lifecycle section** — new fields added:

| Field | Type | Purpose |
|---|---|---|
| `lead_status` | Select | Structured lifecycle stage |
| `onboarding_stage` | Data | Free-text onboarding progress |
| `lead_temperature` | Select | Hot / Warm / Cold |
| `lead_score` | Int | Computed score 0–100 |
| `next_best_action` | Data | Recommended action for staff |
| `assigned_staff` | Data | Staff name assigned (demo only) |
| `last_contacted_on` | Date | Date of last contact attempt |
| `next_follow_up_on` | Date | Scheduled follow-up date |
| `follow_up_outcome` | Data | Outcome text from last contact |
| `drop_off_reason` | Data | Reason for dropping off |

**Attribution section** — new fields added:

| Field | Type | Purpose |
|---|---|---|
| `source_route` | Data | URL path that generated the lead |
| `campaign_source` | Data | UTM source |
| `campaign_medium` | Data | UTM medium |
| `campaign_name` | Data | UTM campaign name |

**Journey flags section** — new fields added:

| Field | Type | Purpose |
|---|---|---|
| `projection_viewed` | Check | Did the user view a projection? |
| `checkout_started` | Check | Did the user start checkout? |
| `payment_completed` | Check | Was a payment simulated? |

**Lead status values:**
`New` → `Personal Details Captured` → `Goal Selected` → `Projection Viewed` → `Checkout Started` → `Payment Pending` → `Payment Completed` → `Staff Follow-up Required` → `Contacted` → `Converted` → `Dormant` → `Disqualified`

---

## Lead scoring rules (`lead_scoring.py`)

Function: `calculate_lead_score(lead_or_dict)` → `{lead_score, lead_temperature, next_best_action, score_reasons}`

| Signal | Points |
|---|---|
| Consent given (gate) | +15 |
| Payment completed | +30 |
| Checkout started | +15 |
| Contribution ≥ 500k | +10 |
| Contribution ≥ 100k | +7 |
| Contribution ≥ 50k | +4 |
| Contribution > 0 | +2 |
| Frequency (daily=5, weekly=4, monthly=2…) | 1–5 |
| Saver type (existing_member=10, staff_assisted=9…) | 3–10 |
| Projection viewed | +8 |
| Staff assisted | +5 |
| Contact channel (sms/call=5, email=4…) | 0–5 |
| Age band (25-44 peak) | 3–5 |
| Goal with target amount | +5 |
| Goal only | +2 |
| Source route (checkout) | +3 |

**No consent → score 0, temperature Cold, action "No action until consent is granted"**

Temperature bands: Hot ≥ 65 · Warm ≥ 35 · Cold < 35

---

## APIs added

All endpoints are `allow_guest=True` for the prototype. Production would require role-based auth.

| Method | Purpose | PII exposure |
|---|---|---|
| `score_lead(session_id)` | Score a lead by session ID | None — bands only |
| `get_lead_summary()` | Aggregate counts by status/temp/segment/goal | None — counts only |
| `get_staff_queue(limit)` | Paginated staff action queue | Phone and email masked |
| `update_follow_up_status(lead_name, outcome, new_status)` | Record follow-up result | None |
| `assign_lead(lead_name, staff_name)` | Assign to staff | Staff name (not member PII) |
| `update_journey_flag(session_id, flag)` | Set projection_viewed / checkout_started / payment_completed | None |

Existing APIs updated:
- `submit_demo_lead` — now sets `lead_status`, runs scoring, sets `source_route`
- `submit_personal_details` — now sets `lead_status = Personal Details Captured`, runs scoring, sets `source_route`

---

## Routes added

| Route | File | Purpose |
|---|---|---|
| `/smartlife-staff-queue` | `www/smartlife-staff-queue.html` + `.py` | Staff lead queue demo page |

All Phase 1 routes unchanged.

---

## Staff queue page

`/smartlife-staff-queue` shows:
- Lead Overview metrics (total, hot, warm, cold, payment pending, staff required, converted, dormant)
- Lead Temperature bar chart
- Leads by saver type / savings goal / preferred contact channel
- Follow-up priority table (sorted by score, phone/email masked)
- Next Best Actions summary

Empty states render instead of errors when there is no data.

---

## Privacy rules

Phase 2 does not weaken Phase 1 privacy.

**Never sent to analytics, URLs, or frontend payloads:**
- first/last name, phone, email, NIN, DOB, exact age, birthday_month, birthday_day, OTP

**Safe analytics dimensions (unchanged from Phase 1):**
`saver_type`, `age_band`, `goal_category`, `contribution_band`, `onboarding_stage`, `lead_temperature`, `consent_status`, `source_route`

**Staff queue masking:**
- Phone: `070****545`
- Email: `ro***@domain.com`

**`get_lead_summary` returns counts only — no individual records.**

---

## Demo safety

- All data is demo-safe: `demo_note` field on every lead
- No real member data in source code
- Staff queue includes "Prototype environment" notice
- All API endpoints return `demo_notice` in response

---

---

## Personalisation Team PII Access Model

The SmartLife Personalisation Team is authorised under company policy to access customer/member PII for onboarding support, follow-up, service recovery, conversion tracking, dormancy prevention, birthday readiness and personalised engagement. The prototype therefore supports full PII access in authenticated staff views, while public demo views remain masked and analytics remains PII-safe.

### Why the Personalisation Team needs full PII

The Personalisation Team performs:
- **Follow-up calls and messages** — requires full phone and email
- **Consent calls** — requires consent status and preferred contact channel
- **Birthday readiness** — requires birthday_month and birthday_day for timely outreach
- **Service recovery** — requires full name, contact, and onboarding stage
- **Reactivation / dormancy prevention** — requires lead temperature, last contacted date, and next follow-up date
- **Conversion tracking** — requires checkout_started, payment_completed, goal, and contribution data
- **Segmentation** — requires saver_type, age_band, goal, and industry

None of these functions can be performed effectively with masked data.

### Three-tier access model

| Tier | Who | What they see |
|---|---|---|
| Tier 1: Public/Guest | Anyone (unauthenticated) | Aggregate counts, masked phone/email, distributions, lead temperature |
| Tier 2: Authenticated Staff | Any signed-in Frappe user | Tier 1 + full PII in `/smartlife-staff-queue-full` and `get_staff_queue_full` / `get_lead_full_detail` |
| Tier 3: Analytics | GTM / GA4 / Clarity | Safe dimensions only — never raw PII |

### Guest/public view (`/smartlife-staff-queue`)

Shows:
- Total leads, temperature counts, status counts
- Leads by saver type / goal / channel (aggregate)
- Masked phone (`070****545`), masked email (`ro***@domain.com`)
- Next best action labels
- "Masked demo view" notice

Does **not** show:
- Full phone, email, name, DOB, birthday fields, exact age, notes

### Authenticated Personalisation Team view (`/smartlife-staff-queue-full`)

Shows all fields including:
- `first_name`, `last_name`
- `primary_phone`, `email_address`
- `date_of_birth`, `age_years`, `birthday_month`, `birthday_day`
- `preferred_contact_channel`, `consent_to_contact`
- `lead_status`, `lead_temperature`, `lead_score`
- `next_best_action`, `assigned_staff`
- `last_contacted_on`, `next_follow_up_on`, `follow_up_outcome`
- `source_route`, `campaign_source`, `campaign_medium`, `campaign_name`
- `projection_viewed`, `checkout_started`, `payment_completed`
- `staff_notes` (internal remarks)

If user is not signed in, shows "Staff sign-in required" and a sign-in link. No PII visible to guest.

### Guest-safe API endpoints (`allow_guest=True`)

| Endpoint | What it returns |
|---|---|
| `get_lead_summary` | Counts grouped by status / temperature / segment / goal / channel — no individual records |
| `get_staff_queue` | Masked queue (phone_masked, email_masked) — aggregate-safe |
| `get_projection` | Projection calculation — no PII |
| `get_personalised_plan_api` | Plan recommendation — no PII |
| `submit_demo_lead` | Lead creation — returns session_id and age_band only |
| `submit_personal_details` | Personal details capture — returns session_id and age_band only |
| `log_analytics_event` | Analytics logging — PII is filtered before storage |
| `log_dropoff` | Dropoff logging — no PII |
| `request_support` | Support request — sanitised before storage |
| `score_lead` | Score by session_id — returns bands only, no raw PII |

### Authenticated full-PII API endpoints (require sign-in)

| Endpoint | Auth required | What it returns |
|---|---|---|
| `get_staff_queue_full` | Any authenticated user | Full unmasked queue records |
| `get_lead_full_detail` | Any authenticated user | All fields for a single lead including PII |

### Write endpoints (require sign-in)

| Endpoint | Auth required | Action |
|---|---|---|
| `update_follow_up_status` | Any authenticated user | Updates outcome and lead status |
| `assign_lead` | Any authenticated user | Assigns staff to lead |
| `update_journey_flag` | Any authenticated user | Sets projection_viewed / checkout_started / payment_completed |

### Why analytics still blocks PII

Even though staff can see full PII in the authenticated view, analytics pipelines (GTM, GA4, Clarity, frontend dataLayer) must never receive raw PII because:
- Analytics events may be logged to third-party platforms outside NSSF's control
- Event logs may be accessible to non-authorised parties
- Regulatory and data protection obligations apply to analytics platforms

The `analytics_helper.js` frontend block list and `sanitise_event_params()` server-side allowlist both enforce this independently.

### Why logs should avoid raw PII

Internal action logs (follow-up updates, assignment changes) record:
- Lead document name (internal reference)
- Action taken
- Staff user identifier
- Old and new status

They do not record phone, email, DOB, name, or notes, so that log access does not require the same controls as PII access.

### Current prototype guard

```python
def _require_personalisation_access():
    if _is_guest():
        frappe.throw("Personalisation team sign-in required.", frappe.PermissionError)
    # Any authenticated Frappe user passes.
    # Production TODO: enforce SmartLife Personalisation Team / NSSF Staff / System Manager role.
```

### Production requirement for formal role-based access

Before going live, replace the prototype authenticated-session guard with a Frappe role check:

```python
allowed_roles = {"SmartLife Personalisation Team", "NSSF Staff", "System Manager"}
if not allowed_roles.intersection(set(frappe.get_roles())):
    frappe.throw("Access denied.", frappe.PermissionError)
```

Create the `SmartLife Personalisation Team` role in Frappe and assign it only to authorised NSSF staff. The `NSSF Staff` and `System Manager` roles should be narrowly assigned.

---

## What is required before production launch

1. Role-based authentication on all Phase 2 endpoints (remove `allow_guest=True`)
2. Real UTM attribution from frontend query params
3. Actual SMS/email follow-up integration (Phase 3)
4. CRM/Helpdesk sync (Phase 4)
5. Staff login and session management
6. Audit log for follow-up actions
7. NSSF data protection officer sign-off on PII handling
