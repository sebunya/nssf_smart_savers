#!/usr/bin/env bash
# SmartLife Flexi — Comprehensive Smoke Test
# v nssf-brand-dob-ui-20260622
#
# Checks:
#   1. Route HTTP 200s
#   2. Asset HTTP 200s
#   3. CSS/JS injection in rendered HTML
#   4. Design system class presence
#   5. Required content strings (DOB, saver types, staff-assist, projection)
#   6. Analytics / GTM (warn-only)
#   7. Source-level markers (CSS classes, NSSF colours, DOB, no manual age)
#   8. API and DocType integrity
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

# ── 1. Route HTTP 200 checks ────────────────────────────────────
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
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$BASE$ROUTE" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    ok "HTTP 200: $ROUTE"
  else
    fail "HTTP $STATUS: $ROUTE (expected 200)"
  fi
done

# ── 2. Asset availability ────────────────────────────────────────
echo ""
echo "--- Asset availability ---"
CSS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/css/smartlife.css" 2>/dev/null || echo "000")
if [ "$CSS_STATUS" = "200" ]; then
  ok "CSS asset returns 200: /assets/nssf_smart_savers/css/smartlife.css"
else
  fail "CSS asset returned $CSS_STATUS — run: bench build --app nssf_smart_savers"
fi

JS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/js/smartlife.js" 2>/dev/null || echo "000")
if [ "$JS_STATUS" = "200" ]; then
  ok "JS asset returns 200: /assets/nssf_smart_savers/js/smartlife.js"
else
  fail "JS asset returned $JS_STATUS"
fi

AH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE/assets/nssf_smart_savers/js/analytics_helper.js" 2>/dev/null || echo "000")
if [ "$AH_STATUS" = "200" ]; then
  ok "Analytics helper JS returns 200"
else
  fail "Analytics helper JS returned $AH_STATUS"
fi

# ── 3. CSS/JS injection in rendered HTML ────────────────────────
echo ""
echo "--- CSS/JS injection in rendered pages ---"
_fetch() { curl -fsS --max-time 20 --header "Cache-Control: no-cache" "$BASE$1?v=smoketest-$(date +%s)" 2>/dev/null || echo ""; }
check_asset_in_page() {
  local ROUTE="$1" NEEDLE="$2" LABEL="$3"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -q "$NEEDLE"; then
    ok "$LABEL: found in $ROUTE"
  else
    fail "$LABEL: NOT found in $ROUTE — CSS/JS not injected"
  fi
}
check_asset_in_page "/smartlife-self-serve"       "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-staff-assist"     "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-projection-demo"  "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-checkout-demo"    "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-thank-you"        "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-flexi-demo"       "smartlife.css"         "smartlife.css link"
check_asset_in_page "/smartlife-self-serve"       "smartlife.js"          "smartlife.js link"
check_asset_in_page "/smartlife-staff-assist"     "analytics_helper.js"   "analytics_helper.js link"

# ── 4. Design system class presence in rendered HTML ─────────────
echo ""
echo "--- Design system class presence ---"
check_class_in_page() {
  local ROUTE="$1" CLASS="$2"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -q "$CLASS"; then
    ok "$CLASS found in $ROUTE"
  else
    fail "$CLASS NOT found in $ROUTE"
  fi
}
check_class_in_page "/smartlife-self-serve"      "sl-choice-card"
check_class_in_page "/smartlife-self-serve"      "sl-stepper"
check_class_in_page "/smartlife-self-serve"      "sl-step-actions"
check_class_in_page "/smartlife-self-serve"      "sl-details-form"
check_class_in_page "/smartlife-staff-assist"    "sl-form"
check_class_in_page "/smartlife-staff-assist"    "sl-select"
check_class_in_page "/smartlife-projection-demo" "sl-result-card"
check_class_in_page "/smartlife-checkout-demo"   "sl-summary"

# ── 5. Required content strings ──────────────────────────────────
echo ""
echo "--- Required content strings ---"
check_content_in_page() {
  local ROUTE="$1" STRING="$2"
  local HTML; HTML=$(_fetch "$ROUTE")
  if echo "$HTML" | grep -qi "$STRING"; then
    ok "\"$STRING\" found in $ROUTE"
  else
    fail "\"$STRING\" NOT found in $ROUTE"
  fi
}

# Self-serve saver types
check_content_in_page "/smartlife-self-serve" "Existing NSSF Member"
check_content_in_page "/smartlife-self-serve" "New Saver"
check_content_in_page "/smartlife-self-serve" "Diaspora Saver"
check_content_in_page "/smartlife-self-serve" "Informal Sector"
check_content_in_page "/smartlife-self-serve" "Staff-Assisted"
check_content_in_page "/smartlife-self-serve" "Who are you saving as"

# Self-serve Step 2 — Personal Details with DOB
check_content_in_page "/smartlife-self-serve" "Your Personal Details"
check_content_in_page "/smartlife-self-serve" "Date of birth"
check_content_in_page "/smartlife-self-serve" "date_of_birth"
check_content_in_page "/smartlife-self-serve" "Primary phone"
check_content_in_page "/smartlife-self-serve" "consent"
check_content_in_page "/smartlife-self-serve" "Your information is stored securely"

# Staff-assist
check_content_in_page "/smartlife-staff-assist" "Staff-Guided Session"
check_content_in_page "/smartlife-staff-assist" "Prospect Segment"
check_content_in_page "/smartlife-staff-assist" "Savings Goal"

# Projection
check_content_in_page "/smartlife-projection-demo" "Savings Projection Calculator"
check_content_in_page "/smartlife-projection-demo" "Projection is indicative"
check_content_in_page "/smartlife-projection-demo" "Semi-Annually"

# Demo safety notices
check_content_in_page "/smartlife-self-serve"      "Prototype environment"
check_content_in_page "/smartlife-staff-assist"    "Prototype environment"
check_content_in_page "/smartlife-projection-demo" "Prototype environment"
check_content_in_page "/smartlife-checkout-demo"   "Prototype environment"

# Checkout / thank-you
check_content_in_page "/smartlife-checkout-demo" "SmartLife Flexi"
check_content_in_page "/smartlife-thank-you"     "Thank"

# ── 6. Analytics / GTM (warn only) ──────────────────────────────
echo ""
echo "--- Analytics / GTM (warnings only) ---"
GTM_HTML=$(_fetch "/smartlife-flexi-demo")
if echo "$GTM_HTML" | grep -q "GTM-PZRV3MQL\|analytics_helper"; then
  ok "GTM or analytics_helper found in landing page"
else
  warn "GTM-PZRV3MQL not found in smartlife-flexi-demo — check hooks.py or template includes"
fi
if echo "$GTM_HTML" | grep -qi "uvlttflnbt\|clarity"; then
  ok "Microsoft Clarity ID found in landing page"
else
  warn "Clarity ID not detected — check GTM configuration"
fi

# ── 7. Source-level checks ───────────────────────────────────────
echo ""
echo "--- Source-level checks ---"

# CSS required classes
CSS_FILE="nssf_smart_savers/public/css/smartlife.css"
if [ -f "$CSS_FILE" ]; then
  for CLASS in ".sl-page" ".sl-container" ".sl-card" ".sl-choice-card" ".sl-goal-card" \
               ".sl-stepper" ".sl-step" ".sl-btn-primary" ".sl-btn-secondary" \
               ".sl-form" ".sl-input" ".sl-select" ".sl-result-card" \
               ".sl-table" ".sl-summary" ".sl-alert" ".sl-disclaimer"; do
    grep -q "$CLASS" "$CSS_FILE" \
      && ok "CSS: $CLASS defined" \
      || fail "CSS: $CLASS MISSING"
  done

  # NSSF brand colours must be present
  for COLOUR in "#002060" "#0F2C59" "#00AEEF" "#00A3E0" "#00A859" "#107C41"; do
    grep -qi "$COLOUR" "$CSS_FILE" \
      && ok "CSS: NSSF colour $COLOUR present" \
      || fail "CSS: NSSF colour $COLOUR MISSING from smartlife.css"
  done
else
  fail "CSS file not found: $CSS_FILE"
fi

# analytics_helper.js PII block-list
AH_FILE="nssf_smart_savers/public/js/analytics_helper.js"
if [ -f "$AH_FILE" ]; then
  for BLOCKED_KEY in "first_name" "last_name" "phone" "email" "nin" "date_of_birth" "age_years"; do
    grep -q "$BLOCKED_KEY" "$AH_FILE" \
      && ok "Analytics: '$BLOCKED_KEY' referenced in PII block-list" \
      || fail "Analytics: '$BLOCKED_KEY' NOT found in analytics_helper.js PII block-list"
  done
  grep -q "PII_KEYS\|isPiiKey\|sanitise" "$AH_FILE" \
    && ok "Analytics: PII guard function present" \
    || fail "Analytics: PII guard MISSING from analytics_helper.js"
else
  fail "analytics_helper.js not found"
fi

# Self-serve template checks
SS_FILE="nssf_smart_savers/www/smartlife-self-serve.html"
if [ -f "$SS_FILE" ]; then
  grep -q "smartlife.css" "$SS_FILE" \
    && ok "Source: smartlife.css link in self-serve.html" \
    || fail "Source: smartlife.css link MISSING from self-serve.html"
  grep -q "sl-choice-card" "$SS_FILE" \
    && ok "Source: sl-choice-card in self-serve.html" \
    || fail "Source: sl-choice-card MISSING"
  grep -q "Existing NSSF Member" "$SS_FILE" \
    && ok "Source: 'Existing NSSF Member' in self-serve.html" \
    || fail "Source: 'Existing NSSF Member' NOT found"
  grep -q "date_of_birth" "$SS_FILE" \
    && ok "Source: date_of_birth field in self-serve.html" \
    || fail "Source: date_of_birth MISSING from self-serve.html"
  grep -qi "Date of birth" "$SS_FILE" \
    && ok "Source: 'Date of birth' label in self-serve.html" \
    || fail "Source: 'Date of birth' label MISSING"
  if grep -q 'id="sl-age"' "$SS_FILE"; then
    fail "Source: manual age input (id=sl-age) still present — must be replaced by DOB"
  else
    ok "Source: manual age input correctly removed"
  fi
fi

# Staff-assist template
SA_FILE="nssf_smart_savers/www/smartlife-staff-assist.html"
if [ -f "$SA_FILE" ]; then
  grep -q "sl-form"   "$SA_FILE" && ok "Source: sl-form in staff-assist.html"   || fail "Source: sl-form MISSING"
  grep -q "sl-select" "$SA_FILE" && ok "Source: sl-select in staff-assist.html" || fail "Source: sl-select MISSING"
fi

# Projection template
PROJ_FILE="nssf_smart_savers/www/smartlife-projection-demo.html"
if [ -f "$PROJ_FILE" ]; then
  grep -q "sl-result-card" "$PROJ_FILE" && ok "Source: sl-result-card in projection-demo.html" || fail "Source: sl-result-card MISSING"
  grep -qi "semi-annually"  "$PROJ_FILE" && ok "Source: semi-annually in projection-demo.html"  || fail "Source: semi-annually MISSING"
fi

# API source checks
API_FILE="nssf_smart_savers/api.py"
if [ -f "$API_FILE" ]; then
  grep -q "date_of_birth"  "$API_FILE" && ok "API: date_of_birth accepted"     || fail "API: date_of_birth NOT found"
  grep -q "birthday_month" "$API_FILE" && ok "API: birthday_month computed"    || fail "API: birthday_month NOT found"
  grep -q "birthday_day"   "$API_FILE" && ok "API: birthday_day computed"      || fail "API: birthday_day NOT found"
  grep -q "age_band"       "$API_FILE" && ok "API: age_band computed"          || fail "API: age_band NOT found"
else
  fail "api.py not found"
fi

# DocType JSON checks
DT_FILE="nssf_smart_savers/nssf_smart_savers/doctype/smartlife_demo_lead/smartlife_demo_lead.json"
if [ -f "$DT_FILE" ]; then
  for DT_FIELD in "date_of_birth" "birthday_month" "birthday_day" "age_years" "age_band" \
                  "primary_phone" "gender" "consent_to_contact"; do
    grep -q "\"$DT_FIELD\"" "$DT_FILE" \
      && ok "DocType: $DT_FIELD field present" \
      || fail "DocType: $DT_FIELD MISSING"
  done
else
  fail "DocType JSON not found: $DT_FILE"
fi

# No PII test values in source
for f in nssf_smart_savers/www/smartlife-*.html; do
  if grep -qiE "CM[0-9]{7}[A-Z]{2}|\+2567[0-9]{8}|@gmail\.com|@yahoo\.com" "$f" 2>/dev/null; then
    fail "Source: PII test value detected in $(basename "$f")"
  else
    ok "Source: No PII test values in $(basename "$f")"
  fi
done

# Cache-Control headers in all templates
for f in nssf_smart_savers/www/smartlife-*.html; do
  grep -q "Cache-Control" "$f" \
    && ok "Source: no-cache header in $(basename "$f")" \
    || warn "Source: no-cache header MISSING from $(basename "$f")"
done

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "================================================================"
echo -e "Results: ${GREEN}$PASS passed${NC} | ${RED}$FAIL failed${NC} | ${YELLOW}$WARN warnings${NC}"
echo "================================================================"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo -e "${RED}SMOKE TEST FAILED${NC} — $FAIL check(s) did not pass."
  echo ""
  echo "Common causes:"
  echo "  1. Run: bench build --app nssf_smart_savers"
  echo "  2. Run: bench --site \$SITE clear-cache && bench --site \$SITE clear-website-cache"
  echo "  3. Check explicit <link> tags exist in every template"
  echo "  4. If origin passes but public fails: purge Cloudflare cache for the domain"
  echo "  5. Check Frappe hooks.py web_include_css/js lists are correct"
  exit 1
else
  echo -e "${GREEN}ALL CHECKS PASSED${NC}"
  exit 0
fi
