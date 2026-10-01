"""
kpi_calculation.py
------------------
All business KPIs for insurance claims analytics.

Primary class : ClaimsKPI
Wrappers      : total_claims, approval_rate, denial_rate, ...

Business rules implemented:
    - Decided claims = APPROVED + DENIED + SETTLED
    - Approval Rate  = Approved / Decided × 100
    - Denial Rate    = Denied   / Decided × 100
    - Processing Days = decision_date - submission_date
    - Delayed claim  = Processing Days > threshold (default 30)
    - Claim → Approval Gap   = claimed - approved
    - Approval → Payment Gap = approved - paid

Status normalisation:
    Handles multiple raw status labels (from SQL Server, DenialIQ
    CSV, or synthetic sample) and maps them to the 5 canonical
    project statuses: SUBMITTED, APPROVED, DENIED, PENDING, SETTLED.
"""

from typing import Dict, List

import pandas as pd

from .logger import get_logger

logger = get_logger(__name__)

DECIDED_STATUSES  = {"APPROVED", "DENIED", "SETTLED"}
APPROVED_STATUSES = {"APPROVED", "SETTLED"}
DENIED_STATUSES   = {"DENIED"}
DEFAULT_THRESHOLD_DAYS = 30


class ClaimsKPI:
    """Calculates all volume, rate, rejection, time and money KPIs."""

    # -----------------------------------------------------------
    # Status normalisation: raw label → canonical project status
    # -----------------------------------------------------------
    STATUS_MAP: Dict[str, str] = {
        "PAID":            "SETTLED",
        "SETTLED":         "SETTLED",
        "APPROVED":        "APPROVED",
        "PARTIALLY PAID":  "APPROVED",
        "PARTIAL":         "APPROVED",
        "PARTIAL_PAY":     "APPROVED",
        "PARTIAL PAYMENT": "APPROVED",
        "DENIED":          "DENIED",
        "REJECTED":        "DENIED",
        "PENDING":         "PENDING",
        "IN REVIEW":       "PENDING",
        "UNDER REVIEW":    "PENDING",
        "SUBMITTED":       "SUBMITTED",
        "PROCESSING":      "PENDING",
    }

    # -----------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------
    def __init__(
        self,
        df: pd.DataFrame,
        threshold_days: int = DEFAULT_THRESHOLD_DAYS,
    ) -> None:
        """
        Args:
            df: Claims dataframe (from database.load_claims()).
            threshold_days: Days above which a claim is delayed.
        """
        self.df = df.copy()
        self.threshold_days = threshold_days

        # Normalise status values so KPI math stays consistent
        if "status" in self.df.columns:
            self.df["status"] = (
                self.df["status"]
                .astype(str)
                .str.strip()
                .str.upper()
                .map(self.STATUS_MAP)
                .fillna("PENDING")
            )

        self._add_processing_days()

        logger.info(
            "ClaimsKPI initialised | rows=%d | threshold=%d days",
            len(self.df), self.threshold_days,
        )

    # -----------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------
    def _add_processing_days(self) -> None:
        """Add `processing_days` = decision_date − submission_date."""
        sub = pd.to_datetime(self.df.get("submission_date"), errors="coerce")
        dec = pd.to_datetime(self.df.get("decision_date"), errors="coerce")
        self.df["processing_days"] = (dec - sub).dt.days

    def _decided(self) -> pd.DataFrame:
        """Rows with a final outcome (approved / denied / settled)."""
        return self.df[self.df["status"].isin(DECIDED_STATUSES)]

    # -----------------------------------------------------------
    # Volume
    # -----------------------------------------------------------
    def total_claims(self) -> int:
        """Total number of claims."""
        return int(len(self.df))

    def claims_by_status(self) -> pd.DataFrame:
        """Return count and percentage of claims by status."""
        if self.df.empty:
            return pd.DataFrame(columns=["status", "count", "percentage"])
        out = self.df.groupby("status").size().reset_index(name="count")
        out["percentage"] = (out["count"] / out["count"].sum() * 100).round(2)
        return out.sort_values("count", ascending=False).reset_index(drop=True)

    # -----------------------------------------------------------
    # Rates
    # -----------------------------------------------------------
    def approval_rate(self) -> float:
        """Approval Rate = Approved / Decided × 100."""
        decided = self._decided()
        if decided.empty:
            return 0.0
        approved = decided["status"].isin(APPROVED_STATUSES).sum()
        return round(approved / len(decided) * 100, 2)

    def denial_rate(self) -> float:
        """Denial Rate = Denied / Decided × 100."""
        decided = self._decided()
        if decided.empty:
            return 0.0
        denied = decided["status"].isin(DENIED_STATUSES).sum()
        return round(denied / len(decided) * 100, 2)

    # -----------------------------------------------------------
    # Rejections
    # -----------------------------------------------------------
    def rejection_reasons(self) -> pd.DataFrame:
        """Return denial reasons with their claim counts."""
        denied = self.df[self.df["status"].isin(DENIED_STATUSES)]
        if denied.empty:
            return pd.DataFrame(columns=["rejection_reason", "count"])
        out = (
            denied["rejection_reason"]
            .fillna("Not Specified")
            .value_counts()
            .reset_index()
        )
        out.columns = ["rejection_reason", "count"]
        return out

    # -----------------------------------------------------------
    # Processing time
    # -----------------------------------------------------------
    def avg_processing_time(self) -> float:
        """Average processing days across decided claims."""
        valid = self.df["processing_days"].dropna()
        return round(valid.mean(), 1) if not valid.empty else 0.0

    def delayed_claims(self, threshold: int | None = None) -> pd.DataFrame:
        """Return decided claims whose processing days exceed the threshold."""
        limit = threshold if threshold is not None else self.threshold_days
        decided = self._decided()
        return decided[decided["processing_days"] > limit]

    # -----------------------------------------------------------
    # Financial
    # -----------------------------------------------------------
    def financial_summary(self) -> Dict[str, float]:
        """Return totals and gaps across claimed / approved / paid."""
        claimed  = float(self.df["claimed_amount"].fillna(0).sum())
        approved = float(self.df["approved_amount"].fillna(0).sum())
        paid     = float(self.df["paid_amount"].fillna(0).sum())

        logger.info(
            "Financial summary | claimed=%.2f approved=%.2f paid=%.2f",
            claimed, approved, paid,
        )

        return {
            "total_claimed":  round(claimed, 2),
            "total_approved": round(approved, 2),
            "total_paid":     round(paid, 2),
            "claim_to_approval_gap":   round(claimed - approved, 2),
            "approval_to_payment_gap": round(approved - paid, 2),
        }

    # -----------------------------------------------------------
    # Comparisons
    # -----------------------------------------------------------
    def company_comparison(self) -> pd.DataFrame:
        """Compare insurance companies on volume, rates, time and money."""
        if self.df.empty:
            return pd.DataFrame()
        rows: List[Dict] = []
        for name, group in self.df.groupby("company_name"):
            kpi = ClaimsKPI(group, self.threshold_days)
            decided = group[group["status"].isin(DECIDED_STATUSES)]
            rows.append({
                "company_name": name,
                "total_claims": len(group),
                "approved": int(decided["status"].isin(APPROVED_STATUSES).sum()),
                "denied":   int(decided["status"].isin(DENIED_STATUSES).sum()),
                "approval_rate": kpi.approval_rate(),
                "denial_rate":   kpi.denial_rate(),
                "avg_processing_days": kpi.avg_processing_time(),
                "total_claimed": round(group["claimed_amount"].fillna(0).sum(), 2),
                "total_paid":    round(group["paid_amount"].fillna(0).sum(), 2),
            })
        logger.info("Company comparison generated for %d companies", len(rows))
        return pd.DataFrame(rows).sort_values("total_claims", ascending=False)

    def department_analysis(self) -> pd.DataFrame:
        """Compare hospital departments on volume, denials and time."""
        if self.df.empty:
            return pd.DataFrame()
        rows: List[Dict] = []
        for name, group in self.df.groupby("dept_name"):
            kpi = ClaimsKPI(group, self.threshold_days)
            decided = group[group["status"].isin(DECIDED_STATUSES)]
            rows.append({
                "dept_name": name,
                "total_claims": len(group),
                "denied": int(decided["status"].isin(DENIED_STATUSES).sum()),
                "denial_rate": kpi.denial_rate(),
                "avg_processing_days": kpi.avg_processing_time(),
                "total_claimed": round(group["claimed_amount"].fillna(0).sum(), 2),
            })
        logger.info("Department analysis generated for %d departments", len(rows))
        return pd.DataFrame(rows).sort_values("total_claims", ascending=False)

    # -----------------------------------------------------------
    # Lookup
    # -----------------------------------------------------------
    def claim_lookup(self, claim_id) -> pd.DataFrame:
        """Return a single claim's full row for investigation."""
        logger.info("Claim lookup requested for id=%s", claim_id)
        return self.df[self.df["claim_id"] == claim_id]


# =========================================================
# Functional wrappers (notebook / tests)
# =========================================================
def total_claims(df: pd.DataFrame) -> int:
    """Return total number of claims."""
    return ClaimsKPI(df).total_claims()


def claims_by_status(df: pd.DataFrame) -> pd.DataFrame:
    """Return claims grouped by status."""
    return ClaimsKPI(df).claims_by_status()


def approval_rate(df: pd.DataFrame) -> float:
    """Return approval rate."""
    return ClaimsKPI(df).approval_rate()


def denial_rate(df: pd.DataFrame) -> float:
    """Return denial rate."""
    return ClaimsKPI(df).denial_rate()


def rejection_reasons(df: pd.DataFrame) -> pd.DataFrame:
    """Return rejection reasons with counts."""
    return ClaimsKPI(df).rejection_reasons()


def avg_processing_time(df: pd.DataFrame) -> float:
    """Return average processing time in days."""
    return ClaimsKPI(df).avg_processing_time()


def delayed_claims(df: pd.DataFrame, threshold: int = 30) -> pd.DataFrame:
    """Return claims exceeding the processing-time threshold."""
    return ClaimsKPI(df, threshold).delayed_claims()


def financial_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Return claimed / approved / paid totals and gaps."""
    return ClaimsKPI(df).financial_summary()


def company_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Return insurance company comparison table."""
    return ClaimsKPI(df).company_comparison()


def department_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Return department comparison table."""
    return ClaimsKPI(df).department_analysis()


def add_processing_days(df: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe with processing_days column added."""
    return ClaimsKPI(df).df