# NSSF SmartLife Flexi — Server Operator Validation Runbook

This guide is for the remote Frappe server operator validating the SmartLife Flexi voluntary growth system.

---

## 1. Pre-Flight Checks
Confirm local repository parameters before performing any merge:
```bash
# Go to the app directory
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

# Check branch status
git status --short
git branch --show-current
git fetch origin --prune
```
*Verify that the working tree is clean and the current branch matches the production branch (`phase-1-smartlife-onboarding`).*

---

## 2. Git Merge Operations
Merge the validated Claude branch (`claude/cool-bell-t7n0hs`) to the tracking branch:
```bash
git checkout phase-1-smartlife-onboarding
git pull origin phase-1-smartlife-onboarding
git merge origin/claude/cool-bell-t7n0hs --no-edit
```

Verify that the following commits exist in the merged git logs:
- `2c22e04` — Handoff documentation pack
- `d0e2786` — Phase 3 (Payment Readiness)
- `4339a7f` — Phase 4 (suppression messaging)
- `24d9b75` — Phase 5 (Command Centre)
- `f4e522a` — Phase 6 (Support Request)
- `5ab1b69` — Phase 7 (Privacy audit assets)

---

## 3. Bench Migration & Rebuild Sequence
Execute the Frappe schema sync, assets rebuilding, and supervisor restart:
```bash
cd /home/frappe/frappe-bench

# Sync database tables
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# Rebuild frontend files
bench build --app nssf_smart_savers

# Clear website cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

# Restart services
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
```

---

## 4. Run Sequential Smoke Validation Tests
Execute all smoke validation suites inside the app folder:
```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

bash scripts/smoke_test.sh
bash scripts/smoke_test_phase_2.sh
bash scripts/smoke_test_phase_3.sh
bash scripts/smoke_test_phase_4.sh
bash scripts/smoke_test_phase_5.sh
bash scripts/smoke_test_phase_6.sh
bash scripts/smoke_test_phase_7.sh
bash scripts/smoke_test_phase_8.sh
```
*Validation Success Criteria: Every suite must report `ALL PASSED` (0 failed).*

---

## 5. Manual Setup Verification Checklists
- **Personalisation Role Check**: Verify that `SmartLife Personalisation Team` exists in the Roles list.
- **Access Gates Checks**:
  - Visit `/smartlife-staff-queue-full`. Verify that Guest users see the sign-in gate and logged-in users require the team role.
  - Visit `/smartlife-command-centre`. Verify that Guest users are redirected to login.
- **Provider Settings Check**: Verify that site settings contain the relevant credentials keys (Pesapal, ZeptoMail, Phahapa SMS) in `site_config.json`.
