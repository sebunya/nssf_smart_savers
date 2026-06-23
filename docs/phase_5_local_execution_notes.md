# Phase 5 Local Execution Notes — Command Centre and Analytics

## Status
`Phase 5 local implementation complete / server validation pending`

---

## 1. What was Implemented Locally

- **Command Centre Web Page**: Created `/smartlife-command-centre` route which includes a secure guest/role gate requiring `SmartLife Personalisation Team`, `NSSF Staff`, or `System Manager` role.
- **Privacy-Safe Dashboard UI**: The frontend displays aggregate charts and lists, featuring onboarding metrics, campaign performance, age distributions, drop-offs, and birth month metrics, with zero raw PII rendered.
- **6 Aggregate Analytics APIs**:
  - `get_command_centre_summary()`: Summary metrics (Total Leads, Details Completed, Projections, Checkout, Completed payments, Conversion rate) and staff metrics.
  - `get_conversion_funnel()`: Step-by-step conversion counts and percentages.
  - `get_dropoff_by_stage()`: Grouped counts of drop-offs per stage.
  - `get_lead_distribution(dimension)`: Safe fields only (`segment`, `goal`, `age_band`, `preferred_contact_channel`, `lead_temperature`, `gender`, `country`, `frequency`).
  - `get_campaign_performance()`: Lead sources and mediums.
  - `get_birth_month_distribution()`: Aggregated count 1-12. No birthdays shown.
- **Route Registration**: Configured `hooks.py` to register `/smartlife-command-centre`.
- **Phase 5 Smoke Test**: Created `scripts/smoke_test_phase_5.sh` confirming route template structure, whitelisted functions, access control decorators, PII safety checks, and Python compiling.

---

## 2. Files Changed or Created

* **New**: `nssf_smart_savers/www/smartlife-command-centre.py`
* **New**: `nssf_smart_savers/www/smartlife-command-centre.html`
* **New**: `scripts/smoke_test_phase_5.sh` (executable)
* **New**: `docs/phase_5_local_execution_notes.md`
* **Modified**: `nssf_smart_savers/api.py` (added 6 endpoints)
* **Modified**: `nssf_smart_savers/hooks.py` (added route mapping)

---

## 3. What Could Not Be Validated Locally
- **Live Database Grouping / Queries**: Real database execution of SQL functions (`group_by`, `count(name)`) relies on active MySQL/MariaDB schema tables.

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
```

All smoke tests must output `0 failed`.

---

## 5. Rollback Notes
If Phase 5 needs to be rolled back:
1. Revert changes in `api.py` and `hooks.py`.
2. Delete `smartlife-command-centre.html`, `smartlife-command-centre.py`, and `scripts/smoke_test_phase_5.sh`.
3. Clear bench cache and restart supervisor services.
