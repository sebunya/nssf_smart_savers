# Phase 6 Local Execution Notes — Support and Helpdesk

## Status
`Phase 6 local implementation complete / server validation pending`

---

## 1. What was Implemented Locally

- **Support Request DocType**: Designed the complete schema with 12 fields (`lead`, `session_id`, `support_category`, `preferred_contact_channel`, `message`, `status`, `assigned_staff`, `created_on`, `resolved_on`, `resolution_notes`, `consent_snapshot`, `demo_mode`).
- **Support categories**: Setup categories mapping to the spec (need help joining, understanding projections, contribution issues, diaspora, call requests, etc.).
- **User-Facing Form**: Updated `/smartlife-support-demo` HTML page with the exact 7 categories, preferred contact channel dropdown, and hooked up to the `create_support_request` API. On submit success, the generated support request reference name is rendered.
- **4 Support APIs**:
  - `create_support_request(session_id, support_category, message, preferred_contact_channel="")` (`allow_guest=True`): Creates support request and calls Helpdesk adapter integration safely.
  - `get_support_requests(status=None, limit=50)` (`allow_guest=False`): Authenticated staff queue listing (notes and messages omitted).
  - `assign_support_request(request_name, staff_name)` (`allow_guest=False`): Triage assignment endpoint.
  - `update_support_status(request_name, new_status, resolution_notes="")` (`allow_guest=False`): Status updating and resolution notes logging.
- **Soft Helpdesk Adapter Integration**: Connected `helpdesk_adapter.py` inside `create_support_request` to optionally insert an `HD Ticket` if available, falling back safely to a log event if not.
- **Phase 6 Smoke Test**: Created validation checks confirming DocType compile, categories match, whitelisting parameters, and PII boundaries are strictly guarded.

---

## 2. Files Changed or Created

* **New**: `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_support_request/__init__.py`
* **New**: `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_support_request/smartlife_support_request.py`
* **New**: `nssf_smart_savers/nssf_smart_savers/doctype/smartlife_support_request/smartlife_support_request.json`
* **New**: `scripts/smoke_test_phase_6.sh` (executable)
* **New**: `docs/phase_6_local_execution_notes.md`
* **Modified**: `nssf_smart_savers/www/smartlife-support-demo.html`
* **Modified**: `nssf_smart_savers/api.py`

---

## 3. What Could Not Be Validated Locally
- **Frappe DocType DB Sync**: The database structure and roles check require `bench migrate` to execute on the staging/production target environment.

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
bash scripts/smoke_test_phase_5.sh
bash scripts/smoke_test_phase_6.sh
```

All smoke tests must output `0 failed`.

---

## 5. Rollback Notes
If Phase 6 needs to be rolled back:
1. Revert changes in `api.py` and `smartlife-support-demo.html`.
2. Delete the `smartlife_support_request` DocType folder and the `scripts/smoke_test_phase_6.sh` test file.
3. Run `bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate` to drop the tables.
