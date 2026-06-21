# NSSF SmartLife Flexi — Final Production Deployment Runbook

**Site:** `nssf-smartlifeflexi.nile-gov-demo.com`
**App path:** `/home/frappe/frappe-bench/apps/nssf_smart_savers`
**Production branch:** `phase-1-smartlife-onboarding`
**Claude feature branch:** `claude/cool-bell-t7n0hs`

**Golden rule:** Do not run Git as `root`. Run Git as `frappe`. Do not judge success from browser view alone. Prove source, origin, public URL, live CSS, smoke test and browser separately.

---

## STEP 1 — Merge latest Claude work into production branch

Run from root:

```bash
sudo -u frappe -H bash -lc '
set -euo pipefail

APP="/home/frappe/frappe-bench/apps/nssf_smart_savers"

cd "$APP"

export GIT_PAGER=cat
export PAGER=cat

echo "=============================="
echo "PRE-FLIGHT"
echo "=============================="
echo "USER=$(whoami)"
echo "PWD=$(pwd)"
echo "BRANCH=$(git branch --show-current)"

git --no-pager status
git --no-pager log --oneline --decorate -8

echo "=============================="
echo "FETCH LATEST"
echo "=============================="
git fetch origin

echo "=============================="
echo "CHECKOUT TARGET BRANCH"
echo "=============================="
git checkout phase-1-smartlife-onboarding

echo "=============================="
echo "ENSURE WORKING TREE IS CLEAN"
echo "=============================="
if [ -n "$(git status --porcelain)" ]; then
  echo "STOP: Working tree is dirty. Commit, stash, or inspect before deployment."
  git status
  exit 1
fi

echo "=============================="
echo "UPDATE TARGET BRANCH"
echo "=============================="
git pull --ff-only origin phase-1-smartlife-onboarding

echo "=============================="
echo "MERGE CLAUDE FEATURE BRANCH"
echo "=============================="
git merge --no-ff origin/claude/cool-bell-t7n0hs \
  -m "Merge final NSSF brand DOB onboarding and deployment runbook" || {
  echo "STOP: Merge failed. Resolve conflicts before deployment."
  git status
  exit 1
}

echo "=============================="
echo "POST-MERGE STATUS"
echo "=============================="
git --no-pager status
git --no-pager log --oneline --decorate -12

echo "=============================="
echo "PUSH TARGET BRANCH"
echo "=============================="
git push origin phase-1-smartlife-onboarding
'
```

**Expected result:**
- Branch is `phase-1-smartlife-onboarding`
- Working tree is clean
- Log includes the latest Claude branch work
- Push succeeds

**Do not continue if this step fails.**

---

## STEP 2 — Deploy on Frappe

```bash
cd /home/frappe/frappe-bench

bench --site nssf-smartlifeflexi.nile-gov-demo.com backup --with-files

bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

bench build --app nssf_smart_savers

bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache

sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload

sudo supervisorctl status | egrep "frappe-bench-web|frappe-bench-workers"
```

**Expected result:**
- Backup succeeds
- Migration succeeds
- Build succeeds
- Web and workers restart
- Supervisor status shows running services

---

## STEP 3 — Prove source on disk is correct

```bash
sudo -u frappe -H bash -lc '
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

echo "=============================="
echo "SOURCE COMMIT"
echo "=============================="
git --no-pager log --oneline --decorate -8

echo "=============================="
echo "DOB SOURCE CHECK"
echo "=============================="
grep -R "date_of_birth\|Date of birth\|birthday_month\|birthday_day" -n \
  nssf_smart_savers/www nssf_smart_savers/api.py nssf_smart_savers/doctype | head -80

echo "=============================="
echo "NSSF COLOUR SOURCE CHECK"
echo "=============================="
grep -E "#002060|#0F2C59|#00AEEF|#00A3E0|#00A859|#107C41" \
  nssf_smart_savers/public/css/smartlife.css

echo "=============================="
echo "ASSET VERSION SOURCE CHECK"
echo "=============================="
grep -R "nssf-brand-dob-ui-20260622" -n \
  nssf_smart_savers/www nssf_smart_savers/templates | head -80
'
```

**Expected result:**
- DOB fields appear in source
- `birthday_month` and `birthday_day` appear
- NSSF colours appear in CSS
- Versioned asset string appears in templates

---

## STEP 4 — Prove origin HTML is correct

This bypasses Cloudflare and checks what Frappe is serving locally.

```bash
curl -fsSL -H "Host: nssf-smartlifeflexi.nile-gov-demo.com" \
  "http://127.0.0.1/smartlife-self-serve?origin-proof=$(date +%s)" \
| grep -E "smartlife.css|smartlife.js|sl-choice-card|sl-stepper|\
Your Personal Details|Date of birth|Existing NSSF Member|\
New Saver|Diaspora Saver|Informal Sector|Staff-Assisted"
```

**Expected result:** It must print matching HTML lines.

If this fails, the problem is Frappe rendering, not Cloudflare. Re-run migrate, build, clear-cache, clear-website-cache and restart.

---

## STEP 5 — Prove public HTML is correct

This checks the URL NSSF will actually see.

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

curl -fsSL "$BASE/smartlife-self-serve?v=public-proof-$(date +%s)" \
| grep -E "smartlife.css|smartlife.js|sl-choice-card|sl-stepper|\
Your Personal Details|Date of birth|Existing NSSF Member|\
New Saver|Diaspora Saver|Informal Sector|Staff-Assisted"
```

**Expected result:** It must print matching HTML lines.

If origin passes but public fails, the issue is Cloudflare cache. Purge Cloudflare cache for `nssf-smartlifeflexi.nile-gov-demo.com`, then rerun the public proof with a fresh `?v=` value.

---

## STEP 6 — Prove live CSS has NSSF colours

```bash
curl -fsSL "$BASE/assets/nssf_smart_savers/css/smartlife.css?v=colour-proof-$(date +%s)" \
| grep -E "#002060|#0F2C59|#00AEEF|#00A3E0|#00A859|#107C41"
```

**Expected result:** It must show the NSSF colour values.

If this fails, the CSS file being served is stale. Run:

```bash
cd /home/frappe/frappe-bench
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
sudo supervisorctl restart frappe-bench-web:
sudo service nginx reload
```

Then test again.

---

## STEP 7 — Run smoke test

```bash
sudo -u frappe -H bash -lc '
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
export GIT_PAGER=cat PAGER=cat
./scripts/smoke_test.sh
'
```

**Expected result:**
- Routes pass
- Assets pass
- Rendered HTML checks pass
- DOB checks pass
- NSSF colour checks pass
- PII analytics block-list checks pass

If smoke test fails but Steps 4, 5 and 6 pass, inspect whether the smoke test is too brittle. Do not change good product copy just to satisfy an outdated string check.

---

## STEP 8 — Test DOB API with dummy data only

```bash
curl -sS -X POST "$BASE/api/method/nssf_smart_savers.api.submit_personal_details" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Demo",
    "last_name": "Saver",
    "date_of_birth": "1994-06-15",
    "gender": "Male",
    "primary_phone": "256700000000",
    "alternative_phone": "",
    "email": "demo@example.com",
    "country_of_residence": "Uganda",
    "preferred_contact_channel": "SMS",
    "consent_to_contact": 1,
    "saver_type": "new_saver"
  }'
```

**The response may return:**
- success / status
- session id or lead reference
- age band

**The response must not return:**
- full name
- phone
- email
- DOB
- exact age
- birthday day
- birthday month

---

## STEP 9 — Verify DocType fields in Frappe

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com console
```

Inside the console, paste:

```python
import frappe

fields = [f.fieldname for f in frappe.get_meta("SmartLife Demo Lead").fields]

missing = [x for x in [
    "date_of_birth",
    "age_years",
    "age_band",
    "birthday_month",
    "birthday_day",
    "gender",
    "primary_phone",
    "alternative_phone",
    "email",
    "country_of_residence",
    "preferred_contact_channel",
    "consent_to_contact"
] if x not in fields]

missing
```

**Expected result:**

```python
[]
```

Exit:

```python
exit()
```

---

## STEP 10 — Browser acceptance test

Open:

```
https://nssf-smartlifeflexi.nile-gov-demo.com/smartlife-self-serve?v=final-nssf-dob-brand
```

Use Incognito or hard refresh. Mac Chrome: `Cmd + Shift + R`

**Confirm visually:**
- NSSF navy dominates headings and structure
- NSSF green is used for CTAs, selected cards and active stepper
- Sky blue appears as accent/focus colour
- Cards are styled
- Stepper is styled
- Forms are styled
- Step 2 says "Date of birth"
- There is no manual age input
- DOB selection shows calculated age preview
- Next button works
- No PII appears in URL
- Browser console has no fatal JavaScript errors

---

## Troubleshooting logic

| Symptom | Cause | Fix |
|---|---|---|
| Origin curl fails | Frappe serving old HTML | Check branch + commit, then migrate / build / clear-cache / restart |
| Origin passes, public curl fails | Cloudflare cache stale | Purge Cloudflare cache for domain |
| Public curl passes, browser looks old | Browser cache | Incognito or Empty Cache and Hard Reload |
| CSS colour check fails | Asset build or serving stale | `bench build --app nssf_smart_savers`, clear cache, restart |
| Smoke test fails, curl proofs pass | Test checking outdated copy | Fix the smoke test assertion, not the UI |
| Git says dubious ownership | Git ran as root | `sudo -u frappe -H bash -lc 'cd /home/frappe/frappe-bench/apps/nssf_smart_savers && git --no-pager status'` |

---

## Final acceptance criteria

Deployment is complete only when all 10 are true:

1. `phase-1-smartlife-onboarding` includes the latest Claude DOB/NSSF brand commits
2. `bench migrate` passes
3. `bench build --app nssf_smart_savers` passes
4. Origin rendered HTML contains `Date of birth`, `smartlife.css`, `smartlife.js`, and `sl-choice-card`
5. Public rendered HTML contains the same
6. Live CSS contains `#002060`, `#0F2C59`, `#00AEEF`, `#00A3E0`, `#00A859`, and `#107C41`
7. Smoke test passes or leaves only a documented non-blocking warning
8. Browser shows the styled NSSF interface
9. DOB replaces Age and calculates age preview
10. PII is stored server-side only and is not sent to analytics, URLs or console logs
