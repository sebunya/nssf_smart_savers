# Phase 1 Preservation Audit — Updated

**Date:** 2026-06-21 (updated)
**Branch:** claude/cool-bell-t7n0hs
**HEAD at audit:** c1c34eb
**Checkpoint branch:** safeguard-before-nssf-ui-pii-pass-20260621

## Routes that must remain live
- /smartlife-flexi-demo
- /smartlife-self-serve (6-step onboarding)
- /smartlife-staff-assist
- /smartlife-projection-demo
- /smartlife-checkout-demo
- /smartlife-thank-you
- /smartlife-support-demo

## Templates being touched in this pass
- nssf_smart_savers/www/smartlife-self-serve.html (DOB + version bump)
- nssf_smart_savers/www/smartlife-flexi-demo.html (version bump + no-cache)
- nssf_smart_savers/www/smartlife-staff-assist.html (version bump + no-cache)
- nssf_smart_savers/www/smartlife-projection-demo.html (version bump + no-cache)
- nssf_smart_savers/www/smartlife-checkout-demo.html (version bump + no-cache)
- nssf_smart_savers/www/smartlife-thank-you.html (version bump + no-cache)
- nssf_smart_savers/www/smartlife-support-demo.html (version bump + no-cache)
- nssf_smart_savers/templates/includes/smartlife_assets.html (version bump)

## CSS/JS files being touched
- nssf_smart_savers/public/css/smartlife.css (brand corrections, .sl-summary alias)
- nssf_smart_savers/public/js/analytics_helper.js (DOB added to PII block-list)

## API files being touched
- nssf_smart_savers/api.py (DOB-based age calculation)

## DocTypes being touched
- SmartLife Demo Lead: add date_of_birth, age_years, age_band, birthday_month, birthday_day fields
  (old fields preserved — never deleted)

## Adapter files being touched
- nssf_smart_savers/integrations/phahapa_sms_adapter.py
- nssf_smart_savers/integrations/zeptomail_adapter.py
- nssf_smart_savers/integrations/crm_adapter.py

## What must NOT regress
- All 7 routes returning HTTP 200
- /assets/nssf_smart_savers/css/smartlife.css returning 200
- /assets/nssf_smart_savers/js/smartlife.js returning 200
- /assets/nssf_smart_savers/js/analytics_helper.js returning 200
- CSS/JS injection in rendered HTML of all pages
- PII never reaching GTM/GA4/Clarity
- All content string smoke test checks
- Integration adapters (pesapal, phahapa, zeptomail, crm, helpdesk)
- DocType naming_series validity

## New version string
?v=nssf-brand-dob-ui-20260622

## Cloud/Cloudflare note
This repository runs in a cloud dev environment. Changes must be committed and
pushed for deployment. If public URL passes but origin fails (or vice versa),
root cause is likely Cloudflare caching stale HTML. Remedy: purge Cloudflare
cache for nssf-smartlifeflexi.nile-gov-demo.com after deploy + bench clear-website-cache.

## Safety invariants (unchanged)
- Every public page shows "Prototype environment" notice
- Projection pages show "Projection is indicative" disclaimer
- PII (DOB, name, phone, email, NIN, exact age) NEVER goes to GTM/GA4/Clarity/URL params
- analytics_helper.js maintains explicit PII + DOB block-list
