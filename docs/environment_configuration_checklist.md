# NSSF SmartLife Flexi — Environment and Configuration Checklist

Use this checklist to verify production environmental configurations.

---

## 1. Domain & Environment Details
- **Site Name**: `nssf-smartlifeflexi.nile-gov-demo.com`
- **Branch**: `phase-1-smartlife-onboarding`
- **Frappe Path**: `/home/frappe/frappe-bench`
- **Application Path**: `/home/frappe/frappe-bench/apps/nssf_smart_savers`

---

## 2. Required Config Keys (`site_config.json`)
The following configuration properties must be registered in the site config. Value placeholders should be updated with official production keys (never hardcoded in source files):

- **Pesapal Configuration Keys**:
  - `pesapal_mode`: Set to `"sandbox"` or `"live"`
  - `pesapal_consumer_key`: API key from Pesapal developer panel
  - `pesapal_consumer_secret`: API secret from Pesapal developer panel
  - `pesapal_callback_url`: e.g. `/api/method/nssf_smart_savers.api.handle_pesapal_callback`
  - `pesapal_ipn_url`: e.g. `/api/method/nssf_smart_savers.api.handle_pesapal_ipn`
  - `pesapal_ipn_id`: Registered IPN Notification ID from Pesapal panel

- **ZeptoMail Configuration Keys**:
  - `smartlife_zeptomail_token`: ZeptoMail API authorization token
  - `smartlife_zeptomail_sender_email`: Registered sender email address

- **Phahapa Configuration Keys**:
  - `smartlife_phahapa_sms_username`: Phahapa SMS account username
  - `smartlife_phahapa_sms_password`: Phahapa SMS account password
  - `smartlife_phahapa_sms_api_key`: Phahapa SMS account API key

---

## 3. Server Configuration & Setup Requirements
- **Nginx configuration**: Configure rate limits (`limit_req_zone`) for whitelisted guest endpoints.
- **Supervisor configs**: Standard supervisord workers mapping for Redis queue tasks.
- **Manual Role Setup**: The `SmartLife Personalisation Team` role must be created manually in Frappe Desk and assigned to authorized personalization staff.
