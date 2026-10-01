-- =========================================================
-- DenialIQ staging table (25 cols) + normalised view
-- =========================================================

USE hospital_claims;
GO

-- 1. Drop old objects
IF OBJECT_ID('vw_claims', 'V') IS NOT NULL
    DROP VIEW vw_claims;
GO
IF OBJECT_ID('claims_denialiq', 'U') IS NOT NULL
    DROP TABLE claims_denialiq;
GO

-- 2. Staging table — one column per CSV column
--    All text types to avoid conversion errors during BULK INSERT
CREATE TABLE claims_denialiq (
    claim_id                 VARCHAR(50),
    claim_submission_date    VARCHAR(20),
    claim_year               VARCHAR(10),
    claim_quarter            VARCHAR(10),
    payer_type               VARCHAR(50),
    provider_specialty       VARCHAR(100),
    place_of_service_code    VARCHAR(10),
    place_of_service_desc    VARCHAR(100),
    cpt_code                 VARCHAR(20),
    modifier                 VARCHAR(20),
    primary_icd10_dx         VARCHAR(20),
    primary_icd10_desc       VARCHAR(200),
    secondary_icd10_dx       VARCHAR(200),
    secondary_dx_count       VARCHAR(10),
    prior_auth_required      VARCHAR(10),
    prior_auth_obtained      VARCHAR(10),
    prior_auth_number        VARCHAR(50),
    documentation_completeness VARCHAR(10),
    claim_amount_usd         VARCHAR(20),
    outcome                  VARCHAR(20),
    denial_reason_code       VARCHAR(20),
    denial_category          VARCHAR(50),
    dataset_version          VARCHAR(10),
    synthetic_flag           VARCHAR(10),
    generation_date          VARCHAR(20)
);
GO

-- 3. Normalised view used by the Streamlit app
CREATE VIEW vw_claims AS
SELECT
    c.claim_id                                                AS claim_id,
    NULL                                                      AS patient_id,
    NULL                                                      AS patient_name,
    NULL                                                      AS company_id,
    c.payer_type                                              AS company_name,
    NULL                                                      AS dept_id,
    c.provider_specialty                                      AS dept_name,
    c.place_of_service_desc                                   AS claim_type,
    TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2))             AS claimed_amount,

    -- derived approved_amount
    CASE UPPER(LTRIM(RTRIM(c.outcome)))
        WHEN 'PAID'        THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2))
        WHEN 'SETTLED'     THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2))
        WHEN 'PARTIAL_PAY' THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2)) * 0.70
        WHEN 'APPROVED'    THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2)) * 0.70
        ELSE 0
    END                                                       AS approved_amount,

    -- derived paid_amount
    CASE UPPER(LTRIM(RTRIM(c.outcome)))
        WHEN 'PAID'        THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2))
        WHEN 'SETTLED'     THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2))
        WHEN 'PARTIAL_PAY' THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2)) * 0.60
        WHEN 'APPROVED'    THEN TRY_CAST(c.claim_amount_usd AS DECIMAL(12,2)) * 0.60
        ELSE 0
    END                                                       AS paid_amount,

    -- normalised status
    CASE UPPER(LTRIM(RTRIM(c.outcome)))
        WHEN 'PAID'        THEN 'SETTLED'
        WHEN 'SETTLED'     THEN 'SETTLED'
        WHEN 'APPROVED'    THEN 'APPROVED'
        WHEN 'PARTIAL_PAY' THEN 'APPROVED'
        WHEN 'PARTIAL'     THEN 'APPROVED'
        WHEN 'DENIED'      THEN 'DENIED'
        WHEN 'REJECTED'    THEN 'DENIED'
        WHEN 'PENDING'     THEN 'PENDING'
        ELSE 'PENDING'
    END                                                       AS status,

    TRY_CAST(c.claim_submission_date AS DATE)                 AS submission_date,

    -- simulated decision_date = submission + 30 days
    CASE
        WHEN UPPER(LTRIM(RTRIM(c.outcome))) = 'PENDING' THEN NULL
        ELSE DATEADD(DAY, 30, TRY_CAST(c.claim_submission_date AS DATE))
    END                                                       AS decision_date,

    c.denial_reason_code                                      AS rejection_reason
FROM claims_denialiq c;
GO