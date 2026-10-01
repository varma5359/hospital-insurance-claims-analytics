"""
database.py
-----------
Loads claims data. Order of preference:

    1. SQL Server (normalised view `vw_claims`)
    2. DenialIQ CSV (data/claims_main.csv)
    3. Tiny built-in sample

Uses Windows Authentication when DB_TRUSTED_CONNECTION=yes.
"""

import os

import pandas as pd
import pyodbc
from dotenv import load_dotenv

from .logger import get_logger
from .csv_loader import DenialIQLoader

load_dotenv()
logger = get_logger(__name__)


class DatabaseLoader:
    """Loads claims from SQL Server or falls back to CSV."""

    def __init__(self) -> None:
        """Read connection and CSV path from environment."""
        self.driver   = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        self.server   = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
        self.database = os.getenv("DB_NAME", "hospital_claims")
        self.user     = os.getenv("DB_USER", "")
        self.password = os.getenv("DB_PASSWORD", "")
        self.trusted  = os.getenv("DB_TRUSTED_CONNECTION", "no").lower() == "yes"
        self.csv_path = os.getenv("CSV_PATH", "data/claims_main.csv")

    # ---------------- internal ----------------
    def _connection_string(self) -> str:
        """Build the pyodbc connection string."""
        base = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
        if self.trusted:
            return base + "Trusted_Connection=yes;"
        return base + f"UID={self.user};PWD={self.password};"

    def _connect(self) -> pyodbc.Connection:
        """Open connection to SQL Server."""
        return pyodbc.connect(self._connection_string(), timeout=5)

    # ---------------- public ----------------
    def load_claims(self) -> pd.DataFrame:
        """Try SQL first, then CSV, then sample data."""
        try:
            df = self._load_from_sql()
            if not df.empty:
                return df
            logger.warning("SQL returned empty; trying CSV")
        except Exception as exc:
            logger.warning("SQL load failed (%s); trying CSV", exc)

        try:
            df = self._load_from_csv()
            if not df.empty:
                return df
            logger.warning("CSV empty; using sample data")
        except Exception as exc:
            logger.warning("CSV load failed (%s); using sample data", exc)

        return self._sample_data()

    def data_source(self) -> str:
        """Return 'SQL Server', 'CSV', or 'Sample' — used by Streamlit."""
        try:
            self._connect().close()
            return "SQL Server"
        except Exception:
            pass
        if os.path.exists(self.csv_path):
            return "CSV (DenialIQ)"
        return "Sample"

    # ---------------- loaders ----------------
    def _load_from_sql(self) -> pd.DataFrame:
        """Load from the normalised view."""
        query = """
            SELECT claim_id, patient_id, patient_name,
                   company_id, company_name,
                   dept_id, dept_name,
                   claim_type, claimed_amount, approved_amount,
                   paid_amount, status,
                   submission_date, decision_date, rejection_reason
            FROM vw_claims
        """
        conn = self._connect()
        df = pd.read_sql(query, conn)
        conn.close()
        logger.info("Loaded %d claims from SQL Server", len(df))
        return df

    def _load_from_csv(self) -> pd.DataFrame:
        """Load from DenialIQ CSV."""
        loader = DenialIQLoader(self.csv_path)
        df = loader.load()
        logger.info("Loaded %d claims from CSV", len(df))
        return df

    @staticmethod
    def _sample_data() -> pd.DataFrame:
        """Last-resort synthetic sample."""
        return pd.DataFrame([
            {"claim_id":1001,"patient_id":1,"patient_name":"Patient_001",
             "company_id":1,"company_name":"Star Health","dept_id":1,
             "dept_name":"Cardiology","claim_type":"INPATIENT",
             "claimed_amount":120000,"approved_amount":100000,"paid_amount":100000,
             "status":"SETTLED","submission_date":"2025-01-05",
             "decision_date":"2025-01-20","rejection_reason":None},
            {"claim_id":1002,"patient_id":2,"patient_name":"Patient_002",
             "company_id":2,"company_name":"HDFC Ergo","dept_id":2,
             "dept_name":"Orthopedics","claim_type":"OUTPATIENT",
             "claimed_amount":25000,"approved_amount":20000,"paid_amount":20000,
             "status":"APPROVED","submission_date":"2025-01-08",
             "decision_date":"2025-01-18","rejection_reason":None},
            {"claim_id":1003,"patient_id":3,"patient_name":"Patient_003",
             "company_id":3,"company_name":"ICICI Lombard","dept_id":3,
             "dept_name":"Neurology","claim_type":"INPATIENT",
             "claimed_amount":200000,"approved_amount":0,"paid_amount":0,
             "status":"DENIED","submission_date":"2025-01-10",
             "decision_date":"2025-02-20",
             "rejection_reason":"Pre-authorization missing"},
        ])


def load_claims() -> pd.DataFrame:
    """Convenience wrapper."""
    return DatabaseLoader().load_claims()


def data_source() -> str:
    """Convenience wrapper for source detection."""
    return DatabaseLoader().data_source()