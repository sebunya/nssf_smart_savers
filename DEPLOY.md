# NSSF SmartLife Flexi — Deployment and Verification Runbook

**Branch:** `claude/cool-bell-t7n0hs` → `phase-1-smartlife-onboarding`
**Version tag:** `nssf-brand-dob-ui-20260622`

The deployment is complete **only** when all ten acceptance criteria at the end of this document are confirmed true. Route HTTP 200 alone is not proof. Work through every step in order.

---

## STEP 1 — Merge into production branch

Run as root on the server. The script drops to `frappe` user inside.

```bash
sudo -u frappe -H bash -lc '
set -euo pipefail

APP="/home/frappe/frappe-bench/apps/nssf_smart_savers"
cd "$APP"

export GIT_PAGER=cat
export PAGER=cat

echo "USER=$(whoami)"
echo "PWD=$(pwd)"
echo "CURRENT BRANCH=$(git branch --show-current)"

git --no-pager status
git --no-pager log --oneline --decorate -8

git fetch origin

git checkout phase-1-smartlife-onboarding
git pull origin phase-1-smartlife-onboarding

git merge --no-ff origin/claude/cool-bell-t7n0hs \
  -m "Merge final NSSF brand DOB onboarding and smoke-test fixes" || {
  echo "MERGE FAILED. Resolve conflicts before continuing."
  git status
  exit 1
}

git --no-pager status
git --no-pager log --oneline --decorate -12

git push origin phase-1-smartlife-onboarding
'
```

**Expected:**
- Branch is `phase-1-smartlife-onboarding`
- Working tree is clean after merge
- Log includes the DOB/NSSF brand/smoke-test commit or a merge commit containing it
- Push succeeds

**Do not continue if merge fails.**

---

## STEP 2 — Deploy

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

sudo supervisorctl status | grep -E "frappe-bench-web|frappe-bench-workers"
```

**Expected:**
- Backup completes without error
- `migrate` upgrades `nssf_smart_savers` without error
- `bench build` exits 0
- Web and workers show `RUNNING`

---

## STEP 3 — Prove source state on disk

```bash
sudo -u frappe -H bash -lc '
cd /home/frappe/frappe-bench/apps/nssf_smart_savers

echo "=== SOURCE COMMIT ==="
git --no-pager log --oneline --decorate -5

echo ""
echo "=== DOB SOURCE CHECK ==="
grep -Rn "date_of_birth\|Date of birth\|birthday_month\|birthday_day" \
  nssf_smart_savers/www nssf_smart_savers/api.py | head -50

echo ""
echo "=== NSSF COLOUR SOURCE CHECK ==="
grep -E "#002060|#0F2C59|#00AEEF|#00A3E0|#00A859|#107C41" \
  nssf_smart_savers/public/css/smartlife.css

echo ""
echo "=== ASSET VERSION STRING CHECK ==="
grep -Rn "nssf-brand-dob-ui-20260622" \
  nssf_smart_savers/www nssf_smart_savers/templates | head -50
'
```

**Expected:**
- `date_of_birth`, `birthday_month`, `birthday_day` all found
- All six NSSF hex colour values found in `smartlife.css`
- Version string `nssf-brand-dob-ui-20260622` found in templates

---

## STEP 4 — Prove origin rendered HTML (bypasses Cloudflare)

```bash
curl -fsSL \
  -H "Host: nssf-smartlifeflexi.nile-gov-demo.com" \
  "http://127.0.0.1/smartlife-self-serve?origin-test=$(date +%s)" \
| grep -E "smartlife\.css|smartlife\.js|sl-choice-card|sl-stepper|\
Your Personal Details|Date of birth|Existing NSSF Member|\
New Saver|Diaspora Saver|Informal Sector|Staff-Assisted"
```

**Expected:** Matching HTML lines printed for each pattern.

**If this fails** — Frappe is serving old HTML. Re-run clear-cache, clear-website-cache, migrate, build, restart. Do not blame Cloudflare until origin passes.

---

## STEP 5 — Prove public rendered HTML (through Cloudflare)

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

curl -fsSL "$BASE/smartlife-self-serve?v=nssf-brand-dob-ui-$(date +%s)" \
| grep -E "smartlife\.css|smartlife\.js|sl-choice-card|sl-stepper|\
Your Personal Details|Date of birth|Existing NSSF Member|\
New Saver|Diaspora Saver|Informal Sector|Staff-Assisted"
```

**Expected:** Same matching lines as Step 4.

**If origin passes but public fails** — Cloudflare is serving stale HTML. Purge the Cloudflare cache for `nssf-smartlifeflexi.nile-gov-demo.com`, then re-run with a fresh `?v=` value.

---

## STEP 6 — Prove live CSS contains NSSF colours

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

curl -fsSL \
  "$BASE/assets/nssf_smart_savers/css/smartlife.css?v=nssf-colour-check-$(date +%s)" \
| grep -E "#002060|#0F2C59|#00AEEF|#00A3E0|#00A859|#107C41"
```

**Expected:** All six colour values returned.

**If this fails** — Asset build is stale or wrong file served. Re-run `bench build --app nssf_smart_savers`, clear caches, restart, retest.

---

## STEP 7 — Run smoke test

```bash
sudo -u frappe -H bash -lc '
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
export GIT_PAGER=cat PAGER=cat
./scripts/smoke_test.sh
'
```

**Expected:**
- All route checks pass
- Asset availability checks pass
- Rendered HTML class and content checks pass
- DOB source checks pass (date_of_birth present, sl-age absent)
- NSSF colour checks pass
- Analytics PII block-list checks pass

**If smoke test fails but curl checks pass** — A specific content string in the test may not match the current page wording. Fix the smoke test assertion, not the product UI, unless the product genuinely changed.

---

## STEP 8 — Test DOB API with dummy data

```bash
BASE="https://nssf-smartlifeflexi.nile-gov-demo.com"

curl -sS -X POST \
  "$BASE/api/method/nssf_smart_savers.api.submit_personal_details" \
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

**Expected response fields:**
- `success: true`
- `session_id` or anonymous reference
- `age_band` (e.g. `"25-34"`)

**Must NOT appear in response:**
- `first_name`, `last_name`, `phone`, `email`
- `date_of_birth`, `birthday_month`, `birthday_day`
- Exact `age_years`

**If API fails** — Check DocType fields exist after migration, check `api.py` field names, check Frappe error logs (`bench --site ... error-log`).

---

## STEP 9 — Verify DocType fields in console

```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com console
```

Inside console:

```python
import frappe
fields = [f.fieldname for f in frappe.get_meta("SmartLife Demo Lead").fields]
missing = [x for x in [
    "date_of_birth", "age_years", "age_band", "birthday_month", "birthday_day",
    "gender", "primary_phone", "alternative_phone", "email",
    "country_of_residence", "preferred_contact_channel", "consent_to_contact"
] if x not in fields]
print("Missing fields:", missing)
exit()
```

**Expected:**

```
Missing fields: []
```

---

## STEP 10 — Browser acceptance test

Open in Incognito (or Empty Cache and Hard Reload in Chrome DevTools):

```
https://nssf-smartlifeflexi.nile-gov-demo.com/smartlife-self-serve?v=nssf-brand-dob-ui-final
```

**Visual checklist:**
- [ ] NSSF navy (`#002060`) dominates headings and structural elements
- [ ] NSSF green (`#00A859`) used for CTA buttons, selected cards, active stepper step
- [ ] Sky blue (`#00AEEF`) appears as focus ring / accent colour
- [ ] Cards are styled — not raw HTML
- [ ] Stepper is styled and labels are visible
- [ ] Step 1 shows five saver type choice cards (Existing NSSF Member, New Saver, Diaspora Saver, Informal Sector, Staff-Assisted)
- [ ] Step 2 header says "Your Personal Details"
- [ ] Step 2 has a "Date of birth" date picker — no manual age number input
- [ ] Selecting a DOB shows a calculated age preview in green
- [ ] Next button advances the stepper
- [ ] No PII appears in the URL at any step
- [ ] Browser console has no fatal JavaScript errors

---

## Troubleshooting decision tree

| Symptom | Cause | Fix |
|---|---|---|
| Origin curl fails | Frappe cache / wrong branch | clear-cache + clear-website-cache + migrate + build + restart |
| Public curl fails, origin passes | Cloudflare cache | Purge Cloudflare cache for domain |
| Browser looks old, both curls pass | Browser cache | Open Incognito / Empty Cache and Hard Reload |
| CSS 404 | Asset not built | `bench build --app nssf_smart_savers` |
| Smoke test content mismatch | Test wording vs template wording | Fix test assertion (not UI) |
| API 500 | Missing DocType field | `bench migrate`, check console step 9 |
| Merge conflict | Diverged branches | Resolve conflict manually, re-commit, push |

---

## Final acceptance criteria

The deployment is complete only when **all ten** are true:

1. `phase-1-smartlife-onboarding` contains the final DOB/NSSF brand commit
2. `bench migrate` completes without error
3. `bench build --app nssf_smart_savers` completes without error
4. Origin rendered HTML contains `Date of birth`, `smartlife.css`, `smartlife.js`, `sl-choice-card`
5. Public rendered HTML contains the same
6. Live CSS contains `#002060`, `#0F2C59`, `#00AEEF`, `#00A3E0`, `#00A859`, `#107C41`
7. Smoke test passes (or any remaining warning is non-blocking and explained)
8. API returns `success: true` with `age_band` and no PII fields in response
9. DocType console check returns empty missing-fields list
10. Browser shows the styled NSSF-coloured interface with DOB picker and no manual age field
