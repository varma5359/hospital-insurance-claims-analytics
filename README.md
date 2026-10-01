![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2019+-red)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-ff4b4b)
![Tests](https://img.shields.io/badge/tests-37%20passed-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-active-success)

# 🏥 Hospital Insurance Claims & Revenue Analytics

An end-to-end Business Analytics solution for **MediCare Multi-Specialty Hospital**
to monitor insurance claim performance, identify denials, track processing delays,
and analyze financial gaps between **claimed**, **approved**, and **paid** amounts.

Built with **Microsoft SQL Server**, **Python**, **Streamlit**, and **pytest**.

# Developed By: Mr.RaviVarma

---

## 💼 Why This Project Matters (Career Value)

This project is designed to demonstrate the **exact skills** that MNCs and product
companies look for in **Business Analyst**, **Data Analyst**, and **Junior Data
Engineer** roles.

### Job Readiness by Role

| Target Role | Readiness | Notes |
|-------------|-----------|-------|
| Business Analyst (Analytics) | 🟢 85% | Business docs + KPIs + dashboard |
| Data Analyst (Python + SQL) | 🟢 80% | Strong SQL + pandas + visualization |
| BI Developer | 🟡 70% | Streamlit used; MNCs also want Power BI / Tableau |
| Data Engineer (ETL/Cloud) | 🔴 35% | Missing Airflow, dbt, Snowflake, ADF |
| ML Engineer | 🔴 20% | No model training / deployment |
| Full-Stack Developer | 🔴 15% | Streamlit is not full-stack |

### Fresher Readiness

| Experience Level | Ready % | What's Missing |
|------------------|---------|----------------|
| Fresher (0 yrs) | **85%** | Cloud basics, Git workflow |
| 1 year | **75%** | Docker, CI/CD, cloud warehouse |
| 2 years | **60%** | System design, streaming, scale |
| 3+ years | **40%** | Architecture, distributed systems |

**Verdict:** For freshers and early-career professionals, this project places you
in the **top 10% of candidates** for entry-level analytics roles. Adding one cloud
project and one BI tool pushes readiness past **95%**.

### Skills Demonstrated

| Skill Area | Coverage | MNC Value |
|------------|----------|-----------|
| Business Analysis (BRD, KPI rules, UAT) | Complete | ⭐⭐⭐⭐⭐ |
| SQL Server (schema, views, queries) | Complete | ⭐⭐⭐⭐⭐ |
| Python OOP + modules | Complete | ⭐⭐⭐⭐⭐ |
| Pandas analytics | Complete | ⭐⭐⭐⭐⭐ |
| PyODBC + Windows Auth | Complete | ⭐⭐⭐⭐ |
| Streamlit dashboard | Complete | ⭐⭐⭐ |
| pytest unit tests (30+) | Complete | ⭐⭐⭐⭐⭐ |
| Central logging + audit | Complete | ⭐⭐⭐⭐ |
| Data validation | Complete | ⭐⭐⭐⭐⭐ |
| Secrets management (`.env`) | Complete | ⭐⭐⭐⭐ |
| Modular architecture (`src/`) | Complete | ⭐⭐⭐⭐⭐ |
| Documentation (README + user guide) | Complete | ⭐⭐⭐⭐⭐ |

### What This Project Is Missing (To Reach Top-Tier)

| Gap | Why It Matters | Quick Fix |
|-----|----------------|-----------|
| Cloud (AWS / Azure / GCP) | 90% of MNC data lives there | Learn Azure Data Factory |
| Snowflake / BigQuery / Redshift | Modern data warehouse | 1-week course + project |
| Airflow / dbt | Orchestration + transforms | Add small pipeline |
| Power BI / Tableau | MNCs prefer BI tools | Build Power BI version |
| Docker / Kubernetes | Deployment standard | Add `Dockerfile` |
| CI/CD (GitHub Actions) | Auto-test on push | 20-line YAML |
| Star / Snowflake schema | Warehousing standard | Refactor current DB |

Add any 3 → interview callbacks double.

### Who Should Use This Project

- **Freshers** building a portfolio for analytics roles
- **Career switchers** from Excel / manual reporting
- **Interview candidates** needing a deep project to discuss for 30+ minutes
- **Freelancers** quoting similar client work (₹15k–₹40k range)
- **Students** doing final-year analytics / capstone projects

---

## 📌 Table of Contents

1. [Career Value](#-why-this-project-matters-career-value)
2. [Project Overview](#1-project-overview)
3. [Business Problem](#2-business-problem)
4. [Business Objective](#3-business-objective)
5. [Key Features](#4-key-features)
6. [Tech Stack](#5-tech-stack)
7. [Project Structure](#6-project-structure)
8. [Folder & File Reference](#7-folder--file-reference)
9. [Database Schema](#8-database-schema)
10. [KPI Definitions](#9-kpi-definitions)
11. [Setup Guide](#10-setup-guide)
12. [Windows Authentication Setup](#11-windows-authentication-setup)
13. [Running the Project](#12-running-the-project)
14. [Running Tests](#13-running-tests)
15. [Logging](#14-logging)
16. [Screens & Tabs](#15-screens--tabs)
17. [Demo Script](#16-demo-script)
18. [Security Notes](#17-security-notes)
19. [Future Enhancements](#18-future-enhancements)
20. [Author](#19-author)

---

## 1. Project Overview

Hospitals submit hundreds of insurance claims every month. Each claim may be:

- **Approved** and fully paid
- **Partially approved** (approved less than claimed)
- **Denied** (rejected with a reason)
- **Pending** for long periods

Without a centralized analytics system, management cannot easily answer:

- Which insurance companies deny the most claims?
- Which departments generate the most rejections?
- How long does the average claim take to be decided?
- What is the financial gap between claimed, approved, and paid amounts?

This project delivers a **centralized analytics dashboard** that answers these
questions using data — not manual claim-by-claim investigation.

---

## 2. Business Problem

MediCare Multi-Specialty Hospital currently has **limited visibility** into
its insurance claim performance. Management struggles to:

- Identify recurring claim denials
- Detect processing delays
- Understand differences between claimed, approved, and paid amounts
- Compare insurance company performance
- Identify departments with high rejection volumes
- Prioritize follow-up on financially significant claims

The absence of a centralized analytics solution forces the claims team to
investigate individual claims manually — a slow, error-prone process.

---

## 3. Business Objective

Provide a **single analytics platform** that allows:

| Objective | How it is achieved |
|-----------|--------------------|
| Monitor claim volume & status | KPI cards + status charts |
| Analyze approval & denial rates | Calculated KPIs |
| Identify rejection reasons | Denial reasons table |
| Monitor processing time | Days-from-submission metric |
| Compare insurance companies | Companies tab |
| Compare departments | Departments tab |
| Identify financial gaps | Claimed / Approved / Paid analysis |
| Support data-driven decisions | Filters + investigation view |

---

## 4. Key Features

- 📊 **Dashboard** with real-time KPIs
- 🔍 **Multi-dimensional filters** (date, company, department, status, type)
- 📈 **Charts** for status distribution and financial summary
- 🚫 **Rejection reason analysis**
- ⏱ **Delayed claim detection** (configurable threshold)
- 💰 **Financial gap analysis** (Claim → Approval, Approval → Payment)
- 🏢 **Insurance company comparison**
- 🏥 **Department-level analytics**
- 🔎 **Individual claim investigation**
- 📝 **Full application logging**
- ✅ **30+ automated tests** with pytest
- 🔐 **Windows Authentication** — no passwords stored
- 🧪 **Synthetic data only** — no real patient information

---

## 5. Tech Stack

| Layer | Technology |
|-------|------------|
| Database | Microsoft SQL Server |
| Data Access | `pyodbc` + Windows Authentication |
| Data Processing | `pandas`, `numpy` |
| Visualization | `matplotlib`, Streamlit charts |
| Web App | Streamlit |
| Testing | pytest |
| Config | `python-dotenv` |
| Logging | Python `logging` |

---

## 6. Project Structure

```
hospital-insurance-claims-analytics/
│
├── .env                          # Real credentials (NOT committed)
├── .env.example                  # Template for .env
├── .gitignore                    # Ignores secrets + cache
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── pytest.ini                    # pytest configuration
├── conftest.py                   # Root conftest (adds src to path)
├── test_connection.py            # Quick SQL Server connection test
├── quick_load.py                 # DenialIQ CSV → SQL Server bulk loader
├── inspect_denialiq.py           # One-time CSV structure inspector
│
├── data/                         # DenialIQ dataset (CSV)
│   ├── claims_main.csv
│   ├── data_dictionary.csv
│   ├── denial_labels.csv
│   ├── payer_rules.csv
│   └── train_test_split.csv
│
├── 01_Business_Analysis/         # Business documentation
│   ├── BRD.md
│   ├── Requirements.md
│   ├── KPI_Business_Rules.md
│   ├── User_Stories.md
│   └── UAT.md
│
├── 02_Database/                  # SQL Server scripts
│   ├── database.sql
│   ├── analysis_queries.sql
│   ├── database_denialiq.sql
│   └── load_denialiq.sql
│
├── 03_Python_Analysis/           # Analysis layer
│   ├── claims_analysis.ipynb     # Jupyter notebook
│   └── src/                      # Reusable Python modules
│       ├── __init__.py
│       ├── logger.py             # Central logging
│       ├── csv_loader.py         # DenialIQ CSV loader
│       ├── database.py           # SQL Server loader (CSV fallback)
│       ├── data_validation.py    # Data quality checks
│       └── kpi_calculation.py    # All business KPIs
│
├── 04_Streamlit/                 # Web dashboard
│   ├── app.py
│   └── README_STREAMLIT.md       # Dashboard user guide
│
├── 05_Testing/                   # Automated tests
│   ├── conftest.py               # Test fixtures
│   ├── test_claims.py            # 30 KPI tests
│   └── test_csv_loader.py        # 7 CSV loader tests
│
└── 06_Logs/                      # Runtime logs
    └── application.log
```

---

## 7. Folder & File Reference

### 📁 `01_Business_Analysis/`
Holds all **business documents**. No code — pure requirements.

| File | Purpose |
|------|---------|
| `BRD.md` | Business Requirements Document — problem, need, outcome, scope |
| `Requirements.md` | FR-001 to FR-010 and NFR-001 to NFR-009 |
| `KPI_Business_Rules.md` | Formulas for approval rate, denial rate, gaps, delay rules |
| `User_Stories.md` | 8 user stories (US-001 to US-008) |
| `UAT.md` | 10 acceptance tests + sign-off |

### 📁 `02_Database/`
SQL Server scripts.

| File | Purpose |
|------|---------|
| `database.sql` | Creates synthetic DB, 6 tables, sample data |
| `analysis_queries.sql` | 5 ready-made analysis queries |
| `database_denialiq.sql` | Staging table + `vw_claims` view for DenialIQ data |
| `load_denialiq.sql` | BULK INSERT script for the DenialIQ CSV |

### 📁 `03_Python_Analysis/`
Core analysis layer.

| File | Purpose |
|------|---------|
| `claims_analysis.ipynb` | Step-by-step Jupyter notebook analysis |
| `src/logger.py` | Central logging configuration |
| `src/csv_loader.py` | `DenialIQLoader` class — normalises 25-col CSV |
| `src/database.py` | `DatabaseLoader` class — SQL → CSV → sample fallback |
| `src/data_validation.py` | `DataValidator` class — nulls, negatives, dates, statuses |
| `src/kpi_calculation.py` | `ClaimsKPI` class — all business KPIs |

### 📁 `04_Streamlit/`
Web dashboard.

| File | Purpose |
|------|---------|
| `app.py` | Streamlit application — filters, KPI cards, charts, 4 tabs |
| `README_STREAMLIT.md` | Business-user guide to the dashboard |

### 📁 `05_Testing/`
Automated tests.

| File | Purpose |
|------|---------|
| `conftest.py` | `sample_df` and `empty_df` pytest fixtures |
| `test_claims.py` | 30 unit tests across 10 test classes |
| `test_csv_loader.py` | 7 tests for the CSV loader |

### 📁 `06_Logs/`
Runtime logs (auto-created).

| File | Purpose |
|------|---------|
| `application.log` | All app + data processing events |

### 📁 `data/`
DenialIQ synthetic dataset (120K claims).

| File | Purpose |
|------|---------|
| `claims_main.csv` | Main claims table |
| `data_dictionary.csv` | Column definitions |
| `denial_labels.csv` | Denial reason labels |
| `payer_rules.csv` | Payer-specific rules |
| `train_test_split.csv` | ML train/val/test split |

### 📄 Root Files

| File | Purpose |
|------|---------|
| `.env` | Real SQL Server credentials — **not committed** |
| `.env.example` | Safe template showing required keys |
| `.gitignore` | Prevents committing `.env`, caches, and logs |
| `requirements.txt` | Python packages with versions |
| `pytest.ini` | Tells pytest where tests live and how to name them |
| `conftest.py` | Adds `03_Python_Analysis/src` to Python path |
| `test_connection.py` | Standalone SQL Server connectivity test |
| `quick_load.py` | Loads DenialIQ CSV into SQL Server via pyodbc |
| `inspect_denialiq.py` | Prints CSV columns / dtypes / samples |
| `README.md` | This document |

---

## 8. Database Schema

Six tables in the `hospital_claims` database.

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `patients` | Synthetic patient registry | `patient_id`, `patient_name`, `age`, `gender`, `city` |
| `insurance_companies` | Insurers the hospital works with | `company_id`, `company_name`, `contact` |
| `departments` | Hospital departments | `dept_id`, `dept_name` |
| `claims` | Core claim fact table | `claim_id`, `patient_id`, `company_id`, `dept_id`, `claim_type`, `claimed_amount`, `approved_amount`, `paid_amount`, `status`, `submission_date`, `decision_date`, `rejection_reason` |
| `claims_denialiq` | DenialIQ staging table (25 cols, all VARCHAR) | mirrors `claims_main.csv` |
| `claim_status_history` | Status transitions per claim | `history_id`, `claim_id`, `status`, `changed_date` |

### Relationships
```
patients ─┐
          │
companies ┼──► claims ──► claim_status_history
          │
departments ┘
```

### Status Values
`SUBMITTED` · `APPROVED` · `DENIED` · `PENDING` · `SETTLED`

### Normalised View (`vw_claims`)
Maps the DenialIQ staging table to the project schema and derives:
- `approved_amount` and `paid_amount` from `outcome` × `claim_amount_usd`
- `decision_date` = submission + 30 days (simulated)
- `status` normalised from raw `outcome`

---

## 9. KPI Definitions

| KPI | Formula |
|-----|---------|
| **Total Claims** | `COUNT(all claims)` |
| **Decided Claims** | `APPROVED + DENIED + SETTLED` |
| **Approval Rate** | `Approved / Decided × 100` |
| **Denial Rate** | `Denied / Decided × 100` |
| **Processing Time** | `decision_date − submission_date` (days) |
| **Delayed Claim** | `Processing Days > 30` |
| **Claim → Approval Gap** | `claimed_amount − approved_amount` |
| **Approval → Payment Gap** | `approved_amount − paid_amount` |

### Financial Terms
| Term | Meaning |
|------|---------|
| Claimed Amount | Amount billed to the insurance company |
| Approved Amount | Amount accepted by the insurance company |
| Paid Amount | Amount actually received by the hospital |

---

## 10. Setup Guide

### 10.1 Prerequisites
- Windows 10/11
- Python 3.11+
- Microsoft SQL Server (Express or full)
- SSMS (SQL Server Management Studio)
- ODBC Driver 17 for SQL Server

### 10.2 Install Dependencies
```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

### 10.3 Create the Database
Open SSMS → connect to your instance → open `02_Database/database.sql` → **Execute**.

For DenialIQ data:
```
02_Database/database_denialiq.sql  → Execute (creates staging + view)
02_Database/load_denialiq.sql      → Execute (bulk-inserts CSV)
```

Or use the Python loader:
```bash
python quick_load.py
```

### 10.4 Configure Environment
```bash
copy .env.example .env
```
Edit `.env` with your SQL Server details.

### 10.5 Verify the Connection
```bash
python test_connection.py
```
Expected:
```
✅ Connected. Claims rows: 15
```

---

## 11. Windows Authentication Setup

Recommended for local development.

**`.env`**
```env
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=hospital_claims
DB_USER=
DB_PASSWORD=
DB_TRUSTED_CONNECTION=yes
PROCESSING_THRESHOLD_DAYS=30
CSV_PATH=data/claims_main.csv
```

**Requirements**
1. In SSMS → Server Properties → Security → **Windows Authentication mode** enabled.
2. Your Windows account (`whoami`) added under **Security → Logins**.
3. Grant access to the database:
   ```sql
   USE hospital_claims;
   CREATE USER [DESKTOP-93N7UMR\admin] FOR LOGIN [DESKTOP-93N7UMR\admin];
   ALTER ROLE db_owner ADD MEMBER [DESKTOP-93N7UMR\admin];
   ```

---

## 12. Running the Project

### 12.1 Run the Notebook
```bash
cd 03_Python_Analysis
jupyter notebook
```
Open `claims_analysis.ipynb` → **Cell → Run All**.

### 12.2 Run the Streamlit App
From project root:
```bash
streamlit run 04_Streamlit/app.py
```
Browser opens at **http://localhost:8501**.

### 12.3 Stop the App
Press **Ctrl + C** in the terminal.

---

## 13. Running Tests

```bash
pytest 05_Testing/ -v
```

**Expected output:**
```
========================== 37 passed in 0.6s ==========================
```

### Test categories
| Class | Tests |
|-------|-------|
| `TestVolume` | 4 |
| `TestRates` | 3 |
| `TestRejections` | 2 |
| `TestProcessingTime` | 3 |
| `TestDelayed` | 2 |
| `TestFinancial` | 3 |
| `TestComparisons` | 3 |
| `TestLookup` | 2 |
| `TestValidation` | 4 |
| `TestEmptySafety` | 4 |
| `TestCSVLoader` | 7 |
| **Total** | **37** |

Useful flags:
```bash
pytest 05_Testing/ -q                # quiet
pytest 05_Testing/ -k Volume         # only Volume tests
pytest 05_Testing/ --maxfail=1       # stop on first failure
```

---

## 14. Logging

Log file location:
```
06_Logs/application.log
```

**Format**
```
YYYY-MM-DD HH:MM:SS | LEVEL | module | message
```

**What is logged**
- Database load events (row counts, connection status)
- KPI calculation events (financial totals, comparison runs)
- Streamlit filter changes
- Individual claim lookups
- Validation summary reports
- All unexpected errors

**Example**
```
2026-01-15 10:12:03 | INFO | src.database | Loaded 120000 claims from SQL Server
2026-01-15 10:12:03 | INFO | src.kpi_calculation | ClaimsKPI initialised | rows=120000 | threshold=30 days
2026-01-15 10:12:03 | INFO | src.kpi_calculation | Financial summary | claimed=... approved=... paid=...
```

---

## 15. Screens & Tabs

| Tab | Contents |
|-----|----------|
| **📊 Overview** | KPI cards · status bar+pie · rejection table · delayed claims · financial summary |
| **🏢 Companies** | Comparison table · denial-rate bar chart |
| **🏥 Departments** | Comparison table · claim volume chart |
| **🔎 Investigation** | Claim ID selector → full claim row |

Sidebar filters: date range, insurance company, department, status, claim type.

**Full user guide:** See `04_Streamlit/README_STREAMLIT.md`.

---

## 16. Demo Script

| Step | Action | Message |
|------|--------|---------|
| 1 | Open Streamlit | "This is the Claims Analytics dashboard for MediCare Hospital." |
| 2 | Point to KPI cards | "Total claims, approval rate, denial rate, average processing days." |
| 3 | Status charts | "Distribution of claims across statuses." |
| 4 | Rejection table | "Top reasons for denials." |
| 5 | Delayed table | "Claims older than 30 days flagged for follow-up." |
| 6 | Financial summary | "Claimed, approved, paid + both gaps." |
| 7 | Sidebar filter → a payer | "Filters let us drill into any insurer." |
| 8 | Companies tab | "Compare insurers on denial rate and time." |
| 9 | Departments tab | "Same view by department." |
| 10 | Investigation → a claim | "Drill into any claim." |
| 11 | Open `application.log` | "Every action logged for audit." |
| 12 | Run pytest | "37 tests all passing." |

---

## 17. Security Notes

| ✅ Do | ❌ Don't |
|-------|----------|
| Keep credentials in `.env` | Commit `.env` to git |
| Use Windows Authentication | Hardcode passwords in code |
| Use synthetic data only | Use real patient records |
| Share only `.env.example` | Share real database dumps |
| Keep `.gitignore` intact | Disable it |

---

##  Your Deployment Architecture
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Local Dev   │────▶│   GitHub     │────▶│    EC2       │
│  Windows     │     │   Repo       │     │  (Ubuntu)    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                       ┌──────────────┐          │ docker pull
                       │     ECR      │◀─────────┘
                       │ (Docker img) │
                       └──────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │ Streamlit    │
                                          │ :8501 → :80  │
                                          │ Public URL   │
                                          └──────────────┘
```

### Flow:

* Write code locally → push to GitHub

* Build Docker image → push to ECR

* EC2 pulls image from ECR → runs container

* Public IP exposes the dashboard

-----

## 18. Future Enhancements

- 📄 PDF export of dashboards
- 📧 Email alerts for delayed claims
- 🤖 ML model to predict denial likelihood (using `train_test_split.csv` and `denial_labels.csv`)
- 📊 Power BI integration
- 🔄 Real-time refresh from claims system
- 👥 User login with role-based access
- 📅 Month-over-month trend analysis
- ☁️ Cloud migration (Azure SQL + Data Factory)
- 🐳 Docker + CI/CD pipeline

---

## 19. Author

**Project:** Hospital Insurance Claims & Revenue Analytics
**Built for:** MediCare Multi-Specialty Hospital (fictional)
**Dataset:** DenialIQ (Kaggle, 120K synthetic medical claims)

# Mr.RaviVarma
---

> **Note:** All patient and insurance data in this project is **100% synthetic**.
> No real patient information, medical records, or insurance transactions
> are used anywhere in the system.