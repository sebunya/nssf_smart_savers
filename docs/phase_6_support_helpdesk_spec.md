# Phase 6 — Support and Helpdesk

**Status:** Not started  
**Depends on:** Phase 5 complete and smoke tests passing

---

## Objective

Make the support flow at `/smartlife-support-demo` usable for prospects who need help completing SmartLife Flexi onboarding. Replace the basic placeholder with a structured support request form and staff assignment workflow.

---

## Non-Negotiables

- Do not break Phases 1–5
- Do not expose PII in public API responses
- Do not integrate Frappe Helpdesk unless it is confirmed safe and low-risk in the target environment
- Use `SmartLife Support Request` DocType first — Helpdesk integration is optional
- All support messages sanitised before storage (use `sanitise_demo_text`)
- Consent snapshot recorded on every support request

---

## Enhance: `/smartlife-support-demo`

Replace the basic support form with a structured form containing:

### Support categories (radio or select)
```
I need help joining SmartLife Flexi
I need help understanding projections
I need help making a contribution
I am already an NSSF member
I am in the diaspora
I want staff to call me
Other
```

### Form fields
- Support category (required)
- Message / describe your issue (text area, max 500 chars, sanitised)
- Preferred contact channel (SMS / Email / Phone call)
- Session ID (hidden — pre-filled from URL/localStorage)

### Behaviour
- On submit: call `create_support_request` API
- On success: show confirmation with request reference number
- On failure: show retry message — never traceback
- Anonymous (no name/email required at this stage — resolve via session_id → lead link)

---

## New DocType: SmartLife Support Request

**Purpose:** Track each support request from creation to resolution.

### Fields

| Field | Type | Notes |
|---|---|---|
| `lead` | Link → SmartLife Demo Lead | Optional (linked via session_id lookup) |
| `session_id` | Data | From URL/localStorage |
| `support_category` | Select | Enum of categories above |
| `preferred_contact_channel` | Select | SMS, Email, Phone call |
| `message` | Small Text | Sanitised — max 500 chars |
| `status` | Select | New, Assigned, In Progress, Resolved, Closed |
| `assigned_staff` | Data | Staff name |
| `created_on` | Datetime | Auto-set |
| `resolved_on` | Datetime | |
| `resolution_notes` | Small Text | Internal only — never public |
| `consent_snapshot` | Check | consent_to_contact value at time of request |
| `demo_mode` | Check | Always 1 in prototype |

### Status lifecycle
`New` → `Assigned` → `In Progress` → `Resolved` → `Closed`

---

## New API Endpoints

### `create_support_request(session_id, support_category, message, preferred_contact_channel="")`

| Item | Detail |
|---|---|
| **Access** | `allow_guest=True` |
| **Returns PII?** | No — returns request_name (reference) only |
| **Mutates?** | Yes — creates SmartLife Support Request |
| **Sanitisation** | `sanitise_demo_text(message, 500)` before storage; `_check_pii(message)` |
| **Lead link** | Look up lead by session_id — link if found; proceed without link if not |
| **Demo fallback** | Always succeeds with `demo_mode = true` |

### `get_support_requests(status=None, limit=50)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` — any authenticated staff |
| **Returns PII?** | No raw PII — returns reference, category, status, assigned_staff, created_on |
| **Purpose** | Staff view of support request queue |
| **Filter** | Optional status filter |

### `assign_support_request(request_name, staff_name)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` — requires `_require_authenticated_staff()` |
| **Returns PII?** | No |
| **Mutates?** | Yes — sets assigned_staff and status = Assigned |

### `update_support_status(request_name, new_status, resolution_notes="")`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` — requires `_require_authenticated_staff()` |
| **Returns PII?** | No |
| **Mutates?** | Yes — updates status and optional resolution notes |
| **Allowed statuses** | New, Assigned, In Progress, Resolved, Closed |

---

## Frappe Helpdesk Integration (Optional)

If `frappe_helpdesk` is installed and confirmed safe:

1. Create a Helpdesk ticket in addition to `SmartLife Support Request` using `helpdesk_adapter.py`
2. Store the Helpdesk ticket ID in an additional field on `SmartLife Support Request`
3. Do not remove the `SmartLife Support Request` DocType — it remains the authoritative record
4. If Helpdesk is not installed, `helpdesk_adapter.py` must silently skip (no error)

---

## Smoke Test: `scripts/smoke_test_phase_6.sh`

Must check:

```bash
# Baseline
Phase 1, 2, 3, 4, 5 smoke tests pass

# Route
smartlife-support-demo.html exists
Route HTML contains support category options
Route HTML contains 'I need help joining SmartLife Flexi' option
Route HTML contains create_support_request call

# DocType
SmartLife Support Request JSON exists
Required fields: lead, session_id, support_category, status, consent_snapshot, demo_mode

# APIs
create_support_request defined
get_support_requests defined
assign_support_request defined
update_support_status defined

# Access control
create_support_request IS allow_guest=True (public form)
get_support_requests is NOT allow_guest=True
assign_support_request is NOT allow_guest=True
update_support_status is NOT allow_guest=True
assign_support_request calls _require_authenticated_staff
update_support_status calls _require_authenticated_staff

# PII safety
create_support_request calls sanitise_demo_text
No raw PII in get_support_requests return fields
resolution_notes not in any public API return

# Python compile
All Phase 6 Python files compile

# Live route
/smartlife-support-demo returns HTTP 200
```

---

## Anti-Gravity Implementation Prompt

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 6 — Support and Helpdesk — exactly as specified in docs/phase_6_support_helpdesk_spec.md.

STOP CONDITIONS:
- Stop after Phase 6. Do not start Phase 7.
- Do not break Phases 1–5.
- Do not expose raw PII in any public API response.
- Use SmartLife Support Request DocType as primary — Frappe Helpdesk integration is optional.

BEFORE YOU START:
1. Run all five smoke tests — all must pass.
2. Review docs/phase_6_support_helpdesk_spec.md completely.

IMPLEMENTATION ORDER:
1. Create SmartLife Support Request DocType JSON + Python.
2. Enhance www/smartlife-support-demo.html with structured support form.
3. Add Phase 6 API endpoints to api.py (append only).
4. Update helpdesk_adapter.py with optional Frappe Helpdesk integration.
5. Create scripts/smoke_test_phase_6.sh.
6. Run bench migrate after DocType creation.
7. Run all six smoke tests.

ACCEPTANCE FORMAT:
Phase 6 complete.
[use standard format from anti_gravity_master_prompt.md]
```
