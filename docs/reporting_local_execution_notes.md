# SmartLife Flexi — Reporting Local Execution Notes

## Status
`Reporting enhancement blueprint complete / implementation pending`

---

## 1. What was Completed

- **Reporting Blueprint Documentation**: Created the strategy, metric dictionary, board reporting pack, personalization manager reporting pack, and technical implementation plan.
- **Reporting Validation Script**: Prepared `scripts/smoke_test_reporting.sh` to check for all reporting-pack files and their attributes.

---

## 2. Existing Analytics Capability Summary
The application currently features a basic Command Centre dashboard under `/smartlife-command-centre` backed by 6 aggregate APIs in `api.py`. They retrieve lead counts, dropoffs, campaign distributions, age bands, and birth month categories, keeping raw PII excluded from the client.

## 3. Reporting Architecture Decision
Selected **Option D (Documentation-only reporting blueprint)** to prevent risky code revisions on a verified prototype branch prior to remote staging database validation. This strategy ensures zero regression risks on live checkout, payment, or support modules.

## 4. Files Created
* **New**: `docs/smartlife_reporting_charts_strategy.md`
* **New**: `docs/smartlife_reporting_metric_dictionary.md`
* **New**: `docs/smartlife_board_reporting_pack.md`
* **New**: `docs/smartlife_personalisation_manager_reporting_pack.md`
* **New**: `docs/smartlife_reporting_implementation_plan.md`
* **New**: `docs/reporting_local_execution_notes.md`
* **New**: `scripts/smoke_test_reporting.sh` (executable)

---

## 5. Security, PII, and Small-Count Suppression Approach
- **Access Control**: Future endpoints must reject guest calls and restrict access to Personalisation Team roles.
- **PII Suppression**: Raw identifiers (NIN, phone, name, email) are blocked from all query builders.
- **Small-Count Suppression**: Cohorts below a threshold of **5** are grouped to ensure customer anonymity is preserved.

---

## 6. Required Server Validation Steps
Once the branch is merged on the target server, the operator should run `scripts/smoke_test_reporting.sh` to verify document presence, compile python scripts, and proceed with database performance indexation.

---

## 7. Known Limitations
Local review runs offline; query latencies on large database datasets must be validated in staging UAT environments.

---

## 8. Final Self-Critique

- **Which chart is most useful to the board?**
  The *SmartLife conversion funnel*, as it clearly shows where the product leaks interest and drops off before cash deposits.
- **Which chart is most useful to the personalisation manager?**
  The *Acquisition Quality and Campaign Performance* report, allowing them to pause low-performing ad spend.
- **Which metric is most likely to be misunderstood?**
  The *Payment Success Rate*, as sandbox simulations must not be mixed with live transaction success.
- **Which metric needs better data before board use?**
  *Activation Quality*, since it requires linking leads to bank records or third-party wallets.
- **Which chart has the highest privacy risk?**
  *Diaspora country/location breakdown*, where unique countries with single signups could leak user identity.
- **Which chart should not be shown until server data is validated?**
  *Staff Operational Throughput*, since mock logs do not represent actual staff working hours.
- **What would Adobe Target, VWO or AB Tasty expect that is not yet present?**
  Automatic traffic splitting (A/B testing) at the route layer.
- **What should be added later when real behavioural data accumulates?**
  Cohorts by savings duration and dormancy risk predictors.
- **What reporting feature could become dangerous if misused?**
  Unmasked staff logs, if shared outside the Personalisation Team.
- **What should the board not overinterpret?**
  High onboarding starts counts (starts are simple traffic volume; final converted deposits are what matter).
