# NSSF SmartLife Flexi — Release Acceptance Checklist

Use this checklist to verify that all deployment stages are completed and validated.

---

## 1. Repository & Git Verification
- [ ] Working tree is clean on the target server branch (`phase-1-smartlife-onboarding`).
- [ ] Merge commit successfully contains branches through Phase 8.
- [ ] Verification commits (`2c22e04`, `d0e2786`, `4339a7f`, `24d9b75`, `f4e522a`, `5ab1b69`) are present in git log.

---

## 2. Frappe Migration & Environment Setup
- [ ] Database sync (`bench migrate`) executed successfully.
- [ ] Build operations (`bench build`) completed with exit code 0.
- [ ] System cache cleared and supervisor services restarted successfully.
- [ ] Environmental credentials for Pesapal, ZeptoMail, and Phahapa registered in `site_config.json`.
- [ ] `SmartLife Personalisation Team` role created manually in Frappe Desk.

---

## 3. Automation Smoke Tests
- [ ] Phase 1 Smoke Test (`smoke_test.sh`): 140+ passing (0 failed).
- [ ] Phase 2 Smoke Test (`smoke_test_phase_2.sh`): 99+ passing (0 failed).
- [ ] Phase 3 Smoke Test (`smoke_test_phase_3.sh`): 68 passing (0 failed).
- [ ] Phase 4 Smoke Test (`smoke_test_phase_4.sh`): 37 passing (0 failed).
- [ ] Phase 5 Smoke Test (`smoke_test_phase_5.sh`): 30 passing (0 failed).
- [ ] Phase 6 Smoke Test (`smoke_test_phase_6.sh`): 33 passing (0 failed).
- [ ] Phase 7 Smoke Test (`smoke_test_phase_7.sh`): 23 passing (0 failed).
- [ ] Phase 8 Smoke Test (`smoke_test_phase_8.sh`): All passing (0 failed).

---

## 4. UI Route Access Control & Privacy
- [ ] Guest users visiting `/smartlife-staff-queue-full` are blocked by a login gate.
- [ ] Guest users visiting `/smartlife-command-centre` are blocked by a login gate.
- [ ] Support requests created via `/smartlife-support-demo` return only the reference ID.
- [ ] Command Centre analytics APIs return only aggregate totals (0 lead listings or unmasked DOB/NIN/phones).
- [ ] Secret scan confirms no sandbox or production API keys are hardcoded in the codebase.
