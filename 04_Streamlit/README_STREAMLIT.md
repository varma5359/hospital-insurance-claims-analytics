# 🏥 Streamlit Dashboard — User Guide

**MediCare Multi-Specialty Hospital · Insurance Claims Analytics**

This guide explains what each part of the dashboard does, how to
filter data, and how to read the numbers.

---

## 1. What This Dashboard Does

It reads hospital insurance claim data and answers these questions:

- How many claims were submitted?
- How many were approved, denied, or are still pending?
- Which insurance companies deny the most claims?
- Which departments generate the most rejections?
- How long does a claim take to be decided?
- Where is money being lost (claimed vs approved vs paid)?

No manual investigation needed — everything comes from your database.

---

## 2. How to Launch It

From the project root:

```bash
streamlit run 04_Streamlit/app.py
```

Your browser opens at:

```
http://localhost:8501
```

To stop the app: press **Ctrl + C** in the terminal.

---

## 3. Dashboard Layout

```
┌──────────────────────────────────────────────────────────┐
│  🏥 Hospital Insurance Claims Analytics                  │
│  Data source: SQL Server                                 │
├──────────────────────────────────────────────────────────┤
│  🔍 SIDEBAR FILTERS        │  MAIN AREA                  │
│                            │                             │
│  • Date range              │  📊 KPI CARDS               │
│  • Insurance company       │  ┌────┬────┬────┬────┐      │
│  • Department              │  │    │    │    │    │      │
│  • Status                  │  └────┴────┴────┴────┘      │
│  • Claim type              │                             │
│                            │  📈 STATUS CHARTS           │
│                            │  (bar + pie)                │
│                            │                             │
│                            │  🚫 REJECTION REASONS       │
│                            │  ⏱ DELAYED CLAIMS           │
│                            │  💰 FINANCIAL SUMMARY       │
│                            │                             │
│                            │  TABS:                      │
│                            │  [Overview][Companies]      │
│                            │  [Departments][Investigation]│
└──────────────────────────────────────────────────────────┘
```

---

## 4. Sidebar Filters — How to Use Them

Located on the **left side**. Every filter updates the entire dashboard instantly.

| Filter | What it does | Example |
|--------|--------------|---------|
| **Submission date range** | Shows only claims submitted between two dates | `2022-01-01` to `2023-12-31` |
| **Insurance company** | Shows only claims from one payer | `Commercial_PPO` |
| **Department** | Shows only one medical specialty | `Cardiology` |
| **Status** | Shows only one claim outcome | `DENIED` |
| **Claim type** | Shows only one place of service | `Emergency_Room` |

**Tip:** Select **"All"** in any dropdown to remove that filter.

---

## 5. KPI Cards — What Each Number Means

The top row has four big numbers.

### 5.1 Total Claims

```
📊  Total Claims
    120,000
```

**What it means:** Total number of insurance claims in the current selection.

**Formula:** `COUNT(all rows)`

**Business use:** Confirms the volume the claims team is processing.

---

### 5.2 Approval Rate

```
✅  Approval Rate
    62.5 %
```

**What it means:** Percentage of decided claims that were approved or settled.

**Formula:**
```
Approval Rate = (Approved + Settled) ÷ (Approved + Denied + Settled) × 100
```

**Business use:** Higher is better. If this drops month-over-month, investigate.

---

### 5.3 Denial Rate

```
❌  Denial Rate
    37.5 %
```

**What it means:** Percentage of decided claims that were denied.

**Formula:**
```
Denial Rate = Denied ÷ (Approved + Denied + Settled) × 100
```

**Business use:** Even a 1% reduction in denial rate can save lakhs in revenue.

---

### 5.4 Avg Processing

```
⏱  Avg Processing
    34.2 days
```

**What it means:** Average number of days between claim submission and decision.

**Formula:** `AVG(decision_date − submission_date)`

**Business use:** Compare against the threshold (30 days). Higher = slower cash flow.

---

## 6. Charts — How to Read Them

### 6.1 Claims by Status (Bar + Pie)

**Left chart (bar):** Absolute count of claims per status.
**Right chart (pie):** Percentage share per status.

**Reading example:**
- If the bar for `DENIED` is tall → many claims are being rejected.
- If the pie shows `PENDING` growing → claims are stuck in the system.

---

### 6.2 Rejection Reasons Table

Lists each denial reason with the number of claims.

**Example output:**
| rejection_reason | count |
|------------------|-------|
| CO-4             | 4,231 |
| CO-97            | 3,109 |
| CO-16            | 2,872 |

**How to use:**
- **CO-4** = "Procedure not consistent with diagnosis" → check coding accuracy
- **CO-97** = "Duplicate claim" → check submission process
- **CO-16** = "Missing information" → check documentation completeness

**Action:** Assign the top 3 reasons to a task force each month.

---

### 6.3 Delayed Claims Table

Shows every decided claim older than 30 days.

**Columns shown:**
| Column | Meaning |
|--------|---------|
| `claim_id` | Unique claim |
| `company_name` | Who owes the payment |
| `dept_name` | Treating department |
| `processing_days` | Days elapsed |
| `status` | Current outcome |

**How to use:** Call the insurance company about the oldest / highest-value rows first.

---

### 6.4 Financial Summary

Three big numbers plus two gaps:

| Card | Formula | Business meaning |
|------|---------|------------------|
| **Total Claimed** | `SUM(claimed_amount)` | What the hospital billed |
| **Total Approved** | `SUM(approved_amount)` | What the insurer accepted |
| **Total Paid** | `SUM(paid_amount)` | What the hospital actually received |
| **Claim → Approval Gap** | `Claimed − Approved` | Loss at approval stage |
| **Approval → Payment Gap** | `Approved − Paid` | Loss at payment stage |

**Example reading:**
- Claimed ₹100Cr, Approved ₹85Cr → **₹15Cr gap at approval** (coding / eligibility issues)
- Approved ₹85Cr, Paid ₹70Cr → **₹15Cr gap at payment** (short payments / write-offs)

**Action:** Each gap has a different fix. Approval gap = fix documentation. Payment gap = follow up on underpayments.

---

## 7. Tabs Explained

### 7.1 📊 Overview Tab

The main view. Shows:
- KPI cards
- Status charts
- Rejection reasons
- Delayed claims
- Financial summary

**Use this** for a quick daily / weekly check.

---

### 7.2 🏢 Companies Tab

Compares insurance companies side-by-side.

**Table columns:**
| Column | Meaning |
|--------|---------|
| `company_name` | Payer name |
| `total_claims` | Volume |
| `approved` | Approved count |
| `denied` | Denied count |
| `approval_rate` | % approved |
| `denial_rate` | % denied |
| `avg_processing_days` | Speed |
| `total_claimed` | Billed ₹ |
| `total_paid` | Received ₹ |

**Chart:** Denial rate per company — the higher the bar, the more problematic.

**Use this** when negotiating contracts or deciding which payers need escalation.

---

### 7.3 🏥 Departments Tab

Compares hospital departments.

**Table columns:**
| Column | Meaning |
|--------|---------|
| `dept_name` | Department (Cardiology, Orthopedics, ...) |
| `total_claims` | Volume from this department |
| `denied` | Denied count |
| `denial_rate` | % denied |
| `avg_processing_days` | Speed |
| `total_claimed` | Billed ₹ |

**Chart:** Volume per department.

**Use this** to identify departments that need coding/documentation training.

---

### 7.4 🔎 Investigation Tab

Look up a single claim by ID.

**Steps:**
1. Select a **Claim ID** from the dropdown
2. Full claim row appears — every column from the database

**Use this** when the claims team escalates a specific claim.

---

## 8. Typical Workflows

### Workflow A — Morning Check

1. Open dashboard
2. Look at **Denial Rate** card → is it higher than yesterday?
3. If yes, open **Overview → Rejection Reasons** → identify top 3
4. Open **Companies tab** → which payer's denial rate spiked?
5. Assign follow-up.

---

### Workflow B — Weekly Revenue Review

1. Filter date range to **this week**
2. Note **Claim → Approval Gap** and **Approval → Payment Gap**
3. Open **Companies tab** → which company has the biggest payment gap?
4. Open **Departments tab** → which department has the highest denial rate?
5. Send escalation emails.

---

### Workflow C — Specific Claim Investigation

1. Go to **Investigation tab**
2. Pick the claim ID from the escalation email
3. Copy the details (submission date, status, rejection reason, amounts)
4. Reply to the escalation with facts.

---

## 9. Interpreting Common Scenarios

| What you see | What it means | What to do |
|--------------|---------------|------------|
| Denial rate > 30% | Too many rejections | Review top rejection reasons |
| Approval rate < 60% | Documentation / coding issues | Training needed |
| Many `PENDING` claims | Claims stuck | Follow up with payers |
| High Claim→Approval gap | Under-coding, missing docs | Audit billing team |
| High Approval→Payment gap | Underpayments, write-offs | Reconcile with payers |
| One company's denial rate double the average | That payer is stricter | Contract review |
| One department's denial rate very high | Department-specific issue | Targeted training |

---

## 10. Data Source Indicator

The header shows where data comes from:

| Label | Meaning |
|-------|---------|
| `SQL Server` | Loaded from SQL Server `vw_claims` view |
| `CSV (DenialIQ)` | Loaded from `data/claims_main.csv` |
| `Sample` | Small built-in sample (DB + CSV both unavailable) |

If you see `Sample`, check:
1. SQL Server running?
2. `.env` file correct?
3. `data/claims_main.csv` present?

---

## 11. Troubleshooting

| Problem | Fix |
|---------|-----|
| Blank KPI cards | Reset sidebar filters (select "All") |
| Charts not showing | `pip install matplotlib` |
| `Data source: Sample` | Check SQL Server + CSV file |
| Slow load | First load is slowest — subsequent loads cached |
| Filters return 0 rows | Widen date range or clear filters |
| `ModuleNotFoundError` | Run from project root, not from inside `04_Streamlit/` |

---

## 12. Refreshing the Data

Data is **cached** on first load for speed.

To force refresh:
- Click the **⋮** menu (top right) → **Rerun**
- Or press **R** in the browser

To reload from SQL Server completely: stop the app and restart.

---

## 13. Who Should Use This Dashboard

| Role | Primary tab | What they look for |
|------|-------------|-------------------|
| **Claims Manager** | Overview | Denial rate, rejection reasons |
| **Revenue Cycle Manager** | Companies | Payer performance |
| **Finance Manager** | Overview | Claimed / Approved / Paid gaps |
| **Hospital Manager** | Departments | Department-level issues |
| **Claims Team** | Investigation | Single-claim lookup |

---

## 14. Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│  DASHBOARD CHEAT SHEET                                   │
├──────────────────────────────────────────────────────────┤
│  Approval Rate  = Approved ÷ Decided × 100               │
│  Denial Rate    = Denied   ÷ Decided × 100               │
│  Decided        = Approved + Denied + Settled            │
│  Processing     = decision_date − submission_date        │
│  Delayed        = processing_days > 30                   │
│  Claim→Approval Gap   = claimed − approved               │
│  Approval→Payment Gap = approved − paid                  │
├──────────────────────────────────────────────────────────┤
│  Filters → sidebar                                       │
│  Charts  → Overview tab                                  │
│  Payers  → Companies tab                                 │
│  Depts   → Departments tab                               │
│  Single  → Investigation tab                             │
└──────────────────────────────────────────────────────────┘
```

---

## 15. Support

- **Business questions** → Claims Manager
- **Data questions** → Analytics / IT
- **Code issues** → See `README.md` (project root)
- **Logs** → `06_Logs/application.log`

---

> **Note:** All data in this dashboard is **synthetic** — no real
> patient information is displayed or stored.