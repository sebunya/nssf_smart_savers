# Phase 3 — Payment and Contribution Readiness

**Status:** Not started  
**Depends on:** Phase 2 merged + `bench migrate` run on server + both smoke tests passing

---

## Objective

Make SmartLife Flexi ready for contribution intent tracking and sandbox/demo payment readiness without activating unsafe live payments. Extend the checkout flow with real payment lifecycle tracking using the Pesapal sandbox.

---

## Non-Negotiables

- Do not break Phase 1 or Phase 2
- Do not expose PII publicly
- Do not commit live Pesapal credentials — use environment variables or Frappe site config only
- Do not activate live payments unless explicitly configured with sandbox credentials and approved
- All payment behaviour must be sandbox/demo-safe by default
- If Pesapal credentials are missing, the checkout page must render a controlled demo fallback — never a traceback
- `bench migrate` must be run after creating `SmartLife Contribution Intent`

---

## New DocType: SmartLife Contribution Intent

**Purpose:** Track each payment attempt from checkout through to reconciliation.

### Fields

| Field | Type | Options / Notes |
|---|---|---|
| `lead` | Link → SmartLife Demo Lead | Required |
| `session_id` | Data | Anonymous session ID from lead |
| `saver_type` | Data | Copied from lead at creation |
| `contribution_amount` | Currency | |
| `contribution_frequency` | Select | Monthly, Weekly, Daily, Semi-annually, Annually, One-off |
| `payment_method` | Select | Mobile Money, Card, Bank Transfer, Other |
| `payment_status` | Select | Draft, Checkout Started, Pending, Completed, Failed, Cancelled, Reconciled |
| `payment_reference` | Data | PII — internal only, never analytics |
| `checkout_started_on` | Datetime | |
| `payment_completed_on` | Datetime | |
| `pesapal_tracking_id` | Data | Pesapal internal reference |
| `pesapal_merchant_reference` | Data | Merchant-side reference |
| `callback_status` | Data | Raw callback status code |
| `ipn_status` | Data | IPN verification status |
| `reconciliation_status` | Select | Pending, Matched, Discrepancy, Reconciled |
| `created_by_channel` | Select | Self-serve, Staff-assisted, Other |
| `demo_mode` | Check | Always 1 in prototype |
| `failure_reason` | Data | Human-readable failure description |

### Status lifecycle
`Draft` → `Checkout Started` → `Pending` → `Completed` / `Failed` / `Cancelled` → `Reconciled`

### Access model
- No guest can read raw payment references
- `get_contribution_intent` requires authenticated staff
- Callback/IPN handlers are `allow_guest=True` (Pesapal calls them from outside)
- IPN handler must validate signature before trusting payload

---

## New API Endpoints

### `create_payment_intent(session_id, amount, frequency, payment_method)`

| Item | Detail |
|---|---|
| **Purpose** | Create a `SmartLife Contribution Intent` record and return its name |
| **Access** | `allow_guest=True` (called from checkout page before redirect) |
| **Returns PII?** | No — returns intent_name and session_id only |
| **Mutates?** | Yes — creates DocType record |
| **Demo fallback** | If lead not found by session_id, return `{"success": false, "message": "Session not found"}` |
| **Failure behaviour** | Never traceback — return structured error |
| **Tests** | intent created with correct fields; status = Draft; session_id matches lead |

### `initiate_pesapal_checkout(intent_name)`

| Item | Detail |
|---|---|
| **Purpose** | Call Pesapal API to create order and return redirect URL |
| **Access** | `allow_guest=True` |
| **Returns PII?** | No — returns redirect URL only |
| **Mutates?** | Yes — updates intent status to Checkout Started, stores tracking_id |
| **Demo fallback** | If Pesapal credentials missing, return `{"success": false, "demo_mode": true, "message": "Sandbox credentials not configured — demo fallback active"}` and render simulated response |
| **Failure behaviour** | Never traceback; log error to SmartLife Integration Event |
| **Tests** | Fallback fires when credentials absent; status updated on success |

### `handle_pesapal_callback(OrderTrackingId, OrderMerchantReference)`

| Item | Detail |
|---|---|
| **Purpose** | Receive Pesapal redirect callback after user payment action |
| **Access** | `allow_guest=True` (Pesapal redirects user here) |
| **Returns PII?** | No |
| **Mutates?** | Yes — updates callback_status on intent |
| **Demo fallback** | If intent not found, redirect to `/smartlife-thank-you?status=unknown` |
| **Failure behaviour** | Redirect user gracefully — never show traceback |
| **Tests** | Callback updates intent; missing intent handled gracefully |

### `handle_pesapal_ipn(OrderTrackingId, OrderMerchantReference, OrderNotificationType)`

| Item | Detail |
|---|---|
| **Purpose** | Receive Pesapal IPN (server-to-server notification) and verify payment |
| **Access** | `allow_guest=True` (Pesapal posts from their servers) |
| **Returns PII?** | No |
| **Mutates?** | Yes — calls verify_payment_status, updates ipn_status and payment_status |
| **Demo fallback** | Log IPN payload to SmartLife Integration Event; return HTTP 200 to Pesapal |
| **Failure behaviour** | Must return HTTP 200 to Pesapal regardless — log errors internally |
| **Tests** | IPN verified; status updated to Completed on valid payload |

### `verify_payment_status(intent_name)`

| Item | Detail |
|---|---|
| **Purpose** | Query Pesapal API to check current payment status for an intent |
| **Access** | `@frappe.whitelist()` (authenticated staff only) |
| **Returns PII?** | No |
| **Mutates?** | Yes — updates payment_status if changed |
| **Demo fallback** | If credentials missing, return simulated Completed status |
| **Failure behaviour** | Return current status from DB if API call fails |
| **Tests** | Status returned correctly; auth guard enforced |

### `get_contribution_intent(intent_name)`

| Item | Detail |
|---|---|
| **Purpose** | Return contribution intent details for staff view |
| **Access** | `@frappe.whitelist()` (authenticated staff, full detail requires personalisation role) |
| **Returns PII?** | Payment reference is internal — mask in public contexts |
| **Mutates?** | No |
| **Demo fallback** | N/A |
| **Tests** | Returns correct fields; auth enforced |

---

## Checkout UX — `/smartlife-checkout-demo` Enhancements

Enhance the existing checkout page with:

- **Plan summary card**: saver type, selected goal, goal label, target amount, years
- **Contribution details**: amount (UGX), frequency, payment method selector
- **Projection summary**: expected value at maturity (from `get_projection`)
- **Prototype/sandbox notice**: "This is a demo environment. No real payment will be processed." — always visible
- **Payment status display**: updates after callback/IPN (polling or redirect)
- **Continue / Retry button**: enabled after payment status = Completed; shows retry on Failed
- **Safe demo fallback**: if Pesapal credentials are missing, show simulated "Payment Accepted" response with clear demo label — never a traceback

Do not remove the existing checkout content. Add to it.

---

## Smoke Test: `scripts/smoke_test_phase_3.sh`

Must check:

```bash
# Baseline
Phase 1 smoke test passes
Phase 2 smoke test passes

# DocType
SmartLife Contribution Intent JSON exists
Required fields present: lead, session_id, payment_status, demo_mode, pesapal_tracking_id

# APIs in api.py
create_payment_intent defined
initiate_pesapal_checkout defined
handle_pesapal_callback defined
handle_pesapal_ipn defined
verify_payment_status defined
get_contribution_intent defined

# Access control
verify_payment_status is NOT allow_guest=True
get_contribution_intent is NOT allow_guest=True
handle_pesapal_ipn IS allow_guest=True (Pesapal posts to it)
handle_pesapal_callback IS allow_guest=True

# Adapters
pesapal_adapter.py exists
pesapal_adapter.py compiles

# Credential safety
No Pesapal live credentials in source (no sk_live, PESAPAL_KEY, PESAPAL_SECRET patterns)

# Route
checkout-demo route exists (HTML file present)
checkout-demo HTML contains prototype/sandbox notice
checkout-demo HTML contains demo-mode fallback message

# No PII leakage
payment_reference not in ALLOWED_PARAMS
No PII in analytics events

# Python compile
All Phase 3 Python files compile

# Live route (on server after migrate)
/smartlife-checkout-demo returns HTTP 200
```

---

## Anti-Gravity Implementation Prompt

Copy-paste this prompt to implement Phase 3 only:

```
You are working on the Frappe app nssf_smart_savers (repository: sebunya/nssf_smart_savers, branch: claude/cool-bell-t7n0hs).

MISSION: Implement Phase 3 — Payment and Contribution Readiness — exactly as specified in docs/phase_3_payment_contribution_readiness_spec.md.

STOP CONDITIONS:
- Stop after Phase 3. Do not start Phase 4.
- Do not break Phase 1 or Phase 2.
- Do not commit Pesapal live credentials.
- Do not activate live payments.
- Demo fallback must fire if credentials are missing.

BEFORE YOU START:
1. Run: bash scripts/smoke_test.sh — must pass.
2. Run: bash scripts/smoke_test_phase_2.sh — must pass.
3. Review docs/phase_3_payment_contribution_readiness_spec.md completely.
4. Review docs/anti_gravity_handoff.md for architecture context.

IMPLEMENTATION ORDER:
1. Create SmartLife Contribution Intent DocType JSON + Python (no fields removed from SmartLife Demo Lead).
2. Add Phase 3 API endpoints to api.py (append only — do not modify existing endpoints).
3. Enhance /smartlife-checkout-demo with plan summary, contribution details, sandbox notice, demo fallback.
4. Update pesapal_adapter.py with sandbox implementation.
5. Create scripts/smoke_test_phase_3.sh.
6. Run bench migrate (on server) after DocType creation.
7. Run all three smoke tests.

ACCEPTANCE FORMAT:
Phase 3 complete.

Files changed:
- ...

DocTypes changed:
- ...

Routes added:
- ...

APIs added:
- ...

Tests added:
- ...

Smoke tests:
- Phase 1: X passed | 0 failed
- Phase 2: X passed | 0 failed
- Phase 3: X passed | 0 failed

Commit:
- <hash> Add SmartLife Phase 3 payment and contribution readiness

Risks:
- ...
```
