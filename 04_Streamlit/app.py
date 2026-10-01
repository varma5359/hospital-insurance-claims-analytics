"""
app.py
------
Streamlit dashboard for Hospital Insurance Claims Analytics.

This file is presentation-only. All business logic lives in
03_Python_Analysis/src (database, data_validation, kpi_calculation).

Run:
    streamlit run 04_Streamlit/app.py
"""

import os
import sys
import logging
from datetime import date

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------- make src importable ----------
SRC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "03_Python_Analysis")
)
sys.path.append(SRC_PATH)

from src.database import load_claims,data_source
from src.data_validation import validate_all
from src.kpi_calculation import ClaimsKPI

# ---------- logging ----------
LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "06_Logs")
)
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "application.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("streamlit.app")

# ---------- page config ----------
st.set_page_config(
    page_title="Hospital Claims Analytics",
    page_icon="🏥",
    layout="wide",
)


# =========================================================
# Data loading
# =========================================================
@st.cache_data(show_spinner="Loading claims...")
def get_data() -> pd.DataFrame:
    """Load claims once and cache for the session."""
    logger.info("Loading claims data")
    df = load_claims()
    logger.info("Loaded %d claims", len(df))
    return df


# =========================================================
# Sidebar filters
# =========================================================
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render sidebar filters and return the filtered dataframe.

    Filters: date range, insurance company, department,
             claim status, claim type.
    """
    st.sidebar.header("🔍 Filters")

    # Date range
    sub_dates = pd.to_datetime(df["submission_date"], errors="coerce")
    min_date = sub_dates.min().date() if sub_dates.notna().any() else date.today()
    max_date = sub_dates.max().date() if sub_dates.notna().any() else date.today()

    date_range = st.sidebar.date_input(
        "Submission date range",
        value=(min_date, max_date),
    )

    # Categorical filters
    companies = ["All"] + sorted(df["company_name"].dropna().unique().tolist())
    company = st.sidebar.selectbox("Insurance company", companies)

    depts = ["All"] + sorted(df["dept_name"].dropna().unique().tolist())
    dept = st.sidebar.selectbox("Department", depts)

    statuses = ["All"] + sorted(df["status"].dropna().unique().tolist())
    status = st.sidebar.selectbox("Status", statuses)

    types = ["All"] + sorted(df["claim_type"].dropna().unique().tolist())
    claim_type = st.sidebar.selectbox("Claim type", types)

    # Apply filters
    out = df.copy()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        sd = pd.to_datetime(out["submission_date"], errors="coerce")
        out = out[(sd >= start) & (sd <= end)]

    if company    != "All":
        out = out[out["company_name"] == company]
    if dept       != "All":
        out = out[out["dept_name"] == dept]
    if status     != "All":
        out = out[out["status"] == status]
    if claim_type != "All":
        out = out[out["claim_type"] == claim_type]

    logger.info("Filters applied → %d rows", len(out))
    return out


# =========================================================
# Rendering helpers
# =========================================================
def render_header() -> None:
    """Page title + subtitle + data source badge."""
    st.title("🏥 Hospital Insurance Claims Analytics")
    source = data_source()
    st.caption(
        f"MediCare Multi-Specialty Hospital · Claims & Revenue Dashboard "
        f"· **Data source:** {source}"
    )
    st.markdown("---")


def render_kpi_cards(kpi: ClaimsKPI) -> None:
    """Top-row KPI cards."""
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Claims",   kpi.total_claims())
    c2.metric("Approval Rate",  f"{kpi.approval_rate()} %")
    c3.metric("Denial Rate",    f"{kpi.denial_rate()} %")
    c4.metric("Avg Processing", f"{kpi.avg_processing_time()} days")


def render_status_charts(kpi: ClaimsKPI) -> None:
    """Bar + pie chart for claims by status."""
    s = kpi.claims_by_status()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Claims by Status")
        if s.empty:
            st.info("No data for the current filters.")
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(s["status"], s["count"], color="steelblue")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            plt.close(fig)

    with col2:
        st.subheader("🥧 Status Share")
        if s.empty:
            st.info("No data for the current filters.")
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(s["count"], labels=s["status"], autopct="%1.1f%%")
            st.pyplot(fig)
            plt.close(fig)


def render_rejections(kpi: ClaimsKPI) -> None:
    """Rejection reasons table."""
    st.subheader("🚫 Rejection Reasons")
    r = kpi.rejection_reasons()
    if r.empty:
        st.success("No denied claims in the current selection.")
    else:
        st.dataframe(r, use_container_width=True)


def render_delayed(kpi: ClaimsKPI, threshold: int = 30) -> None:
    """Delayed claims table."""
    st.subheader(f"⏱ Delayed Claims (>{threshold} days)")
    delayed = kpi.delayed_claims(threshold=threshold)
    if delayed.empty:
        st.success(f"No claims delayed beyond {threshold} days.")
    else:
        cols = ["claim_id", "company_name", "dept_name",
                "processing_days", "status"]
        st.dataframe(delayed[cols], use_container_width=True)


def render_financials(kpi: ClaimsKPI) -> None:
    """Financial summary + gaps."""
    st.subheader("💰 Financial Summary")
    fin = kpi.financial_summary()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Claimed",  f"₹ {fin['total_claimed']:,.0f}")
    c2.metric("Total Approved", f"₹ {fin['total_approved']:,.0f}")
    c3.metric("Total Paid",     f"₹ {fin['total_paid']:,.0f}")

    c1, c2 = st.columns(2)
    c1.metric("Claim → Approval Gap",
              f"₹ {fin['claim_to_approval_gap']:,.0f}")
    c2.metric("Approval → Payment Gap",
              f"₹ {fin['approval_to_payment_gap']:,.0f}")


# =========================================================
# Tabs
# =========================================================
def tab_overview(kpi: ClaimsKPI) -> None:
    """Overview tab — KPIs, charts, rejections, delays, money."""
    render_kpi_cards(kpi)
    st.markdown("")
    render_status_charts(kpi)
    st.markdown("---")
    render_rejections(kpi)
    st.markdown("---")
    render_delayed(kpi)
    st.markdown("---")
    render_financials(kpi)


def tab_companies(kpi: ClaimsKPI) -> None:
    """Insurance company comparison."""
    st.subheader("🏢 Insurance Company Comparison")
    table = kpi.company_comparison()
    if table.empty:
        st.info("No data for the current filters.")
        return
    st.dataframe(table, use_container_width=True)

    st.subheader("Denial Rate by Company")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(table["company_name"], table["denial_rate"], color="indianred")
    ax.set_ylabel("Denial Rate (%)")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)
    plt.close(fig)


def tab_departments(kpi: ClaimsKPI) -> None:
    """Department analysis."""
    st.subheader("🏥 Department Analysis")
    table = kpi.department_analysis()
    if table.empty:
        st.info("No data for the current filters.")
        return
    st.dataframe(table, use_container_width=True)

    st.subheader("Claims by Department")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(table["dept_name"], table["total_claims"], color="seagreen")
    ax.set_ylabel("Claim Count")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)
    plt.close(fig)


def tab_investigation(kpi: ClaimsKPI, df: pd.DataFrame) -> None:
    """Investigate a single claim by claim_id."""
    st.subheader("🔎 Claim Investigation")
    if df.empty:
        st.info("No claims available for the current filters.")
        return

    claim_ids = sorted(df["claim_id"].dropna().unique().tolist())
    selected = st.selectbox("Select Claim ID", claim_ids)
    row = df[df["claim_id"] == selected]

    if not row.empty:
        st.markdown("### Claim Details")
        st.dataframe(row.T.rename(columns={row.index[0]: "Value"}),
                     use_container_width=True)


# =========================================================
# Main
# =========================================================
def main() -> None:
    """Entry point for the Streamlit app."""
    render_header()

    df = get_data()
    if df.empty:
        st.error("No claims data available. Check database or sample data.")
        return

    filtered = apply_filters(df)

    with st.expander("🧪 Data Quality Summary"):
        st.json(validate_all(filtered))

    kpi = ClaimsKPI(filtered, threshold_days=30)

    t1, t2, t3, t4 = st.tabs(
        ["📊 Overview", "🏢 Companies", "🏥 Departments", "🔎 Investigation"]
    )
    with t1:
        tab_overview(kpi)
    with t2:
        tab_companies(kpi)
    with t3:
        tab_departments(kpi)
    with t4:
        tab_investigation(kpi, filtered)


# ---------- run ----------
if __name__ == "__main__":
    main()