# NSSF SmartLife Flexi — Admin User Guide

This guide is for system administrators configuring and managing the SmartLife Flexi prototype.

---

## 1. Accessing Frappe Desk
Administrators manage system configurations and schema records using the standard Frappe Desk dashboard:
- **URL**: `{your_domain}/desk` (e.g. `nssf-smartlifeflexi.nile-gov-demo.com/desk`)
- Log in using your Frappe Administrator credentials.

---

## 2. Managing SmartLife Leads
- Search for the **SmartLife Demo Lead** DocType using the search bar in Desk.
- Here you can audit submitted lead data, verify consent checks, track lead temperatures, next best actions, and follow-up logs.

---

## 3. Deployment & Cache Operations
After copying updates to the server, run:
```bash
cd /home/frappe/frappe-bench

# Database migration
bench --site nssf-smartlifeflexi.nile-gov-demo.com migrate

# Rebuild assets
bench build --app nssf_smart_savers

# Clear caching
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-cache
bench --site nssf-smartlifeflexi.nile-gov-demo.com clear-website-cache
```

---

## 4. Role Creation and Assignment
To configure the Personalisation Team role:
1. Go to **Role List** -> **Add Role**.
2. Name the role exactly `SmartLife Personalisation Team`.
3. Go to **User List** and assign this role to support agents.
4. Assign permissions on the custom DocTypes (`SmartLife Demo Lead`, `SmartLife Contribution Intent`, `SmartLife Communication Log`, `SmartLife Support Request`) as specified in the release checklist.

---

## 5. Configuration Settings
All credentials for external gateways must be registered in the site config file at `/home/frappe/frappe-bench/sites/nssf-smartlifeflexi.nile-gov-demo.com/site_config.json`:
- `pesapal_consumer_key` & `pesapal_consumer_secret`
- `smartlife_zeptomail_token`
- `smartlife_phahapa_sms_password` & `smartlife_phahapa_sms_api_key`
*Ensure no credentials keys are hardcoded in source files.*
