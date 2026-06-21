# Payment Architecture — Pesapal (Phase 1 Demo)

## Status: SIMULATED in Phase 1

## What Exists Now
- SmartLife Demo Payment DocType records payment intent and simulated outcome
- Payment reference: `SL-DEMO-XXXXXXXX` format
- Provider mode: `demo` (hardcoded)
- No real API calls to Pesapal in Phase 1

## What Pesapal Provides (Phase 2)
- OAuth2 token-based API
- RegisterIPN endpoint (register callback URL)
- SubmitOrderRequest endpoint (initiate payment)
- IPN callback (payment status notification)
- GetTransactionStatus endpoint (verify payment)

## Endpoints (Phase 2, Sandbox)
- Base: https://cybqa.pesapal.com/pesapalv3
- Auth: POST /api/Auth/RequestToken
- Register IPN: POST /api/URLSetup/RegisterIPN
- Submit Order: POST /api/Transactions/SubmitOrderRequest
- Transaction Status: GET /api/Transactions/GetTransactionStatus

## Credentials Required (NOT in Phase 1)
- PESAPAL_CONSUMER_KEY
- PESAPAL_CONSUMER_SECRET
- PESAPAL_IPN_URL (your Frappe site callback URL)

## What Must NOT Be Committed
- Real Pesapal credentials
- Live API tokens

## Deferred to Phase 2
- Sandbox integration
- IPN webhook handler
- Payment retry logic
- Refund handling
- Multi-currency (Phase 3+)
