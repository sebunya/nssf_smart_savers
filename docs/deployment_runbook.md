# Deployment Runbook — SmartLife Flexi Phase 1

## Prerequisites
- Frappe bench installed at /home/frappe/frappe-bench
- Site: nssf-smartlifeflexi.nile-gov-demo.com
- App installed: bench get-app nssf_smart_savers (from GitHub)
- Branch: phase-1-smartlife-onboarding

## Deploy Steps

### 1. Pull Latest Code
```bash
cd /home/frappe/frappe-bench/apps/nssf_smart_savers
git fetch origin
git checkout phase-1-smartlife-onboarding
git pull --ff-only origin phase-1-smartlife-onboarding
```

### 2. Run Migrations
```bash
cd /home/frappe/frappe-bench
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
```

### 3. Build Assets
```bash
bench build --app nssf_smart_savers
```

### 4. Clear Caches
```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
```

### 5. Restart Services
```bash
sudo supervisorctl restart frappe-bench-web:
sudo supervisorctl restart frappe-bench-workers:
sudo service nginx reload
```

### 6. Run Smoke Tests
```bash
./scripts/smoke_test.sh
```

## Rollback
```bash
git checkout <previous-commit>
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate
bench build --app nssf_smart_savers
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
```

## What Must NOT Be Deployed to Production Without Approval
- Real Pesapal credentials
- Real SMS gateway credentials
- Real member data collection features
- Live payment processing

## Post-Deploy Verification
- All routes return 200
- Demo notice banner visible
- Projection calculator returns values
- Staff assist form submits successfully
- No PII accepted in any form
