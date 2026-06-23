# NSSF SmartLife Flexi — Release Rollback Plan

Guidelines to revert the system in case of staging or production validation failures.

---

## 1. Rollback Decision Triggers
A rollback must be initiated immediately if:
- Schema migration (`bench migrate`) fails with unrecoverable database errors.
- Any baseline smoke test (Phases 1–6) fails with unresolved regressions.
- Internal member PII (raw phone numbers, names, or DOBs) is leaked to guest routes or public analytics pipelines.
- Production environment configurations trigger traceback logs in public forms.

---

## 2. Backup Protocol (Pre-requisite)
Before performing any deployment operations, the server operator must run:
```bash
cd /home/frappe/frappe-bench

# Perform site backup (creates database SQL and public files archive)
bench --site nssf-smartlifeflexi.nile-gov-demo.com backup --with-files
```

---

## 3. Reversion Operations
To rollback changes to the prior stable production commit:
```bash
# Go to app directory
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

# Hard reset tracking branch to previous production commit
git reset --hard phase-1-smartlife-onboarding@{1}
```

If database rollback is required (e.g. dropping columns or tables created during migrate):
```bash
cd /home/frappe/frappe-bench

# Re-migrate schema to previous status
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# Re-build assets
bench build --app nssf_smart_savers

# Clear caching
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

# Restart supervisor services
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
```

---

## 4. Post-Rollback Validation
Re-run baseline smoke tests to ensure the system is restored to its working state:
```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
```
All tests must report `ALL PASSED`.
