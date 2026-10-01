USE hospital_claims;
GO

-- Q1: Total claims by status
SELECT status, COUNT(*) AS total
FROM claims
GROUP BY status;

-- Q2: Denial rate by insurance company
SELECT ic.company_name,
       SUM(CASE WHEN c.status = 'DENIED' THEN 1 ELSE 0 END) AS denied,
       SUM(CASE WHEN c.status IN ('APPROVED','DENIED','SETTLED') THEN 1 ELSE 0 END) AS decided,
       ROUND(
           100.0 * SUM(CASE WHEN c.status = 'DENIED' THEN 1 ELSE 0 END)
           / NULLIF(SUM(CASE WHEN c.status IN ('APPROVED','DENIED','SETTLED') THEN 1 ELSE 0 END), 0),
           2
       ) AS denial_rate
FROM claims c
JOIN insurance_companies ic ON c.company_id = ic.company_id
GROUP BY ic.company_name;

-- Q3: Top rejection reasons
SELECT rejection_reason, COUNT(*) AS total
FROM claims
WHERE status = 'DENIED'
GROUP BY rejection_reason
ORDER BY total DESC;

-- Q4: Average processing time by department
SELECT d.dept_name,
       ROUND(AVG(DATEDIFF(DAY, c.submission_date, c.decision_date) * 1.0), 1) AS avg_days
FROM claims c
JOIN departments d ON c.dept_id = d.dept_id
WHERE c.decision_date IS NOT NULL
GROUP BY d.dept_name;

-- Q5: Financial summary (claimed vs approved vs paid)
SELECT
    SUM(claimed_amount)  AS total_claimed,
    SUM(approved_amount) AS total_approved,
    SUM(paid_amount)     AS total_paid,
    SUM(claimed_amount  - approved_amount) AS claim_gap,
    SUM(approved_amount - paid_amount)     AS payment_gap
FROM claims;