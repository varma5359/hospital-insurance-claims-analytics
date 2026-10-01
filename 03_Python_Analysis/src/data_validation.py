"""
data_validation.py
------------------
Validates raw claims data before KPI calculation.

Primary class : DataValidator
Wrapper       : validate_all(df)
"""

import logging
from typing import Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


class DataValidator:
    """Checks required columns, nulls, amounts, dates and statuses."""

    REQUIRED_COLS: List[str] = [
        "claim_id",
        "claimed_amount",
        "approved_amount",
        "paid_amount",
        "status",
        "submission_date",
        "decision_date",
    ]

    VALID_STATUSES = {"SUBMITTED", "APPROVED", "DENIED", "PENDING", "SETTLED"}

    def __init__(self, df: pd.DataFrame) -> None:
        """Store the dataframe to validate."""
        self.df = df

    # ---------------- individual checks ----------------
    def missing_columns(self) -> List[str]:
        """Return required columns that are missing."""
        return [c for c in self.REQUIRED_COLS if c not in self.df.columns]

    def null_counts(self) -> Dict[str, int]:
        """Return null counts (only for columns with nulls)."""
        out: Dict[str, int] = {}
        for col in self.REQUIRED_COLS:
            if col in self.df.columns:
                n = int(self.df[col].isna().sum())
                if n > 0:
                    out[col] = n
        return out

    def negative_amount_rows(self) -> pd.DataFrame:
        """Return rows having any negative monetary amount."""
        mask = pd.Series(False, index=self.df.index)
        for col in ["claimed_amount", "approved_amount", "paid_amount"]:
            if col in self.df.columns:
                mask |= self.df[col] < 0
        return self.df[mask]

    def invalid_date_order_rows(self) -> pd.DataFrame:
        """Return rows where decision_date is before submission_date."""
        if "submission_date" not in self.df or "decision_date" not in self.df:
            return pd.DataFrame()
        sub = pd.to_datetime(self.df["submission_date"], errors="coerce")
        dec = pd.to_datetime(self.df["decision_date"], errors="coerce")
        return self.df[dec.notna() & sub.notna() & (dec < sub)]

    def invalid_status_rows(self) -> pd.DataFrame:
        """Return rows having a status outside the allowed set."""
        if "status" not in self.df.columns:
            return pd.DataFrame()
        return self.df[~self.df["status"].isin(self.VALID_STATUSES)]

    # ---------------- aggregate ----------------
    def run_all(self) -> Dict:
        """Run all validations and return a summary dictionary."""
        report = {
            "row_count": len(self.df),
            "missing_columns": self.missing_columns(),
            "nulls": self.null_counts(),
            "negative_amount_rows": len(self.negative_amount_rows()),
            "date_order_issues": len(self.invalid_date_order_rows()),
            "invalid_status_rows": len(self.invalid_status_rows()),
        }
        logger.info("Validation report: %s", report)
        return report


def validate_all(df: pd.DataFrame) -> Dict:
    """Wrapper: validate_all(df) -> report dict."""
    return DataValidator(df).run_all()