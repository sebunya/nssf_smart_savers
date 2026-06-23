# SmartLife Flexi — Advanced Reporting Implementation Plan

This implementation plan details the phases, file paths, and testing validation steps required to introduce the advanced reporting layer on the NSSF production server.

---

## 1. Selected Implementation Architecture
- **Option Chosen**: **Option D (Documentation-only reporting blueprint)**.
- **Rationale**: Implementing complex aggregate query APIs, DB queries, UI tabs, and charting scripts in local-offline mode is highly risky prior to target staging database validation. Maintaining zero-code-modification safeguards keeps existing verified code robust and prevents regressions.
- **Future Integration Path**: Extend the existing `/smartlife-command-centre` route once server UAT verification completes.

## 2. Target Files for Future Enhancement
- `nssf_smart_savers/api.py`: Introduce aggregate endpoints.
- `nssf_smart_savers/www/smartlife-command-centre.html`: Add tabbed UI views (Board vs Personalisation Manager).
- `nssf_smart_savers/www/smartlife-command-centre.py`: Retrieve variables and pass them to the template context.

## 3. Query and Caching Strategy
- **SQL Aggregations**: Use standard `frappe.db.count` and SQL database groupings rather than looping over documents to conserve system memory.
- **Caching**: Dashboard metrics should be cached via Redis (`frappe.cache().set_value`) with an expiration period of **4 hours** to prevent high server query loads during peak traffic.

## 4. Access Control Strategy
- All reporting endpoints must use the `@frappe.whitelist()` decorator *without* `allow_guest=True`.
- The backend must call the existing `_require_personalisation_access()` method to block non-staff users and prevent horizontal privilege escalation.

## 5. Small-Count Suppression Strategy
- Implement a helper function `suppress_small_counts(data_dict, threshold=5)`:
  ```python
  def suppress_small_counts(data_dict, threshold=5):
      for key, val in list(data_dict.items()):
          if isinstance(val, int) and 0 < val < threshold:
              data_dict[key] = 0 # or omit
  ```
- This prevents identifying specific customers in small cohorts (e.g. unique diaspora country signups).

## 6. Server Validation Plan
- Merge branch `claude/cool-bell-t7n0hs`.
- Run database migrations (`bench migrate`).
- Verify that custom indexes are added to fields `saver_type`, `savings_goal`, `payment_status`, and `assigned_staff` to support quick analytics queries.

## 7. User Acceptance Testing (UAT) Plan
- Populate sandbox database with 10,000 mock leads.
- Compare dashboard metrics against direct SQL queries to confirm mathematical accuracy.
- Confirm dashboard renders correctly on Safari iOS and Chrome Android viewports.

## 8. Rollback Plan
- Revert commit changes to `/smartlife-command-centre` files.
- Clear Redis query cache.
- Restart supervisor processes.

## 9. Implementation Phases
1. **Phase 1: Blueprint** (Current state) - Finalize metric formulas, schemas, and mockup shapes.
2. **Phase 2: Local Staging Implementation** - Write the controller queries and script files on the target server.
3. **Phase 3: Security Review** - DPO verifies PII compliance and small-count suppression functions.
4. **Phase 4: UAT Verification** - Run performance validation on a staging database.
5. **Phase 5: Release and Board Presentation** - Present dashboard views to NSSF stakeholders.
