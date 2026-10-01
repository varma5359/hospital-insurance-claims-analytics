"""
conftest.py
-----------
Shared pytest fixtures for the claims test suite.

Provides a small synthetic claims dataframe so tests run
without needing the SQL Server connection.
"""

import os
import sys

import pandas as pd
import pytest

# Make src importable from tests
ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "03_Python_Analysis", "src")
sys.path.append(SRC)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Small synthetic claims dataset covering all statuses.

    Returns:
        pd.DataFrame with columns used by ClaimsKPI.
    """
    return pd.DataFrame([
        # claim, company, dept, claimed, approved, paid, status, sub, dec, reason
        {"claim_id": 1, "company_name": "Star Health",   "dept_name": "Cardiology",
         "claimed_amount": 120000, "approved_amount": 100000, "paid_amount": 100000,
         "status": "SETTLED", "submission_date": "2025-01-05",
         "decision_date": "2025-01-20", "rejection_reason": None},

        {"claim_id": 2, "company_name": "HDFC Ergo",     "dept_name": "Orthopedics",
         "claimed_amount": 25000,  "approved_amount": 20000,  "paid_amount": 20000,
         "status": "APPROVED", "submission_date": "2025-01-08",
         "decision_date": "2025-01-18", "rejection_reason": None},

        {"claim_id": 3, "company_name": "ICICI Lombard", "dept_name": "Neurology",
         "claimed_amount": 200000, "approved_amount": 0,      "paid_amount": 0,
         "status": "DENIED", "submission_date": "2025-01-10",
         "decision_date": "2025-02-20",
         "rejection_reason": "Pre-authorization missing"},

        {"claim_id": 4, "company_name": "Niva Bupa",     "dept_name": "General Surgery",
         "claimed_amount": 40000,  "approved_amount": 0,      "paid_amount": 0,
         "status": "PENDING", "submission_date": "2025-01-15",
         "decision_date": None, "rejection_reason": None},

        {"claim_id": 5, "company_name": "Star Health",   "dept_name": "Cardiology",
         "claimed_amount": 60000,  "approved_amount": 55000,  "paid_amount": 50000,
         "status": "APPROVED", "submission_date": "2025-01-20",
         "decision_date": "2025-03-05", "rejection_reason": None},
    ])


@pytest.fixture
def empty_df() -> pd.DataFrame:
    """Empty dataframe with required columns — tests graceful behavior."""
    cols = ["claim_id", "company_name", "dept_name",
            "claimed_amount", "approved_amount", "paid_amount",
            "status", "submission_date", "decision_date", "rejection_reason"]
    return pd.DataFrame(columns=cols)