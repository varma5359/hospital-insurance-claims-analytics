# Requirements

## Functional Requirements

| ID | Description |
|----|-------------|
| FR-001 | Display total number of claims for selected period |
| FR-002 | Show claims by status (count + %) |
| FR-003 | Calculate approval rate and denial rate |
| FR-004 | Summarize rejection reasons |
| FR-005 | Calculate processing time; flag delayed claims |
| FR-006 | Compare insurance companies on volume, rates, time, money |
| FR-007 | Analyze claim performance by department |
| FR-008 | Show claimed, approved, paid amounts and gaps |
| FR-009 | Allow viewing individual claim details |
| FR-010 | Filter results by date, company, department, status, type |

## Non-Functional Requirements

| ID | Description |
|----|-------------|
| NFR-001 | Application responds quickly on project dataset |
| NFR-002 | KPIs must match business rules exactly |
| NFR-003 | App must not crash on missing/invalid data |
| NFR-004 | Important events written to application log |
| NFR-005 | Data processing must be traceable (auditable) |
| NFR-006 | Business logic in reusable Python modules |
| NFR-007 | Synthetic data only; no hardcoded credentials |
| NFR-008 | Business logic covered by pytest tests |
| NFR-009 | UI must be easy for hospital business users |