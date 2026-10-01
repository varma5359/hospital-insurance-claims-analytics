"""
test_csv_loader.py
------------------
Unit tests for DenialIQLoader.
"""
import pandas as pd
import pytest

from csv_loader import DenialIQLoader


@pytest.fixture
def tiny_csv(tmp_path):
    """Create a tiny DenialIQ-like CSV for testing."""
    p = tmp_path / "tiny.csv"
    p.write_text(
        "claim_id,patient_id,payer_name,provider_specialty,"
        "place_of_service,billed_amount,allowed_amount,paid_amount,"
        "claim_status,service_date,adjudication_date,denial_code\n"
        "1,100,Star Health,Cardiology,INPATIENT,120000,100000,100000,"
        "PAID,2025-01-05,2025-01-20,\n"
        "2,101,ICICI Lombard,Neurology,INPATIENT,200000,0,0,"
        "DENIED,2025-01-10,2025-02-20,CO-16\n"
        "3,102,HDFC Ergo,Orthopedics,OUTPATIENT,25000,20000,20000,"
        "APPROVED,2025-01-08,2025-01-18,\n"
    )
    return str(p)


def test_loads_rows(tiny_csv):
    """Loader returns all rows."""
    df = DenialIQLoader(tiny_csv).load()
    assert len(df) == 3


def test_columns_mapped(tiny_csv):
    """All required columns must be present."""
    df = DenialIQLoader(tiny_csv).load()
    for c in ["claim_id", "claimed_amount", "approved_amount",
              "paid_amount", "status", "submission_date", "decision_date"]:
        assert c in df.columns


def test_status_normalised(tiny_csv):
    """Statuses must be one of the 5 project values."""
    df = DenialIQLoader(tiny_csv).load()
    assert set(df["status"]).issubset(
        {"APPROVED", "DENIED", "PENDING", "SETTLED", "SUBMITTED"}
    )


def test_paid_maps_to_settled(tiny_csv):
    """PAID → SETTLED."""
    df = DenialIQLoader(tiny_csv).load()
    row = df[df["claim_id"] == 1].iloc[0]
    assert row["status"] == "SETTLED"


def test_denied_maps_correctly(tiny_csv):
    """DENIED stays DENIED."""
    df = DenialIQLoader(tiny_csv).load()
    row = df[df["claim_id"] == 2].iloc[0]
    assert row["status"] == "DENIED"


def test_amounts_numeric(tiny_csv):
    """Amounts should be numeric."""
    df = DenialIQLoader(tiny_csv).load()
    assert df["claimed_amount"].dtype.kind in "if"
    assert df["approved_amount"].dtype.kind in "if"
    assert df["paid_amount"].dtype.kind in "if"


def test_dates_parsed(tiny_csv):
    """Dates should be datetime."""
    df = DenialIQLoader(tiny_csv).load()
    assert pd.api.types.is_datetime64_any_dtype(df["submission_date"])
    assert pd.api.types.is_datetime64_any_dtype(df["decision_date"])