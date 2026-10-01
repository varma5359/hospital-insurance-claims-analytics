# User Acceptance Testing (UAT) — Execution Log

Tester : ________________
Date   : ________________
Env    : Windows + SQL Server + Streamlit

| AC ID | Test | Steps | Expected | Result | Notes |
|-------|------|-------|----------|--------|-------|
| AC-001 | Claim volume | Open app | Total Claims card shows number | ⬜ | |
| AC-002 | Status breakdown | Overview tab | Bar + pie by status | ⬜ | |
| AC-003 | Denial rate | Overview tab | Denial Rate card matches formula | ⬜ | |
| AC-004 | Rejections | Overview tab | Table of reasons + counts | ⬜ | |
| AC-005 | Processing time | Overview tab | Avg Processing card > 0 | ⬜ | |
| AC-006 | Delayed claims | Overview tab | Claims > 30 days listed | ⬜ | |
| AC-007 | Financial totals | Overview tab | Claimed / Approved / Paid shown | ⬜ | |
| AC-008 | Company filter | Sidebar → company | KPIs update | ⬜ | |
| AC-009 | Department filter | Sidebar → dept | KPIs update | ⬜ | |
| AC-010 | Claim investigation | Investigation tab | Full row shown for selected claim | ⬜ | |
| AC-011 | Logs written | Open `06_Logs/application.log` | Events visible | ⬜ | |
| AC-012 | Tests pass | `pytest 05_Testing/ -v` | 30 passed | ⬜ | |

**Result legend:** ✅ Pass · ❌ Fail · ⬜ Not Run

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Claims Manager | | | |
| Revenue Cycle Manager | | | |
| Finance Manager | | | |
| IT / Analytics | | | |