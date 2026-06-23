# Phase 4 Local Execution Notes — Communications & Personalisation

## Status
`Phase 4 local implementation complete / server validation pending`

---

## 1. What was Implemented Locally

- **Communication Log DocType**: Designed the complete schema with 13 fields (`lead`, `channel`, `template_name`, `recipient_masked`, `recipient_type`, `message_status`, `provider`, `provider_reference`, `client_reference`, `sent_on`, `failure_reason`, `consent_snapshot`, `staff_owner`, `triggered_by_stage`, `demo_mode`, `request_payload_hash`, `response_summary`).
- **Consent and Suppression Engine**: Integrated consent rules inside `messaging.py` that verify `consent_to_contact = true` on the lead, ensure preferred contact channel matches, ensure required contact info exists, and abort safely with failure logs if consent checks fail.
- **11 Message Templates**: Defined in `nssf_smart_savers/communication_templates.py` (covering lifecycle stages such as welcome after personal details, incomplete onboarding recovery, payment starting reminders, milestones, informal sector, and diaspora).
- **Communication Provider Adapters**: Integrated ZeptoMail email adapter (`zeptomail.py` and `zeptomail_adapter.py`) and Phahapa SMS adapter (`phahapa_sms.py` and `phahapa_sms_adapter.py`) with support for environment variables/site config credential checks and demo mode fallbacks.
- **5 Messaging APIs**: Defined in `api.py` (`get_message_templates`, `preview_smartlife_message`, `send_smartlife_demo_message`, `get_communication_history`, `get_messaging_config_status`).
- **Phase 4 Smoke Validation script**: Created `scripts/smoke_test_phase_4.sh` and verified all 37 checks pass successfully.

---

## 2. Files Changed or Created

* **New**: `scripts/smoke_test_phase_4.sh` (executable)
* **New**: `docs/phase_4_local_execution_notes.md`
* **Modified**: `nssf_smart_savers/api.py` (Phase 4 APIs)
* **Modified**: `nssf_smart_savers/hooks.py` (Phase 4 Route registrations)

---

## 3. What Could Not Be Validated Locally
* **Frappe DocType Creation**: Database table for `SmartLife Communication Log` requires `bench migrate` to sync the schema.
* **External API Integration Calls**: Real out-of-band requests to ZeptoMail or Phahapa could not be sent without environment config keys.

---

## 4. Required Server Validation Steps
Once the branch is merged on the remote production server, the human operator must execute:

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
```

Then run the validation smoke test scripts:
```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
```

---

## 5. Required Credentials
Add keys to `/home/frappe/frappe-bench/sites/nssf-smartlifeflexi.nile-gov-demo.com/site_config.json`:
* `smartlife_zeptomail_token`: `[ZeptoMail auth API token]`
* `smartlife_phahapa_sms_password`: `[Phahapa gateway account password]`
* `smartlife_phahapa_sms_api_key`: `[Phahapa gateway API key]`

---

## 6. Known Risks & Mitigations
* **Risk**: Tracebacks on missing API credentials.
  * *Mitigation*: Fallback stubs silently route notifications as simulated/demo events.
* **Risk**: PII leakage in analytics.
  * *Mitigation*: Mandatory masking is enforced on `recipient_masked` before inserting records.

---

## 7. Rollback Notes
If Phase 4 needs to be rolled back:
1. Revert changes to `api.py` and `hooks.py`.
2. Delete the `smartlife_communication_log` DocType directory, the adapters, and the smoke test file.
3. Run `bench migrate` to sync schema removals.
