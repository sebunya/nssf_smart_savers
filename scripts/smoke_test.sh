#!/usr/bin/env bash
set -euo pipefail

SITE_NAME="${SITE_NAME:-nssf-smartlifeflexi.nile-gov-demo.com}"
BENCH_PATH="${BENCH_PATH:-/home/frappe/frappe-bench}"
APP_NAME="${APP_NAME:-nssf_smart_savers}"
BASE_URL="https://${SITE_NAME}"
PASS=0; FAIL=0

ok() { echo "✓ $1"; PASS=$((PASS+1)); }
fail() { echo "✗ $1"; FAIL=$((FAIL+1)); }
warn() { echo "⚠ $1"; }

echo "=== SmartLife Flexi Smoke Tests ==="
echo "Site: $BASE_URL"
echo ""

# 1. App installed
cd "$BENCH_PATH"
bench --site "$SITE_NAME" list-apps 2>/dev/null | grep -q "$APP_NAME" && ok "App $APP_NAME installed" || fail "App $APP_NAME NOT installed"

# Route checks
check_route() {
  local path="$1"; local label="$2"
  local code=$(curl -o /dev/null -s -w "%{http_code}" "$BASE_URL$path")
  [ "$code" = "200" ] && ok "GET $path -> 200" || fail "GET $path -> $code (expected 200)"
}

check_route "/smartlife-flexi-demo" "Landing"
check_route "/smartlife-self-serve" "Self-serve"
check_route "/smartlife-staff-assist" "Staff assist"
check_route "/smartlife-projection-demo" "Projection"
check_route "/smartlife-checkout-demo" "Checkout"
check_route "/smartlife-support-demo" "Support"
check_route "/smartlife-thank-you" "Thank you"
check_route "/helpdesk/home" "Helpdesk"

# Content checks
check_content() {
  local path="$1"; local label="$2"; local pattern="$3"
  local body=$(curl -s "$BASE_URL$path")
  echo "$body" | grep -q "$pattern" && ok "$label: '$pattern'" || fail "$label: missing '$pattern'"
}

echo ""
echo "--- Content checks ---"
check_content "/smartlife-flexi-demo" "Landing" "SmartLife Flexi Demo"
check_content "/smartlife-flexi-demo" "Landing" "Prototype environment"
check_content "/smartlife-self-serve" "Self-serve" "Who are you saving as"
check_content "/smartlife-self-serve" "Self-serve" "Existing NSSF Member"
check_content "/smartlife-self-serve" "Self-serve" "New Saver"
check_content "/smartlife-self-serve" "Self-serve" "Diaspora"
check_content "/smartlife-self-serve" "Self-serve" "Informal"
check_content "/smartlife-self-serve" "Self-serve" "semi-annually"
check_content "/smartlife-self-serve" "Self-serve" "Do not enter real"
check_content "/smartlife-staff-assist" "Staff assist" "Staff-Guided Session"
check_content "/smartlife-staff-assist" "Staff assist" "Prospect Segment"
check_content "/smartlife-staff-assist" "Staff assist" "Savings Goal"
check_content "/smartlife-staff-assist" "Staff assist" "Generate"
check_content "/smartlife-projection-demo" "Projection" "Savings Projection Calculator"
check_content "/smartlife-projection-demo" "Projection" "indicative"
check_content "/smartlife-projection-demo" "Projection" "semi-annually"
check_content "/smartlife-checkout-demo" "Checkout" "Prototype environment"
check_content "/smartlife-thank-you" "Thank-you" "Thank"

# GTM check (warn only)
GTM_BODY=$(curl -s "$BASE_URL/smartlife-flexi-demo")
echo "$GTM_BODY" | grep -q "GTM-PZRV3MQL" && ok "GTM-PZRV3MQL present" || warn "GTM-PZRV3MQL not found in landing HTML"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && echo "ALL SMOKE TESTS PASSED" || { echo "SMOKE TESTS FAILED"; exit 1; }
