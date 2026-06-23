# SmartLife Flexi — Advanced Reporting and Charts Strategy

This document defines the strategic reporting architecture, decision framework, and security boundaries for NSSF SmartLife Flexi dashboards.

---

## 1. Purpose of the Reporting Layer
To empower NSSF leadership with governance-grade metrics and growth managers with operational insights. Every chart and metric is designed to drive key business decisions regarding voluntary savings adoption, customer friction, operational bottlenecks, and product risk.

## 2. Audience Split
- **NSSF Board / Executive Committee**: Focuses on long-term growth, contribution volume, adoption velocity, demographic risk, compliance, and product performance.
- **SmartLife Personalisation Manager / Growth Team**: Focuses on micro-funnel dropoffs, campaign performance, staff follow-up effectiveness, system latency, communication suppressions, and UAT feedback.

## 3. Key Business Questions
- Are we acquiring the intended demographic segments?
- Where do prospects drop out of the onboarding funnel?
- Are payment callbacks resolving cleanly?
- What support topics act as the primary friction points?
- Are staff follow-up tasks successfully activating dormant leads?

## 4. Decision Framework
- **Metric Worsening (e.g. Funnel Dropoff > 15%)**: Alert is triggered to Growth Team. Action: Inspect channel onboarding friction or payment gateway callbacks.
- **Adoption Skew**: Board assesses if voluntary savings are failing to attract informal/diaspora savers, adjusting campaign funding accordingly.

## 5. Data Sources
All metrics are derived from the following core DocTypes:
- `SmartLife Demo Lead` (Onboarding database)
- `SmartLife Contribution Intent` (Payment transactions)
- `SmartLife Communication Log` (Notification logs)
- `SmartLife Support Request` (Customer queries)

## 6. Metric Hierarchy
- **Level 1 (KPIs)**: Total Active Savers, Completion Rate, Total Contribution Volume.
- **Level 2 (Diagnostic)**: Funnel Stage Completion, Segment Performance, Lead Temperatures.
- **Level 3 (Operational)**: Queue Ageing, Staff Response Times, Delivery Failures.

## 7. Chart Inventory
- Onboarding Funnel (Horizontal Stage Bars)
- Segment Mix (Donut Chart)
- Payment Status Breakdown (Stacked Horizontal Bar)
- Campaign Performance (Horizontal Bar)
- Support Categories (Bar Chart)

## 8. Filter Strategy
- **Allowed**: Date range, Segment, Goal, Age-band, Contact channel preference.
- **Rejected**: Individual identifiers (NIN, Phone, Name, Email, Address, Payment reference).

## 9. Access Control Model
Strictly restricted to the following roles in Frappe:
- `SmartLife Personalisation Team`
- `NSSF Staff`
- `System Manager`

All guest endpoint access is blocked.

## 10. PII and Privacy Approach
Reports use pre-aggregated counters. Raw customer data is never queried directly by the frontend, preventing memory exposure.

## 11. Small-Count Suppression Rule
Any group, segment, or filter returning a lead count of **less than 5** is automatically suppressed or aggregated into an "Other" category to prevent individual re-identification.

## 12. Board Reporting Pack Strategy
Highly summarized cards and charts focusing on overall conversion, financial growth, demographic alignment, and deployment readiness.

## 13. Personalisation Manager Reporting Pack Strategy
Granular diagnostic tools detailing template success rates, staff-assisted queues, and payment callback latencies.

## 14. Frappe Implementation Approach
Utilizes standard custom pages backed by secure whitelist python controller methods to fetch JSON-preaggregated numbers.

## 15. Server Validation Requirements
Database indexes must be verified for performance once test data reaches 10,000+ mock records.

## 16. Known Limitations
Local UAT does not run on a live MariaDB server. DB queries are simulated via mocks.

## 17. Future Enhancements
Incorporate predictive modeling for lead dormancy alerts once historical transaction history accumulates (post-launch).
