# SmartLife Flexi — Production Readiness Checklist

This checklist outlines the infrastructure, application, privacy, verification, and sign-off requirements that must be completed before launching the SmartLife Flexi application in a live production environment.

---

## Production Readiness Checklist

### Infrastructure
- [ ] Production server provisioned (separate from demo)
- [ ] SSL certificate installed
- [ ] Frappe production mode configured
- [ ] Backups configured and tested
- [ ] Monitoring and alerting set up

### Application
- [ ] SmartLife Personalisation Team role created and assigned
- [ ] NSSF Staff role assigned to authorised users
- [ ] Pesapal production credentials configured (env var / site config)
- [ ] Phahapa SMS production credentials configured
- [ ] ZeptoMail production email credentials configured
- [ ] Demo mode disabled or clearly labelled
- [ ] Rate limiting configured at Nginx layer
- [ ] CORS configured for production domain

### Data and Privacy
- [ ] NSSF DPO sign-off obtained on PII handling and data retention
- [ ] Data retention schedule defined and implemented
- [ ] Analytics pipeline reviewed (no PII to GA4/GTM/Clarity)
- [ ] Consent workflow reviewed by legal
- [ ] Staff PII access documented and authorised

### Smoke Tests
- [ ] Phase 1 smoke test passes on production server
- [ ] Phase 2 smoke test passes on production server
- [ ] Phase 3 smoke test passes on production server
- [ ] Phase 4 smoke test passes on production server
- [ ] Phase 5 smoke test passes on production server
- [ ] Phase 6 smoke test passes on production server
- [ ] Phase 7 smoke test passes on production server

### Sign-off
- [ ] NSSF Technical Lead sign-off
- [ ] NSSF DPO sign-off on PII
- [ ] System integrator sign-off
- [ ] Anti-Gravity / build team sign-off
