# SmartLife Flexi — Messaging Setup Guide

**Providers:** ZeptoMail (email) · Phahapa SMS / eGoSMS (SMS)  
**App:** `nssf_smart_savers`  
**Site:** `nssf-smartlifeflexi.nile-gov-demo.com`

---

## Important: Secret-handling rules

- Never commit credentials to source code or git
- Never put credentials in docs, smoke tests, or templates
- Never share credentials in plain text or ticket comments
- Store all credentials using `bench set-config` (encrypted in site config)
- Credentials are accessed in Python via `frappe.conf.get("key_name")`

---

## 1. ZeptoMail Email Setup

ZeptoMail is the transactional email provider.  
Documentation: https://www.zoho.com/zeptomail/help/api/email-sending.html

### 1.1 Required site config keys

```bash
# Set in Frappe site config — NOT in source code
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_api_url "https://api.zeptomail.com/v1.1/email"

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_token "REPLACE_WITH_ZEPTOMAIL_SEND_MAIL_TOKEN"
# Token format: Zoho-enczapikey <your-token-value>

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_from_email "REPLACE_WITH_VERIFIED_SENDER_EMAIL"
# Must be a verified sender address in your ZeptoMail account

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_from_name "NSSF SmartLife Flexi"

# Start in demo mode (safe default — no real emails sent)
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_demo_mode 1
```

### 1.2 How the token is used

The token is placed in the `Authorization` HTTP header:

```
Authorization: Zoho-enczapikey <your-token-value>
```

If the ZeptoMail dashboard shows the full header string starting with `Zoho-enczapikey`, store that entire string as the token value.

### 1.3 Verify ZeptoMail config (without revealing secrets)

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com execute \
  nssf_smart_savers.integrations.zeptomail.get_config_status
# Expected:
# {"configured": true, "api_url": "configured", "token": "configured", ...}
```

Or via the messaging console at `/smartlife-messaging-demo` (approved role required).

### 1.4 Send a controlled test email

Enable live mode for the test only:
```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_demo_mode 0
```

Use the messaging console (`/smartlife-messaging-demo`) with a real lead name.
Or set environment variables and run the live test helper:
```bash
SMARTLIFE_SEND_LIVE_TEST=1 \
SMARTLIFE_TEST_EMAIL=your-test-address@example.com \
  python3 scripts/live_send_test.py
```

Re-enable demo mode after testing:
```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_zeptomail_demo_mode 1
```

### 1.5 ZeptoMail demo mode

When `smartlife_zeptomail_demo_mode = 1`:
- No real email is sent
- Send function returns `{"status": "Demo Mode", "demo_mode": true}`
- Communication log records the send as `Demo Mode`

### 1.6 Rotate or revoke ZeptoMail credentials

To rotate the token:
1. Generate a new Send Mail token in ZeptoMail dashboard
2. `bench --site ... set-config smartlife_zeptomail_token "REPLACE_WITH_NEW_TOKEN"`
3. Revoke the old token in ZeptoMail dashboard

To revoke immediately:
1. Revoke in ZeptoMail dashboard (token is instantly invalid)
2. Update site config with new token

### 1.7 Expected ZeptoMail errors

| Error | Likely cause | Fix |
|---|---|---|
| HTTP 401 | Invalid token or wrong format | Check token starts with `Zoho-enczapikey ` (with space) |
| HTTP 422 | Invalid payload (from/to format) | Check verified sender email is set |
| HTTP 429 | Rate limit exceeded | Add delay between sends |
| Timeout | Network or ZeptoMail unreachable | Retry; check server outbound egress |

---

## 2. Phahapa SMS / eGoSMS Setup

SMS provider: eGoSMS (https://comms.egosms.co)  
API: POST https://comms.egosms.co/api/v1/json/

### 2.1 Required site config keys

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_api_url "https://comms.egosms.co/api/v1/json/"

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_username "REPLACE_WITH_EGOSMS_USERNAME"

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_password "REPLACE_WITH_EGOSMS_PASSWORD"

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_sender_id "REPLACE_WITH_SENDER_ID"

# API key if required by your eGoSMS account (optional)
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_api_key "REPLACE_WITH_API_KEY_IF_USED"

# Start in demo mode (safe default)
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_demo_mode 1
```

### 2.2 eGoSMS request format

```json
POST https://comms.egosms.co/api/v1/json/
Content-Type: application/json

{
  "Username": "your-username",
  "Password": "your-password",
  "SenderId": "SmartLife",
  "MessageParameters": [
    {
      "Number": "256700000000",
      "Text": "Hello from NSSF SmartLife Flexi"
    }
  ]
}
```

### 2.3 Phone number formats supported

- Uganda local: `07XXXXXXXX` → normalised to `256XXXXXXXXX`
- International: `+2567XXXXXXXX` or `2567XXXXXXXX` → used as-is

### 2.4 Verify SMS config

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com execute \
  nssf_smart_savers.integrations.phahapa_sms.get_config_status
# Expected:
# {"configured": true, "api_url": "configured", "username": "configured", ...}
```

### 2.5 Send a controlled test SMS

```bash
bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_demo_mode 0

SMARTLIFE_SEND_LIVE_TEST=1 \
SMARTLIFE_TEST_PHONE=+256700000000 \
  python3 scripts/live_send_test.py

bench --site nssf-smartlifeflexi.nile-gov-demo.com set-config \
  smartlife_phahapa_sms_demo_mode 1
```

### 2.6 Rotate or revoke SMS credentials

1. Generate new credentials in eGoSMS dashboard
2. `bench --site ... set-config smartlife_phahapa_sms_password "NEW_PASSWORD"`
3. Deactivate old credentials in eGoSMS dashboard

---

## 3. Demo mode behaviour

Both providers support demo mode independently:

| Setting | Behaviour |
|---|---|
| `smartlife_zeptomail_demo_mode = 1` | No emails sent; logged as `Demo Mode` |
| `smartlife_phahapa_sms_demo_mode = 1` | No SMS sent; logged as `Demo Mode` |
| Either = 0 | Live sends active — credentials must be configured |

Safe default: always start with demo mode enabled. Only disable for controlled testing.

---

## 4. Consent rules

The messaging service enforces consent before every send:

| Template | Requires `consent_to_contact = true`? |
|---|---|
| Most templates | Yes |
| `consent_missing_education` | No — educational content only |

If consent is missing:
- Send is skipped
- Communication Log records `Skipped - No Consent`
- No error is raised to the user

---

## 5. Communication log

Every preview and send attempt is logged in `SmartLife Communication Log`:
- Recipient is always stored masked (`070****545`, `ro***@domain.com`)
- Raw phone/email is never stored in the log
- Provider token and API keys are never stored in the log
- Logs are visible to approved staff roles only

---

## 6. What not to commit

Never commit:
- `smartlife_zeptomail_token` value
- `smartlife_phahapa_sms_password` value
- `smartlife_phahapa_sms_api_key` value
- Any file containing real credentials
- `.env` files with real values

The smoke test (`scripts/smoke_test_messaging.sh`) scans for committed credential patterns.

---

## 7. Troubleshooting

### Email not sending

1. Check demo mode: `get_messaging_config_status` API or `/smartlife-messaging-demo`
2. Check `smartlife_zeptomail_token` is set and starts with `Zoho-enczapikey `
3. Check `smartlife_zeptomail_from_email` is a verified ZeptoMail sender
4. Check Frappe error log: `bench --site ... error-log`

### SMS not sending

1. Check demo mode
2. Check `smartlife_phahapa_sms_username` and `password` are set
3. Check phone number is in valid Ugandan format
4. Check eGoSMS account has credit balance
5. Check Frappe error log

### Communication log not created

1. Check `SmartLife Communication Log` DocType exists (run `bench migrate` if newly deployed)
2. Check Frappe error log for insert errors
