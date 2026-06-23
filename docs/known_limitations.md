# SmartLife Flexi — Known Limitations

This document lists the known technical and operational limitations of the SmartLife Flexi voluntary saving growth prototype.

---

## Technical and Operational Gaps

1. **Demo Environment Data Restriction**
   - The application is a prototype and must not contain real NSSF member data. All leads, intents, logs, and support requests created are for demonstration purposes only.

2. **Sandbox Payment Restrictions**
   - The Pesapal integration is active in sandbox/demo modes only. Live payments cannot be processed without production merchant credentials. Live mode is blocked at the code adapter level to prevent accidental live charges.

3. **No App-Layer Rate Limiting**
   - Rate limiting is not implemented at the application layer. Protection against brute force attacks, denial of service (DoS), or API spamming must be configured at the Nginx, API Gateway, or load balancer levels.

4. **WhatsApp Integration Limitations**
   - The WhatsApp messaging channel is "copy-ready" (it generates and displays pre-formatted templates and instructions for the agent to copy). The automated WhatsApp API is not connected.

5. **Manual Role Assignment**
   - There is no automated provisioning of system roles. User roles such as `SmartLife Personalisation Team` and `NSSF Staff` must be assigned manually by a system manager in Frappe Desk.

6. **Database Migration Requirement**
   - Any modifications to DocType definitions, custom fields, or schema configurations require running `bench --site [site-name] migrate` to rebuild database tables and clear old descriptors.

7. **Outreach Automation Trigger**
   - Birthday-based messaging and follow-up alerts require the setup and scheduling of a background cron task (Frappe scheduler) to query daily birthdays and trigger notification events automatically.

8. **Single Site Deployment**
   - The application is optimized for single-tenant site deployment. Multi-tenant instances sharing the same application container require custom site-specific routing and environment checks.

9. **No Default Role Audit Logs**
   - Frappe does not track role modification logs or desk view access history by default. It is highly recommended to enable Frappe's audit log settings in production to track staff access to PII.
