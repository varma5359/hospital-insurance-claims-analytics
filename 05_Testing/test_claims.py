"""
test_claims.py
--------------
Unit tests for the claims KPI and validation modules.

Covers:
    - total claims
    - claims by status
    - approval rate
    - denial rate
    - rejection reasons
    - processing time
    - delayed claims
    - financial summary + gaps
    - company comparison
    - department analysis
    - claim lookup
    - data validation
    - empty dataframe safety
"""

import pandas as pd
import pytest

from kpi_calculation import ClaimsKPI
from data_validation import DataValidator


# =========================================================
# Volume
# =========================================================
class TestVolume:
    """Tests for claim volume KPIs."""

    def test_total_claims(self, sample_df):
        """Total claims should equal row count."""
        assert ClaimsKPI(sample_df).total_claims() == 5

    def test_claims_by_status_columns(self, sample_df):
        """Result must have status, count, percentage columns."""
        out = ClaimsKPI(sample_df).claims_by_status()
        assert list(out.columns) == ["status", "count", "percentage"]

    def test_claims_by_status_counts(self, sample_df):
        """APPROVED should be 2, DENIED 1, PENDING 1, SETTLED 1."""
        out = ClaimsKPI(sample_df).claims_by_status()
        m = dict(zip(out["status"], out["count"]))
        assert m["APPROVED"] == 2
        assert m["DENIED"]   == 1
        assert m["PENDING"]  == 1
        assert m["SETTLED"]  == 1

    def test_claims_by_status_percentage_total(self, sample_df):
        """Percentages must sum to ~100."""
        out = ClaimsKPI(sample_df).claims_by_status()
        assert abs(out["percentage"].sum() - 100) < 0.1


# =========================================================
# Rates
# =========================================================
class TestRates:
    """Tests for approval and denial rates."""

    def test_approval_rate(self, sample_df):
        """
        Approved = 3 (2 APPROVED + 1 SETTLED)
        Decided  = 4 (3 approved-ish + 1 denied)
        Rate     = 75.0
        """
        assert ClaimsKPI(sample_df).approval_rate() == 75.0

    def test_denial_rate(self, sample_df):
        """Denied / Decided * 100 = 1/4 * 100 = 25.0."""
        assert ClaimsKPI(sample_df).denial_rate() == 25.0

    def test_rates_sum_to_100(self, sample_df):
        """Approval + Denial must be 100 for decided claims."""
        kpi = ClaimsKPI(sample_df)
        assert round(kpi.approval_rate() + kpi.denial_rate(), 2) == 100.0


# =========================================================
# Rejections
# =========================================================
class TestRejections:
    """Tests for rejection reason analysis."""

    def test_rejection_reasons_count(self, sample_df):
        """Only denied claims should be counted."""
        out = ClaimsKPI(sample_df).rejection_reasons()
        assert out["count"].sum() == 1

    def test_rejection_reason_value(self, sample_df):
        """The single reason should match input."""
        out = ClaimsKPI(sample_df).rejection_reasons()
        assert out.iloc[0]["rejection_reason"] == "Pre-authorization missing"


# =========================================================
# Processing time
# =========================================================
class TestProcessingTime:
    """Tests for processing-time KPIs."""

    def test_processing_days_column(self, sample_df):
        """processing_days column should exist and be numeric."""
        kpi = ClaimsKPI(sample_df)
        assert "processing_days" in kpi.df.columns
        assert kpi.df["processing_days"].dtype.kind in "if"

    def test_processing_days_value(self, sample_df):
        """Claim 1: 2025-01-05 → 2025-01-20 = 15 days."""
        kpi = ClaimsKPI(sample_df)
        row = kpi.df[kpi.df["claim_id"] == 1].iloc[0]
        assert row["processing_days"] == 15

    def test_avg_processing_time(self, sample_df):
        """Average of decided claims should be a positive number."""
        avg = ClaimsKPI(sample_df).avg_processing_time()
        assert avg > 0


# =========================================================
# Delayed
# =========================================================
class TestDelayed:
    """Tests for delayed-claim flagging."""

    def test_delayed_claims_threshold_30(self, sample_df):
        """
        Claim 3: 41 days (>30) → delayed
        Claim 5: 44 days (>30) → delayed
        Claim 1: 15 days      → not delayed
        So exactly 2 delayed claims.
        """
        out = ClaimsKPI(sample_df, threshold_days=30).delayed_claims()
        assert len(out) == 2

    def test_delayed_claims_threshold_high(self, sample_df):
        """Very high threshold → no delayed claims."""
        out = ClaimsKPI(sample_df, threshold_days=9999).delayed_claims()
        assert len(out) == 0


# =========================================================
# Financial
# =========================================================
class TestFinancial:
    """Tests for financial summary and gaps."""

    def test_financial_totals(self, sample_df):
        """Sum of claimed / approved / paid must match."""
        fin = ClaimsKPI(sample_df).financial_summary()
        assert fin["total_claimed"]  == 120000 + 25000 + 200000 + 40000 + 60000
        assert fin["total_approved"] == 100000 + 20000 + 0 + 0 + 55000
        assert fin["total_paid"]     == 100000 + 20000 + 0 + 0 + 50000

    def test_claim_to_approval_gap(self, sample_df):
        """Claimed - Approved should match formula."""
        fin = ClaimsKPI(sample_df).financial_summary()
        assert fin["claim_to_approval_gap"] == (
            fin["total_claimed"] - fin["total_approved"]
        )

    def test_approval_to_payment_gap(self, sample_df):
        """Approved - Paid should match formula."""
        fin = ClaimsKPI(sample_df).financial_summary()
        assert fin["approval_to_payment_gap"] == (
            fin["total_approved"] - fin["total_paid"]
        )


# =========================================================
# Comparisons
# =========================================================
class TestComparisons:
    """Tests for company and department comparison."""

    def test_company_comparison_shape(self, sample_df):
        """One row per company."""
        out = ClaimsKPI(sample_df).company_comparison()
        assert len(out) == 4          # Star, HDFC, ICICI, Niva

    def test_company_comparison_columns(self, sample_df):
        """Required columns present."""
        out = ClaimsKPI(sample_df).company_comparison()
        for col in ["company_name", "total_claims",
                    "approval_rate", "denial_rate", "avg_processing_days"]:
            assert col in out.columns

    def test_department_analysis_shape(self, sample_df):
        """One row per department."""
        out = ClaimsKPI(sample_df).department_analysis()
        assert len(out) == 4          # Cardiology, Orthopedics, Neurology, Gen Surgery


# =========================================================
# Lookup
# =========================================================
class TestLookup:
    """Tests for single-claim investigation."""

    def test_claim_lookup_found(self, sample_df):
        """Existing claim should return 1 row."""
        out = ClaimsKPI(sample_df).claim_lookup(1)
        assert len(out) == 1

    def test_claim_lookup_not_found(self, sample_df):
        """Unknown claim id should return empty."""
        out = ClaimsKPI(sample_df).claim_lookup(9999)
        assert out.empty


# =========================================================
# Validation
# =========================================================
class TestValidation:
    """Tests for the DataValidator module."""

    def test_no_missing_columns(self, sample_df):
        """Sample data should have all required columns."""
        report = DataValidator(sample_df).run_all()
        assert report["missing_columns"] == []

    def test_invalid_date_order_detected(self, sample_df):
        """Inject a bad date and confirm detection."""
        bad = sample_df.copy()
        bad.loc[0, "decision_date"] = "2024-01-01"   # before submission
        report = DataValidator(bad).run_all()
        assert report["date_order_issues"] >= 1

    def test_negative_amount_detected(self, sample_df):
        """Inject negative amount and confirm detection."""
        bad = sample_df.copy()
        bad.loc[0, "claimed_amount"] = -5000
        report = DataValidator(bad).run_all()
        assert report["negative_amount_rows"] >= 1

    def test_invalid_status_detected(self, sample_df):
        """Unknown status must be flagged."""
        bad = sample_df.copy()
        bad.loc[0, "status"] = "UNKNOWN"
        report = DataValidator(bad).run_all()
        assert report["invalid_status_rows"] >= 1


# =========================================================
# Empty dataframe safety
# =========================================================
class TestEmptySafety:
    """Tests that modules handle empty dataframes gracefully."""

    def test_total_claims_empty(self, empty_df):
        assert ClaimsKPI(empty_df).total_claims() == 0

    def test_rates_empty(self, empty_df):
        kpi = ClaimsKPI(empty_df)
        assert kpi.approval_rate() == 0.0
        assert kpi.denial_rate()   == 0.0

    def test_financial_empty(self, empty_df):
        fin = ClaimsKPI(empty_df).financial_summary()
        assert fin["total_claimed"] == 0

    def test_rejection_empty(self, empty_df):
        out = ClaimsKPI(empty_df).rejection_reasons()
        assert out.empty