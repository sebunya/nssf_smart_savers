# Anti-Gravity Validation Runbook

**For:** Google Anti-Gravity (coding agent) and human/server operator  
**Purpose:** Exact commands to validate the SmartLife Flexi app at every checkpoint

---

## Before Starting Any Phase

Run all of these. Every command must succeed before starting work.

```bash
# 1. Navigate to app root
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

# 2. Check git status and branch
git status
git --no-pager log --oneline --decorate -15

# 3. Confirm on correct branch
git branch --show-current
# Expected: claude/cool-bell-t7n0hs (or the active development branch)

# 4. Python compile check — all files in app
python3 -m compileall nssf_smart_savers -q
# Expected: no errors

# 5. Smoke test syntax checks
bash -n scripts/smoke_test.sh
bash -n scripts/smoke_test_phase_2.sh
# Expected: no syntax errors (bash -n exits 0)

# 6. Live smoke tests
./scripts/smoke_test.sh
./scripts/smoke_test_phase_2.sh
# Expected: Phase 1: ≥140 passed | 0 failed
#           Phase 2: ≥99 passed | 0 failed (network warns are acceptable)
```

**If any of the above fails: STOP. Do not start the phase. Fix the regression first.**

---

## After Every DocType Change (bench migrate required)

Run as the `frappe` user on the server after merging or adding any DocType JSON changes:

```bash
cd /home/frappe/frappe-bench

# 1. Migrate database (picks up new/changed DocType fields)
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# 2. Build app assets
bench build --app nssf_smart_savers

# 3. Clear all caches
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

# 4. Restart web and worker processes
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:

# 5. Reload Nginx
sudo service nginx reload

# 6. Verify services are running
sudo supervisorctl status frappe-bench-web:
```

**DocTypes that required migrate so far:**
- Phase 2: `staff_notes`, `lead_status`, `lead_temperature`, `lead_score`, `next_best_action`, lifecycle, attribution, and journey flag fields on `SmartLife Demo Lead`
- Phase 3: `SmartLife Contribution Intent` (new DocType — migrate required)
- Phase 4: `SmartLife Communication Log` (new DocType — migrate required)
- Phase 6: `SmartLife Support Request` (new DocType — migrate required)

---

## Merging Phase 2 Into Production (Pre-Phase 3 Server Action)

This must be done by a human with server access before Anti-Gravity starts Phase 3.

```bash
# SSH to server
ssh frappe@nssf-smartlifeflexi.nile-gov-demo.com

cd /home/frappe/frappe-bench

# Fetch latest Claude branch
git -C apps/nssf_smart_savers fetch origin claude/cool-bell-t7n0hs

# Switch to production branch
git -C apps/nssf_smart_savers checkout phase-1-smartlife-onboarding

# Check what will be merged
git -C apps/nssf_smart_savers log --oneline origin/claude/cool-bell-t7n0hs ^HEAD

# Merge Phase 2 changes
git -C apps/nssf_smart_savers merge origin/claude/cool-bell-t7n0hs

# Run migration and restart (see "After Every DocType Change" section above)
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

# Run smoke tests on server
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
./scripts/smoke_test.sh
./scripts/smoke_test_phase_2.sh
# Both must show 0 failed before Phase 3 starts
```

---

## Route Proof Commands

Run these manually or in CI to confirm all routes return HTTP 200.

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

# Phase 1 routes
for ROUTE in /smartlife-flexi-demo /smartlife-self-serve /smartlife-staff-assist \
             /smartlife-projection-demo /smartlife-checkout-demo \
             /smartlife-thank-you /smartlife-support-demo; do
  CODE=$(curl -ksS -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$ROUTE")
  echo "$CODE $ROUTE"
done

# Phase 2 routes
for ROUTE in /smartlife-staff-queue /smartlife-staff-queue-full; do
  CODE=$(curl -ksS -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$ROUTE")
  echo "$CODE $ROUTE"
done

# Phase 5 route (after Phase 5 is deployed)
CODE=$(curl -ksS -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/smartlife-command-centre")
echo "$CODE /smartlife-command-centre"
```

Expected: all return `200`. Phase 2 routes return 200 with a guest gate — not a block.

---

## Smoke Test Order (Always Run in This Order)

```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

./scripts/smoke_test.sh              # Phase 1 baseline
./scripts/smoke_test_phase_2.sh      # Phase 2 (after Phase 2 merged)
./scripts/smoke_test_phase_3.sh      # Phase 3 (after Phase 3 implemented)
./scripts/smoke_test_phase_4.sh      # Phase 4 (after Phase 4 implemented)
./scripts/smoke_test_phase_5.sh      # Phase 5 (after Phase 5 implemented)
./scripts/smoke_test_phase_6.sh      # Phase 6 (after Phase 6 implemented)
./scripts/smoke_test_phase_7.sh      # Phase 7 (after Phase 7 implemented)
```

**Failure rule:** If any previous phase smoke test fails after a new phase is implemented, stop immediately. Fix the regression before continuing. Never add a phase on top of a failing previous-phase baseline.

---

## Checking the PII Block List

### Server-side ALLOWED_PARAMS (Python AST check)

```bash
python3 -c "
import ast

src = open('nssf_smart_savers/utils/analytics.py').read()
tree = ast.parse(src)

allowed = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'ALLOWED_PARAMS':
                allowed = [
                    e.value for e in node.value.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                ]

PII_KEYS = {
    'first_name','last_name','full_name','phone','primary_phone',
    'email','nin','national_id','date_of_birth','dob',
    'birthday_day','birthday_month','age_years','exact_age',
    'staff_notes','notes','remarks','raw_remarks',
    'user_submitted_text','free_text',
}

bad = PII_KEYS.intersection(set(allowed))
if bad:
    print('FAIL: PII in ALLOWED_PARAMS:', sorted(bad))
else:
    print('PASS: ALLOWED_PARAMS is PII-free. Count:', len(allowed))
"
```

### Frontend PII_KEYS check

```bash
grep "PII_KEYS" nssf_smart_savers/public/js/analytics_helper.js
# Expected: var PII_KEYS = [ ... ] with first_name, last_name, primary_phone,
#           birthday_day, birthday_month, age_years, nin, etc.
```

---

## Checking the Role Guard

```bash
# Confirm role constant exists
grep -n "ALLOWED_PERSONALISATION_ROLES" nssf_smart_savers/api.py

# Confirm _has_allowed_personalisation_role calls frappe.get_roles
grep -n "frappe.get_roles" nssf_smart_savers/api.py

# Confirm full-PII endpoints are not allow_guest
python3 -c "
import ast, sys
src = open('nssf_smart_savers/api.py').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name in ('get_staff_queue_full', 'get_lead_full_detail'):
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == 'allow_guest' and isinstance(kw.value, ast.Constant) and kw.value.value:
                        print('FAIL:', node.name, 'is allow_guest=True')
                        sys.exit(1)
        print('PASS:', node.name, 'is not allow_guest')
"
```

---

## Confirming Guest Gate on Full-PII Routes

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

# Fetch as guest and confirm sign-in gate renders (not data)
curl -sSL --max-time 10 "$BASE/smartlife-staff-queue-full" | grep -i "sign-in\|authorised\|access restricted"
# Expected: contains "Staff sign-in required" or "Access restricted"

# Confirm page does NOT contain raw phone patterns
curl -sSL --max-time 10 "$BASE/smartlife-staff-queue-full" | grep -Eo "07[0-9]{8}" | head -5
# Expected: no output (no raw phone numbers in guest response)
```

---

## Checking Python Syntax Across All App Files

```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
python3 -m compileall nssf_smart_savers -q
# Expected: exits 0, no output (or "Compiling..." lines with no errors)

# Check specific files
for f in nssf_smart_savers/api.py \
          nssf_smart_savers/lead_scoring.py \
          nssf_smart_savers/utils/analytics.py \
          nssf_smart_savers/utils/privacy.py \
          nssf_smart_savers/utils/safe_input.py \
          nssf_smart_savers/www/smartlife-staff-queue-full.py; do
  python3 -m py_compile "$f" && echo "OK: $f" || echo "FAIL: $f"
done
```

---

## Checking for Committed Credentials

```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

# Credential pattern scan
grep -rEn "sk_live|pk_live|SECRET_KEY|PRIVATE_KEY|PESAPAL_SECRET|PHAHAPA_KEY|ZEPTOMAIL_TOKEN|API_KEY\s*=" \
  nssf_smart_savers/ scripts/ docs/ 2>/dev/null
# Expected: no output

# Also check for any .env files accidentally committed
git ls-files | grep -E "\.env$|credentials"
# Expected: no output
```

---

## Phase-Specific Validation Triggers

| Phase | Trigger for migrate | Trigger for bench build | New smoke test |
|---|---|---|---|
| Phase 2 merge | Yes — new SmartLife Demo Lead fields | Yes | smoke_test_phase_2.sh |
| Phase 3 | Yes — SmartLife Contribution Intent | Yes | smoke_test_phase_3.sh |
| Phase 4 | Yes — SmartLife Communication Log | Yes | smoke_test_phase_4.sh |
| Phase 5 | No new DocTypes | Yes (new route) | smoke_test_phase_5.sh |
| Phase 6 | Yes — SmartLife Support Request | Yes | smoke_test_phase_6.sh |
| Phase 7 | No DocTypes | Maybe (if fixes needed) | smoke_test_phase_7.sh |
| Phase 8 | No | No | None (all previous) |
