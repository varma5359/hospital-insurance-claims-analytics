"""
csv_loader.py
-------------
Loads the DenialIQ claims CSV (25 columns) and normalises it
to the schema expected by ClaimsKPI.

DenialIQ does not provide approved_amount, paid_amount, or
decision_date directly — these are derived from `outcome`
and `claim_amount_usd`.
"""

import os
from typing import Dict

import numpy as np
import pandas as pd

from .logger import get_logger

logger = get_logger(__name__)


class DenialIQLoader:
    """Loads DenialIQ CSV into a ClaimsKPI-compatible dataframe."""

    # DenialIQ → project column name
    RENAME_MAP: Dict[str, str] = {
        "claim_id":              "claim_id",
        "claim_submission_date": "submission_date",
        "payer_type":            "company_name",
        "provider_specialty":    "dept_name",
        "place_of_service_desc": "claim_type",
        "claim_amount_usd":      "claimed_amount",
        "outcome":               "status",
        "denial_reason_code":    "rejection_reason",
    }

    # Outcome → project status
    STATUS_MAP = {
        "PAID":        "SETTLED",
        "SETTLED":     "SETTLED",
        "APPROVED":    "APPROVED",
        "PARTIAL_PAY": "APPROVED",
        "PARTIAL":     "APPROVED",
        "DENIED":      "DENIED",
        "REJECTED":    "DENIED",
        "PENDING":     "PENDING",
    }

    # Outcome → recovery ratios (approved/paid as fraction of claimed)
    RECOVERY_RATIO = {
        "SETTLED":  (1.00, 1.00),
        "APPROVED": (0.70, 0.60),   # partial_pay
        "DENIED":   (0.00, 0.00),
        "PENDING":  (0.00, 0.00),
    }

    def __init__(self, csv_path: str) -> None:
        """Store the CSV path."""
        self.csv_path = csv_path

    def load(self) -> pd.DataFrame:
        """Return a normalised, ClaimsKPI-ready dataframe."""
        if not os.path.exists(self.csv_path):
            logger.error("CSV not found: %s", self.csv_path)
            return pd.DataFrame()

        logger.info("Loading CSV: %s", self.csv_path)
        df = pd.read_csv(self.csv_path, low_memory=False)
        logger.info("Raw CSV: %d rows × %d cols", *df.shape)

        df = self._select_and_rename(df)
        df = self._normalise_status(df)
        df = self._derive_financials(df)
        df = self._derive_dates(df)
        df = self._fill_defaults(df)

        logger.info("Normalised CSV: %d rows × %d cols", *df.shape)
        return df

    # ---------------- helpers ----------------
    def _select_and_rename(self, df: pd.DataFrame) -> pd.DataFrame:
        """Keep only mapped columns and rename them."""
        df.columns = [c.strip().lower() for c in df.columns]

        keep = {k: v for k, v in self.RENAME_MAP.items() if k in df.columns}
        if not keep:
            logger.warning("No columns matched — returning raw")
            return df

        out = df[list(keep.keys())].rename(columns=keep)
        logger.info("Mapped columns: %s", list(out.columns))
        return out

    def _normalise_status(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map outcome strings to the 5 project statuses."""
        if "status" not in df.columns:
            df["status"] = "PENDING"
            return df

        df["status"] = (
            df["status"]
            .astype(str).str.strip().str.upper()
            .map(self.STATUS_MAP)
            .fillna("PENDING")
        )
        return df

    def _derive_financials(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute approved_amount and paid_amount from claimed_amount × ratio."""
        if "claimed_amount" not in df.columns:
            df["claimed_amount"] = 0.0
        df["claimed_amount"] = pd.to_numeric(
            df["claimed_amount"], errors="coerce"
        ).fillna(0.0)

        approved = []
        paid = []
        for status, claimed in zip(df["status"], df["claimed_amount"]):
            a_ratio, p_ratio = self.RECOVERY_RATIO.get(status, (0.0, 0.0))
            approved.append(round(float(claimed) * a_ratio, 2))
            paid.append(round(float(claimed) * p_ratio, 2))

        df["approved_amount"] = approved
        df["paid_amount"] = paid
        return df

    def _derive_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse submission_date and simulate decision_date."""
        if "submission_date" in df.columns:
            df["submission_date"] = pd.to_datetime(
                df["submission_date"], errors="coerce"
            )
        else:
            df["submission_date"] = pd.NaT

        # Decision date = submission + pseudo-random 15–45 days
        # Only for decided claims (not PENDING)
        rng = np.random.default_rng(seed=42)  # reproducible
        offsets = rng.integers(15, 46, size=len(df))
        decisions = df["submission_date"] + pd.to_timedelta(offsets, unit="D")

        # PENDING claims have no decision_date
        decisions = decisions.where(df["status"] != "PENDING", pd.NaT)
        df["decision_date"] = decisions
        return df

    def _fill_defaults(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure required columns exist."""
        defaults = {
            "claim_id":         None,
            "patient_id":       None,
            "patient_name":     None,
            "company_id":       None,
            "company_name":     "Unknown",
            "dept_id":          None,
            "dept_name":        "Unknown",
            "claim_type":       "UNKNOWN",
            "claimed_amount":   0.0,
            "approved_amount":  0.0,
            "paid_amount":      0.0,
            "status":           "PENDING",
            "submission_date":  pd.NaT,
            "decision_date":    pd.NaT,
            "rejection_reason": None,
        }
        for col, default in defaults.items():
            if col not in df.columns:
                df[col] = default
        return df