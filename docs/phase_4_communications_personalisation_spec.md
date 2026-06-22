# Phase 4 — Communications and Personalisation

**Status:** Not started  
**Depends on:** Phase 3 complete and smoke tests passing

---

## Objective

Prepare consented lifecycle messaging across SMS, email and WhatsApp-ready copy. All outbound communication must be consent-gated, logged, and demo-safe. No real messages sent unless explicitly configured with provider credentials.

---

## Non-Negotiables

- Do not break Phases 1, 2, or 3
- No outbound communication without `consent_to_contact = true`
- Never send PII to analytics
- Never log raw PII in message logs (mask recipient in list views)
- Provider credentials must not be committed — environment variables or Frappe site config only
- If provider credentials are missing, all sends must silently simulate and log as `demo_mode = true`
- WhatsApp: provide message copy only — do not activate API unless explicitly configured

---

## Channels

| Channel | Provider | Status |
|---|---|---|
| SMS | Phahapa | Adapter stub exists (`integrations/phahapa_sms_adapter.py`) |
| Email | ZeptoMail | Adapter stub exists (`integrations/zeptomail_adapter.py`) |
| WhatsApp | TBD | Copy-ready only unless API explicitly configured |

---

## Message Templates

Create a `SmartLife Personalisation Rule` or static template store for the following templates. Each template must have: `template_name`, `channel`, `subject` (email), `body`, `placeholders`, `trigger_stage`.

| Template Name | Channel | Trigger Stage |
|---|---|---|
| `welcome_personal_details` | SMS + Email | Personal Details Captured |
| `projection_viewed_reminder` | SMS | Projection Viewed (no checkout after 24h) |
| `checkout_abandoned_reminder` | SMS + Email | Checkout Started (no payment after 2h) |
| `initial_deposit_reminder` | Email | Payment Pending (after 48h) |
| `birthday_message` | SMS | Birthday month (birthday_day = today) |
| `staff_followup_message` | SMS | Staff Follow-up Required |
| `savings_milestone_message` | SMS + Email | Payment Completed |
| `dormant_lead_reactivation` | SMS + Email | Dormant (after 30 days) |
| `consent_education_content` | Email | No consent — educational only, no ask |
| `diaspora_saver_followup` | Email | segment = diaspora_ugandan |
| `informal_sector_followup` | SMS | segment = informal_sector |

### Template placeholder rules
Allowed placeholders: `{first_name}`, `{goal_label}`, `{contribution_amount}`, `{frequency}`, `{next_follow_up_on}`, `{saver_type_label}`  
Never use: `{email}`, `{phone}`, `{nin}`, `{dob}`, `{age}`, `{primary_phone}`, `{date_of_birth}`

---

## Consent Rules

No outbound message may be sent unless ALL of the following are true:
1. `consent_to_contact = true` on the lead
2. `preferred_contact_channel` is set and matches the channel being used
3. The required contact field exists (`primary_phone` for SMS, `email_address` for email)
4. The send is logged to `SmartLife Communication Log` before and after

If any condition fails, log the failure and abort silently — never throw to the user.

---

## New DocType: SmartLife Communication Log

**Purpose:** Audit trail for all outbound communication attempts.

### Fields

| Field | Type | Notes |
|---|---|---|
| `lead` | Link → SmartLife Demo Lead | Required |
| `channel` | Select | SMS, Email, WhatsApp |
| `template_name` | Data | Template used |
| `recipient_masked` | Data | Masked phone/email — never raw PII in this field |
| `message_status` | Select | Draft, Sent, Delivered, Failed, Simulated |
| `provider` | Data | phahapa, zeptomail, etc. |
| `provider_reference` | Data | Provider message ID |
| `sent_on` | Datetime | |
| `failure_reason` | Data | |
| `consent_snapshot` | Check | Value of consent_to_contact at send time |
| `staff_owner` | Data | Staff user who triggered send |
| `triggered_by_stage` | Data | Lead lifecycle stage at trigger |
| `demo_mode` | Check | Always 1 in prototype |

**PII rule:** `recipient_masked` must always store masked value — e.g. `070****545` or `ro***@domain.com`. Never store raw phone or email in this field.

---

## New API Endpoints

### `get_message_templates(channel=None)`

| Item | Detail |
|---|---|
| **Access** | `allow_guest=True` (returns template structure only, no PII) |
| **Returns PII?** | No |
| **Purpose** | Return available templates, optionally filtered by channel |

### `preview_message(template_name, session_id)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` (staff only — resolves lead PII for preview) |
| **Returns PII?** | Yes — full name in preview body (staff only, role-gated) |
| **Purpose** | Render personalised message body for staff review before send |

### `send_demo_message(lead_name, template_name, channel)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` — requires `_require_personalisation_access()` |
| **Returns PII?** | No |
| **Mutates?** | Yes — calls provider, creates Communication Log |
| **Demo fallback** | If provider credentials missing, log as `demo_mode = true`, `message_status = Simulated` |
| **Consent check** | Must verify consent before send; abort and log if not consented |

### `log_communication(lead_name, channel, template_name, message_status, provider_reference=None, failure_reason=None)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` (internal — called by send functions) |
| **Returns PII?** | No |
| **Mutates?** | Yes — creates Communication Log record |

### `get_communication_history(lead_name, limit=20)`

| Item | Detail |
|---|---|
| **Access** | `@frappe.whitelist()` — requires `_require_personalisation_access()` |
| **Returns PII?** | No — returns masked recipient only |
| **Purpose** | Return communication history for a lead (staff view) |

---

## Smoke Test: `scripts/smoke_test_phase_4.sh`

Must check:

```bash
# Baseline
Phase 1, 2, 3 smoke tests pass

# DocType
SmartLife Communication Log JSON exists
Required fields: lead, channel, recipient_masked, consent_snapshot, demo_mode

# Templates
Message template store/rules exist (file or DocType)
At least welcome_personal_details template defined
At least checkout_abandoned_reminder template defined

# APIs
get_message_templates defined
preview_message defined
send_demo_message defined
log_communication defined
get_communication_history defined

# Access control
send_demo_message is NOT allow_guest=True
preview_message is NOT allow_guest=True
get_communication_history is NOT allow_guest=True
send_demo_message calls _require_personalisation_access

# Consent enforcement
send_demo_message implementation checks consent_to_contact before send

# PII safety
recipient_masked field exists in Communication Log (not recipient or phone)
No raw phone/email in Communication Log list view fields

# Provider credentials
No Phahapa API key committed (grep for pattern)
No ZeptoMail API key committed

# Analytics
No PII in analytics events from Phase 4 code

# Python compile
All Phase 4 Python files compile

# Live route
/smartlife-staff-queue-full returns HTTP 200 (comms actions added there)
```

---

## Anti-Gravity Implementation Prompt

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 4 — Communications and Personalisation — exactly as specified in docs/phase_4_communications_personalisation_spec.md.

STOP CONDITIONS:
- Stop after Phase 4. Do not start Phase 5.
- Do not break Phases 1, 2, or 3.
- No outbound communication without consent_to_contact = true.
- Do not commit Phahapa or ZeptoMail credentials.
- Demo fallback (simulated send) must fire if credentials missing.

BEFORE YOU START:
1. Run: bash scripts/smoke_test.sh — must pass.
2. Run: bash scripts/smoke_test_phase_2.sh — must pass.
3. Run: bash scripts/smoke_test_phase_3.sh — must pass.
4. Review docs/phase_4_communications_personalisation_spec.md completely.

IMPLEMENTATION ORDER:
1. Create SmartLife Communication Log DocType.
2. Create message template store (SmartLife Personalisation Rule or static).
3. Add Phase 4 API endpoints to api.py (append only).
4. Update phahapa_sms_adapter.py and zeptomail_adapter.py with consent-gated send logic.
5. Create scripts/smoke_test_phase_4.sh.
6. Run bench migrate after DocType creation.
7. Run all four smoke tests.

ACCEPTANCE FORMAT:
Phase 4 complete.
[use standard format from anti_gravity_master_prompt.md]
```
