#!/usr/bin/env bash
# SmartLife Flexi — Smoke Test
# v nssf-brand-shell-20260622
#
# Checks:
#   1. Route HTTP 200s
#   2. Asset HTTP 200s
#   3. CSS/JS in rendered HTML (robust — tolerates query strings and attribute order)
#   4. Design system class presence
#   5. Brand shell presence (sl-brand-shell, sl-brand-bar, sl-demo-route)
#   6. Required content strings (DOB, saver types, staff-assist, projection)
#   7. Analytics / GTM (warn-only)
#   8. Source-level markers (NSSF colours, brand shell, DOB, no manual age)
#   9. API and DocType integrity
#
# Run from: /home/frappe/frappe-bench/apps/nssf_smart_savers

set -euo pipefail

BASE="${SMARTLIFE_BASE_URL:-https://nssf-smartlifeflexi.nile-gov-demo.com}"
PASS=0
FAIL=0
WARN=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[PASS]${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}[FAIL]${NC} $1"; FAIL=$((FAIL+1)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; WARN=$((WARN+1)); }

echo "================================================================"
echo "SmartLife Flexi Smoke Test — $(date)"
echo "Base URL: $BASE"
echo "================================================================"

# ── Fetch helper ─────────────────────────────────────────────────
# -L follows redirects. Cache-bust prevents stale hits on repeated runs.
_fetch() {
  curl -sSL --max-time 25 \
    --header "Cache-Control: no-cache, no-store" \
    --header "Pragma: no-cache" \
    "$BASE$1?v=smoketest-$(date +%s)" 2>/dev/null || echo ""
}

# ── 1. Route HTTP 200 checks ─────────────────────────────────────
echo ""
echo "--- Route availability ---"
ROUTES=(
  "/smartlife-flexi-demo"
  "/smartlife-self-serve"
  "/smartlife-staff-assist"
  "/smartlife-projection-demo"
  "/smartlife-checkout-demo"
  "/smartlife-thank-you"
  "/smartlife-support-demo"
)
for ROUTE in "${ROUTES[@]}"; do
  STATUS=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 15 "$BASE$ROUTE" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "HTTP 200: $ROUTE"
  else
    fail "HTTP $STATUS: $ROUTE (expected 200)"
  fi
done

# ── 2. Asset availability ─────────────────────────────────────────
echo ""
echo "--- Asset availability ---"
_asset_check() {
  local APATH="$1" LABEL="$2"
  local STATUS
  STATUS=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$APATH" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "Asset 200: $LABEL"
  else
    fail "Asset $STATUS: $LABEL — run: bench build --app nssf_smart_savers"
  fi
}
_asset_check "/assets/nssf_smart_savers/css/smartlife.css" "smartlife.css"
_asset_check "/assets/nssf_smart_savers/js/smartlife.js"   "smartlife.js"
_asset_check "/assets/nssf_smart_savers/js/analytics_helper.js" "analytics_helper.js"

# ── 3. CSS/JS in rendered HTML ────────────────────────────────────
# grep -qi so query-string versions and attribute order do not matter.
echo ""
echo "--- CSS/JS in rendered HTML ---"
_check_asset_in_page() {
  local ROUTE="$1" NEEDLE="$2" LABEL="$3"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -qi "$NEEDLE"; then
    ok "$LABEL: found in $ROUTE"
  else
    fail "$LABEL: NOT found in $ROUTE"
    echo "       Diagnostic (first asset-related lines):"
    echo "$HTML" | grep -i 'stylesheet\|script\|\.css\|\.js' | head -5 || echo "       (none)"
  fi
}
_check_asset_in_page "/smartlife-self-serve"      "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-staff-assist"    "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-projection-demo" "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-checkout-demo"   "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-thank-you"       "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-flexi-demo"      "smartlife\.css"        "smartlife.css"
_check_asset_in_page "/smartlife-self-serve"      "smartlife\.js"         "smartlife.js"
_check_asset_in_page "/smartlife-staff-assist"    "analytics_helper\.js"  "analytics_helper.js"

# ── 4. Design system classes ──────────────────────────────────────
echo ""
echo "--- Design system class presence ---"
_check_class() {
  local ROUTE="$1" CLASS="$2"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -q "$CLASS"; then
    ok "$CLASS: found in $ROUTE"
  else
    fail "$CLASS: NOT found in $ROUTE"
  fi
}
_check_class "/smartlife-self-serve"      "sl-choice-card"
_check_class "/smartlife-self-serve"      "sl-stepper"
_check_class "/smartlife-self-serve"      "sl-step-actions"
_check_class "/smartlife-self-serve"      "sl-form"
_check_class "/smartlife-staff-assist"    "sl-form"
_check_class "/smartlife-staff-assist"    "sl-select"
_check_class "/smartlife-projection-demo" "sl-result-card"
_check_class "/smartlife-checkout-demo"   "sl-summary"

# ── 5. Brand shell presence ───────────────────────────────────────
echo ""
echo "--- Brand shell and navbar suppression ---"
for ROUTE in "/smartlife-self-serve" "/smartlife-staff-assist" "/smartlife-projection-demo" \
             "/smartlife-checkout-demo" "/smartlife-thank-you" "/smartlife-flexi-demo"; do
  HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -q "sl-brand-shell\|sl-brand-bar"; then
    ok "Brand shell: $ROUTE"
  else
    fail "Brand shell: NOT found in $ROUTE"
  fi
  if echo "$HTML" | grep -q "sl-demo-route"; then
    ok "sl-demo-route: $ROUTE"
  else
    warn "sl-demo-route: NOT found in $ROUTE (navbar may not be suppressed)"
  fi
done

# ── 6. Required content strings ───────────────────────────────────
echo ""
echo "--- Required content strings ---"
_check_content() {
  local ROUTE="$1" STRING="$2"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -qi "$STRING"; then
    ok "\"$STRING\": found in $ROUTE"
  else
    fail "\"$STRING\": NOT found in $ROUTE"
  fi
}

# Saver types
_check_content "/smartlife-self-serve" "Existing NSSF Member"
_check_content "/smartlife-self-serve" "New Saver"
_check_content "/smartlife-self-serve" "Diaspora Saver"
_check_content "/smartlife-self-serve" "Informal Sector"
_check_content "/smartlife-self-serve" "Staff-Assisted"
_check_content "/smartlife-self-serve" "Who are you saving as"

# Step 2 — DOB
_check_content "/smartlife-self-serve" "Your Personal Details"
_check_content "/smartlife-self-serve" "Date of birth"
_check_content "/smartlife-self-serve" "date_of_birth"
_check_content "/smartlife-self-serve" "phone"
_check_content "/smartlife-self-serve" "consent"
_check_content "/smartlife-self-serve" "stored securely"

# Staff-assist
_check_content "/smartlife-staff-assist" "Staff-Guided Session"
_check_content "/smartlife-staff-assist" "Prospect Segment"
_check_content "/smartlife-staff-assist" "Savings Goal"

# Projection
_check_content "/smartlife-projection-demo" "Savings Projection Calculator"
_check_content "/smartlife-projection-demo" "Projection is indicative"
_check_content "/smartlife-projection-demo" "Semi-Annually"

# Prototype notices
_check_content "/smartlife-self-serve"      "Prototype environment"
_check_content "/smartlife-staff-assist"    "Prototype environment"
_check_content "/smartlife-projection-demo" "Prototype environment"
_check_content "/smartlife-checkout-demo"   "Prototype environment"

# Checkout / thank-you
_check_content "/smartlife-checkout-demo" "SmartLife Flexi"
_check_content "/smartlife-thank-you"     "SmartLife\|Thank\|on your way"

# ── 7. Analytics / GTM (warn only) ───────────────────────────────
echo ""
echo "--- Analytics / GTM (warnings only) ---"
GTM_HTML=$(_fetch "/smartlife-flexi-demo")
if echo "$GTM_HTML" | grep -q "GTM-PZRV3MQL\|analytics_helper"; then
  ok "GTM or analytics_helper found in landing page"
else
  warn "GTM-PZRV3MQL not found in smartlife-flexi-demo — check hooks.py"
fi
if echo "$GTM_HTML" | grep -qi "uvlttflnbt\|clarity"; then
  ok "Microsoft Clarity ID found in landing page"
else
  warn "Clarity ID not detected — check GTM configuration"
fi

# ── 8. Source-level checks ────────────────────────────────────────
echo ""
echo "--- Source-level checks ---"

CSS_FILE="nssf_smart_savers/public/css/smartlife.css"
if [ -f "$CSS_FILE" ]; then
  for CLASS in ".sl-page" ".sl-container" ".sl-card" ".sl-choice-card" ".sl-goal-card" \
               ".sl-stepper" ".sl-step" ".sl-btn-primary" ".sl-btn-secondary" \
               ".sl-form" ".sl-input" ".sl-select" ".sl-result-card" \
               ".sl-table" ".sl-summary" ".sl-alert" ".sl-disclaimer" \
               ".sl-brand-shell" ".sl-brand-bar" ".sl-brand-lockup"; do
    grep -q "$CLASS" "$CSS_FILE" \
      && ok "CSS: $CLASS defined" \
      || fail "CSS: $CLASS MISSING"
  done
  for COLOUR in "#002060" "#0F2C59" "#00AEEF" "#00A3E0" "#00A859" "#107C41"; do
    grep -qi "$COLOUR" "$CSS_FILE" \
      && ok "CSS: NSSF colour $COLOUR present" \
      || fail "CSS: NSSF colour $COLOUR MISSING"
  done
else
  fail "CSS file not found: $CSS_FILE"
fi

AH_FILE="nssf_smart_savers/public/js/analytics_helper.js"
if [ -f "$AH_FILE" ]; then
  for BLOCKED_KEY in "first_name" "last_name" "phone" "email" "nin" "date_of_birth" "age_years"; do
    grep -q "$BLOCKED_KEY" "$AH_FILE" \
      && ok "Analytics: '$BLOCKED_KEY' in PII block-list" \
      || fail "Analytics: '$BLOCKED_KEY' NOT in analytics_helper.js PII block-list"
  done
  grep -q "PII_KEYS\|isPiiKey\|sanitise" "$AH_FILE" \
    && ok "Analytics: PII guard present" \
    || fail "Analytics: PII guard MISSING"
else
  fail "analytics_helper.js not found"
fi

SS_FILE="nssf_smart_savers/www/smartlife-self-serve.html"
if [ -f "$SS_FILE" ]; then
  grep -q "smartlife\.css" "$SS_FILE"     && ok "Source: smartlife.css in self-serve.html"        || fail "Source: smartlife.css MISSING"
  grep -q "sl-choice-card" "$SS_FILE"     && ok "Source: sl-choice-card in self-serve.html"       || fail "Source: sl-choice-card MISSING"
  grep -q "Existing NSSF Member" "$SS_FILE" && ok "Source: 'Existing NSSF Member' in self-serve.html" || fail "Source: 'Existing NSSF Member' NOT found"
  grep -q "date_of_birth" "$SS_FILE"      && ok "Source: date_of_birth in self-serve.html"        || fail "Source: date_of_birth MISSING"
  grep -qi "Date of birth" "$SS_FILE"     && ok "Source: 'Date of birth' label in self-serve.html" || fail "Source: 'Date of birth' label MISSING"
  grep -q "sl-brand-shell\|sl-brand-bar" "$SS_FILE" && ok "Source: brand shell in self-serve.html" || fail "Source: brand shell MISSING"
  if grep -q 'id="sl-age"' "$SS_FILE"; then
    fail "Source: manual age input (id=sl-age) still present — replace with DOB"
  else
    ok "Source: manual age input correctly absent"
  fi
fi

SA_FILE="nssf_smart_savers/www/smartlife-staff-assist.html"
if [ -f "$SA_FILE" ]; then
  grep -q "sl-form"   "$SA_FILE" && ok "Source: sl-form in staff-assist.html"   || fail "Source: sl-form MISSING"
  grep -q "sl-select" "$SA_FILE" && ok "Source: sl-select in staff-assist.html" || fail "Source: sl-select MISSING"
  grep -q "sl-brand-shell\|sl-brand-bar" "$SA_FILE" && ok "Source: brand shell in staff-assist.html" || fail "Source: brand shell MISSING"
fi

PROJ_FILE="nssf_smart_savers/www/smartlife-projection-demo.html"
if [ -f "$PROJ_FILE" ]; then
  grep -q "sl-result-card" "$PROJ_FILE" && ok "Source: sl-result-card in projection-demo.html" || fail "Source: sl-result-card MISSING"
  grep -qi "semi-annually"  "$PROJ_FILE" && ok "Source: semi-annually in projection-demo.html"  || fail "Source: semi-annually MISSING"
fi

API_FILE="nssf_smart_savers/api.py"
if [ -f "$API_FILE" ]; then
  grep -q "date_of_birth"  "$API_FILE" && ok "API: date_of_birth accepted"  || fail "API: date_of_birth NOT found"
  grep -q "birthday_month" "$API_FILE" && ok "API: birthday_month computed" || fail "API: birthday_month NOT found"
  grep -q "birthday_day"   "$API_FILE" && ok "API: birthday_day computed"   || fail "API: birthday_day NOT found"
  grep -q "age_band"       "$API_FILE" && ok "API: age_band computed"       || fail "API: age_band NOT found"
else
  fail "api.py not found"
fi

DT_FILE="nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json"
if [ -f "$DT_FILE" ]; then
  for DT_FIELD in "date_of_birth" "birthday_month" "birthday_day" "age_years" "age_band" \
                  "primary_phone" "gender" "consent_to_contact"; do
    grep -q "\"$DT_FIELD\"" "$DT_FILE" \
      && ok "DocType: $DT_FIELD present" \
      || fail "DocType: $DT_FIELD MISSING"
  done
else
  fail "DocType JSON not found: $DT_FILE"
fi

for f in nssf_smart_savers/www/smartlife-*.html; do
  if grep -qiE "CM[0-9]{7}[A-Z]{2}|\+2567[0-9]{8}|@gmail\.com|@yahoo\.com" "$f" 2>/dev/null; then
    fail "Source: PII test value in $(basename "$f")"
  else
    ok "Source: no PII test values in $(basename "$f")"
  fi
done

for f in nssf_smart_savers/www/smartlife-*.html; do
  grep -q "Cache-Control" "$f" \
    && ok "Source: no-cache header in $(basename "$f")" \
    || warn "Source: no-cache header MISSING from $(basename "$f")"
done

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "================================================================"
echo -e "Results: ${GREEN}$PASS passed${NC} | ${RED}$FAIL failed${NC} | ${YELLOW}$WARN warnings${NC}"
echo "================================================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo -e "${RED}SMOKE TEST FAILED${NC} — $FAIL check(s) did not pass."
  echo ""
  echo "Common causes:"
  echo "  1. bench build --app nssf_smart_savers"
  echo "  2. bench --site \$SITE clear-cache && bench --site \$SITE clear-website-cache"
  echo "  3. Verify <link> and <script> tags exist in every template"
  echo "  4. If origin passes but public fails: purge Cloudflare cache"
  echo "  5. If brand shell checks fail: confirm sl-brand-shell wrapper in templates"
  exit 1
else
  echo -e "${GREEN}ALL CHECKS PASSED${NC}"
  exit 0
fi
