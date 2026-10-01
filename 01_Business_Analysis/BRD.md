# Business Requirements Document (BRD)

## 1. Business Problem
MediCare Multi-Specialty Hospital processes many insurance claims but
has no centralized view of claim performance. Management cannot easily
see denials, delays, payment gaps, or differences between claimed,
approved, and paid amounts.

## 2. Business Need
A centralized analytics system to:
- Monitor claim volume and status
- Analyze approval and denial rates
- Identify rejection reasons
- Track processing time
- Compare insurance companies
- Compare claimed / approved / paid amounts
- Identify delayed or financially impacted claims

## 3. Expected Business Outcome
Management and the claims team get a consistent, data-driven view of
claim performance so they can fix process issues instead of manually
investigating individual claims.

## 4. In Scope
- Claim, patient, insurance, and department analysis
- Claim status, approval, denial, rejection analysis
- Processing-time analysis
- Insurance company and department comparison
- KPI calculation
- Data-quality validation
- Streamlit analytics app
- Automated tests (pytest)
- Application and data-processing logging
- User Acceptance Testing (UAT)

## 5. Out of Scope
- Real patient data
- Live insurance company API integration
- Payment processing
- Machine learning models