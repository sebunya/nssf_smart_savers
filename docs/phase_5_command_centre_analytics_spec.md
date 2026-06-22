# Phase 5 — Command Centre and Analytics

**Status:** Not started  
**Depends on:** Phase 4 complete and smoke tests passing

---

## Objective

Create a management dashboard at `/smartlife-command-centre` for NSSF leadership and programme managers to review SmartLife Flexi onboarding performance — in aggregate only, with zero raw PII.

---

## Non-Negotiables

- Do not break Phases 1–4
- All dashboard data must be aggregate — no individual records visible to any user
- Birthday month: allowed only as a distribution count (e.g. "January: 12 leads") — never individual birthday
- No raw phone, email, name, NIN, DOB rendered anywhere on this route
- All APIs on this route are aggregate-only
- No analytics PII leakage

---

## New Route: `/smartlife-command-centre`

### Route Python file: `nssf_smart_savers/www/smartlife-command-centre.py`

- Sets `context.is_demo = True`
- Sets `context.no_breadcrumbs = True`
- Does not expose individual records server-side

### Route HTML file: `nssf_smart_savers/www/smartlife-command-centre.html`

Extends `templates/web.html`. Includes `smartlife_brand_shell.html`. Uses NSSF brand bar with tagline "Command Centre".

### Dashboard sections and cards

#### Summary metrics strip
| Card | Metric |
|---|---|
| Total Leads | Count of all SmartLife Demo Leads |
| Personal Details Completed | Count with lead_status ≥ Personal Details Captured |
| Projections Viewed | Count with projection_viewed = 1 |
| Checkout Started | Count with checkout_started = 1 |
| Payment Pending | Count with lead_status = Payment Pending |
| Payment Completed | Count with payment_completed = 1 |
| Conversion Rate | (Payment Completed / Total Leads) × 100% |

#### Funnel section
Drop-off at each stage: Goal Selected → Personal Details → Projection → Checkout → Payment

#### Distribution sections (aggregate counts only)
- Leads by saver type (`segment`)
- Leads by savings goal (`goal`)
- Leads by age band (`age_band`)
- Leads by preferred contact channel
- Lead temperature distribution (Hot / Warm / Cold counts)
- Birthday month distribution (count per month — no individual birthday shown)
- Campaign source performance (count per `campaign_source`)
- Contribution intent summary (if Phase 3 is deployed: total intents, completed, pending, failed)

#### Staff follow-up queue summary
- Count of leads in Staff Follow-up Required status
- Count unassigned
- Count assigned but overdue (next_follow_up_on < today)

---

## Access Model

`/smartlife-command-centre` is restricted to authenticated staff — guest should see a sign-in gate (same pattern as `/smartlife-staff-queue-full` but without individual PII).

**Python controller** sets `context.is_guest` and `context.has_personalisation_role` (same pattern as `smartlife-staff-queue-full.py`).

**Guest** → "Staff sign-in required" gate with login link  
**Signed-in, any role** → full aggregate dashboard (no PII in aggregate data so any authenticated user can view)

---

## New API Endpoints

All command centre APIs are `@frappe.whitelist()` (authenticated required) and return aggregates only — no individual records.

### `get_command_centre_summary()`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No — counts and percentages only |
| **Purpose** | Return all summary metric counts in one call |
| **Returns** | `{total, personal_details, projections_viewed, checkout_started, payment_pending, payment_completed, conversion_rate, staff_followup_required, unassigned, overdue}` |

### `get_conversion_funnel()`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No |
| **Purpose** | Return count at each funnel stage for drop-off visualisation |
| **Returns** | `{stages: [{stage, count, pct_of_total}]}` |

### `get_dropoff_by_stage()`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No |
| **Purpose** | Count of leads whose `dropoff_step` matches each stage |
| **Returns** | `{by_stage: {stage_name: count}}` |

### `get_lead_distribution(dimension)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No |
| **Purpose** | Count leads grouped by a safe dimension |
| **Allowed dimensions** | `segment`, `goal`, `age_band`, `preferred_contact_channel`, `lead_temperature`, `gender`, `country`, `frequency` |
| **Returns** | `{dimension, distribution: {value: count}}` |

### `get_campaign_performance()`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No |
| **Purpose** | Count leads by `campaign_source` and `campaign_medium` |
| **Returns** | `{by_source: {source: count}, by_medium: {medium: count}}` |

### `get_birth_month_distribution()`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` |
| **Returns PII?** | No — month distribution only (1–12 as count per month) |
| **Purpose** | Show birthday month distribution for birthday campaign planning |
| **Returns** | `{months: {1: count, 2: count, ..., 12: count}}` |
| **Privacy** | Never return birthday_day or individual lead data — only month counts |

---

## Smoke Test: `scripts/smoke_test_phase_5.sh`

Must check:

```bash
# Baseline
Phase 1, 2, 3, 4 smoke tests pass

# Route
smartlife-command-centre.html exists
smartlife-command-centre.py exists
Route HTML contains brand shell include
Route HTML contains guest gate logic

# APIs
get_command_centre_summary defined
get_conversion_funnel defined
get_dropoff_by_stage defined
get_lead_distribution defined
get_campaign_performance defined
get_birth_month_distribution defined

# Access control
All command centre APIs are NOT allow_guest=True

# PII safety
get_birth_month_distribution does NOT return birthday_day or primary_phone
get_lead_distribution does NOT include 'first_name' or 'email' as allowed dimensions
No raw PII in any command centre API response structure (inspect function body)

# Analytics safety
No new PII dimensions added to ALLOWED_PARAMS
analytics_helper.js PII_KEYS unchanged

# Python compile
All Phase 5 Python files compile

# Live route
/smartlife-command-centre returns HTTP 200
```

---

## Anti-Gravity Implementation Prompt

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 5 — Command Centre and Analytics — exactly as specified in docs/phase_5_command_centre_analytics_spec.md.

STOP CONDITIONS:
- Stop after Phase 5. Do not start Phase 6.
- Do not break Phases 1–4.
- All data on /smartlife-command-centre must be aggregate only.
- No individual records visible to any user.
- Birthday month: distribution count only — never individual birthday.

BEFORE YOU START:
1. Run all four smoke tests — all must pass.
2. Review docs/phase_5_command_centre_analytics_spec.md completely.

IMPLEMENTATION ORDER:
1. Create www/smartlife-command-centre.html (extends web.html, brand shell, guest gate).
2. Create www/smartlife-command-centre.py (context: is_guest, has_personalisation_role or is_staff).
3. Add Phase 5 API endpoints to api.py (append only).
4. Create scripts/smoke_test_phase_5.sh.
5. No bench migrate needed (no new DocTypes in Phase 5).
6. Run all five smoke tests.

ACCEPTANCE FORMAT:
Phase 5 complete.
[use standard format from anti_gravity_master_prompt.md]
```
