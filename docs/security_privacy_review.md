# NSSF SmartLife Flexi — Security & Privacy Review

## 1. Scope of Review
This report reviews the security and privacy controls of the voluntary saving growth prototype (`nssf_smart_savers` app) built on Frappe v15.

Modules audited:
- Onboarding (Phases 1 & 2)
- Payment/Checkout Integration (Phase 3)
- Communications Suppression & Personalisation (Phase 4)
- Command Centre Analytics (Phase 5)
- Support & Helpdesk (Phase 6)

---

## 2. PII Inventory
The following data elements represent customer PII or sensitive operational information.

| PII Data Element | Stored in DB? | Returned in Public APIs? | Returned in Staff Queue? | Protection / Masking Approach |
|---|---|---|---|---|
| `first_name` | Yes | No | Yes (unmasked) | Only visible in auth-guarded staff views. |
| `last_name` | Yes | No | Yes (unmasked) | Only visible in auth-guarded staff views. |
| `full_name` | Derived | No | Yes (unmasked) | Only visible in auth-guarded staff views. |
| `primary_phone` | Yes | No | Yes (masked) | Masked (`070****545`) in public queue; raw in full staff queue. |
| `email_address` | Yes | No | Yes (masked) | Masked (`ro***@domain.com`) in public queue; raw in full staff queue. |
| `date_of_birth` | Yes | No | Yes | Only returned in auth-guarded staff views. |
| `birthday_day` | Yes | No | Yes | Used for DOB calculation; masked in public views. |
| `birthday_month` | Yes | No | Yes | Used for DOB calculation; masked in public views. |
| `nin` | Yes | No | Yes | Restructured or blank in public views. |
| `payment_reference`| Yes | No | Yes | Never returned in analytics; protected by auth gate. |
| `message` | Yes | No | Yes | Support requests are not visible in public queues. |
| `resolution_notes`| Yes | No | No | Strictly internal notes; never returned to any client views. |

---

## 3. API Access-Control & Guest Endpoint Audit
All SmartLife endpoints are `@frappe.whitelist()`. The access model is detailed below:

### Guest-Open Endpoints (`allow_guest=True`)
Guest endpoints are strictly limited to onboarding submissions and support creations:
1. `get_projection()`: Input calculator parameters. Returns numeric projections.
2. `get_personalised_plan_api()`: Onboarding advisor. Returns plan metrics.
3. `submit_demo_lead()`: Creates lead. Sanitizes name/email and returns session ID.
4. `create_payment_intent()`: Prepares transaction records. Returns checkout reference.
5. `initiate_pesapal_checkout()`: Performs sandbox/demo order submit. Returns redirect URL.
6. `handle_pesapal_callback()`: Redirect target. Validates payment state.
7. `handle_pesapal_ipn()`: Backend IPN receiver. Silent handler returns ok status.
8. `get_message_templates()`: Retrives standard notification details. No customer PII.
9. `create_support_request()`: Guest support submission. Sanitizes inputs and returns request reference name only.

### Staff-Only Endpoints (Guest Access Blocked)
All other APIs require active authentication. Access control is enforced server-side:
1. `get_lead_summary()` & `get_staff_queue()`: Returns masked lead priorities.
2. `get_staff_queue_full()`: Requires `_require_personalisation_access()`. Returns unmasked PII.
3. `get_lead_full_detail()`: Requires `_require_personalisation_access()`. Returns full PII.
4. `update_follow_up_status()`: Requires authenticated session. Writes notes.
5. `assign_lead()` & `update_journey_flag()`: Staff queue management writes.
6. `verify_payment_status()` & `get_contribution_intent()`: Retrieves payment details.
7. `preview_smartlife_message()` & `send_smartlife_demo_message()`: Message control actions.
8. `get_communication_history()` & `get_messaging_config_status()`: History logs.
9. `get_command_centre_summary()` & `get_conversion_funnel()` & `get_dropoff_by_stage()` & `get_lead_distribution()` & `get_campaign_performance()` & `get_birth_month_distribution()`: Command Centre aggregate analytics.
10. `get_support_requests()` & `assign_support_request()` & `update_support_status()`: Support ticket workflow.

---

## 4. Double-Enforcement Analytics PII Blocks
Analytics PII block is enforced independently on the backend and frontend:
1. **Backend Allowlist**: `utils/analytics.py` maintains `ALLOWED_PARAMS`. Any key not present in this list is silently dropped by `sanitise_event_params()`.
2. **Frontend Blocklist**: `analytics_helper.js` blocks client-side tracking calls containing sensitive keys (`first_name`, `last_name`, `phone`, `email`, `nin`, `date_of_birth`, etc.).

---

## 5. Secrets and Configuration Hygiene
- **No Hardcoded Secrets**: Pesapal, ZeptoMail, and Phahapa configurations are read dynamically from `frappe.conf` (e.g. `pesapal_consumer_key`, `smartlife_zeptomail_token`) or environment variables.
- **Fail-Safe Fallbacks**: If keys are not configured, adapters silently switch to demo mode (`demo_mode = 1`) returning simulated parameters rather than throwing fatal connection errors.

---

## 6. Logs & Traceback Protection
- **No Browser Tracebacks**: All exceptions inside whitelisted guest endpoints are intercepted. Fatal stack tracebacks are not exposed to public users; instead, sanitized JSON objects with default error notices are returned.
- **PII-Safe Logging**: Error logs (`frappe.log_error`) record document names and status triggers rather than capturing raw PII inputs.

---

## 7. Open TODOs for Staging/Production Deployment
1. **Manual Role Setup**: Before full-PII queues are usable, the `SmartLife Personalisation Team` role must be created in Frappe:
   - Go to **Role List** → **New**.
   - Set Name to `SmartLife Personalisation Team`.
   - Add role permissions on `SmartLife Demo Lead`, `SmartLife Contribution Intent`, `SmartLife Communication Log`, and `SmartLife Support Request` as defined.
2. **Setup Rate Limiting**: Enable nginx-level or Redis rate limiting on high-frequency guest endpoints (`submit_demo_lead`, `submit_personal_details`, `create_support_request`).
3. **Purge Script**: Implement a recurring bench console script to purge old simulated demo entries from database tables.
4. **Data Protection Officer Sign-off**: Real deployment requires DPO approval on retention periods and data processing agreements with ZeptoMail/Phahapa.
