# KPI Business Rules

## Claim Status Definitions

| Status | Rule |
|--------|------|
| SUBMITTED | Has a valid submission date |
| APPROVED  | Final status = APPROVED |
| DENIED    | Final status = DENIED |
| PENDING   | Submitted but no final outcome yet |
| SETTLED   | Final status = SETTLED (treated as approved) |

## KPI Formulas

| KPI | Formula |
|-----|---------|
| Decided Claims | APPROVED + DENIED + SETTLED |
| Approval Rate  | Approved / Decided × 100 |
| Denial Rate    | Denied / Decided × 100 |
| Processing Time | decision_date − submission_date |
| Delayed Claim  | Processing days > 30 (default threshold) |
| Claim → Approval Gap   | claimed − approved |
| Approval → Payment Gap | approved − paid |

## Financial Definitions

| Term | Meaning |
|------|---------|
| Claimed Amount  | Amount billed to insurance company |
| Approved Amount | Amount accepted by insurance company |
| Paid Amount     | Amount actually received by hospital |

## Data Rules

- BR-014: All data is synthetic (fictional).
- No real patient personal or medical information.