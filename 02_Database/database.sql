-- =========================================================
-- Hospital Insurance Claims Database
-- Database : Microsoft SQL Server
-- Data     : Synthetic (no real patient information)
-- =========================================================

-- Create database (run this once)
CREATE DATABASE hospital_claims;
GO

USE hospital_claims;
GO

-- ---------- Patients ----------
CREATE TABLE patients (
    patient_id   INT PRIMARY KEY,
    patient_name VARCHAR(100),
    age          INT,
    gender       VARCHAR(10),
    city         VARCHAR(50)
);

-- ---------- Insurance Companies ----------
CREATE TABLE insurance_companies (
    company_id   INT PRIMARY KEY,
    company_name VARCHAR(100),
    contact      VARCHAR(50)
);

-- ---------- Departments ----------
CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

-- ---------- Claims ----------
CREATE TABLE claims (
    claim_id          INT PRIMARY KEY,
    patient_id        INT,
    company_id        INT,
    dept_id           INT,
    claim_type        VARCHAR(20),      -- INPATIENT / OUTPATIENT
    claimed_amount    DECIMAL(12,2),
    approved_amount   DECIMAL(12,2),
    paid_amount       DECIMAL(12,2),
    status            VARCHAR(20),      -- SUBMITTED/APPROVED/DENIED/PENDING/SETTLED
    submission_date   DATE,
    decision_date     DATE,
    rejection_reason  VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (company_id) REFERENCES insurance_companies(company_id),
    FOREIGN KEY (dept_id)    REFERENCES departments(dept_id)
);

-- ---------- Claim Status History ----------
CREATE TABLE claim_status_history (
    history_id   INT IDENTITY(1,1) PRIMARY KEY,
    claim_id     INT,
    status       VARCHAR(20),
    changed_date DATE,
    FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);
GO

-- =========================================================
-- SAMPLE DATA
-- =========================================================

INSERT INTO insurance_companies (company_id, company_name, contact) VALUES
(1,'Star Health','9800000001'),
(2,'HDFC Ergo','9800000002'),
(3,'ICICI Lombard','9800000003'),
(4,'Bajaj Allianz','9800000004'),
(5,'Niva Bupa','9800000005');

INSERT INTO departments (dept_id, dept_name) VALUES
(1,'Cardiology'),
(2,'Orthopedics'),
(3,'Neurology'),
(4,'Oncology'),
(5,'General Surgery'),
(6,'Pediatrics');

INSERT INTO patients (patient_id, patient_name, age, gender, city) VALUES
(1,'Patient_001',34,'M','Chennai'),
(2,'Patient_002',45,'F','Mumbai'),
(3,'Patient_003',28,'M','Delhi'),
(4,'Patient_004',52,'F','Bangalore'),
(5,'Patient_005',60,'M','Hyderabad'),
(6,'Patient_006',41,'F','Pune'),
(7,'Patient_007',37,'M','Kolkata'),
(8,'Patient_008',55,'F','Chennai'),
(9,'Patient_009',29,'M','Mumbai'),
(10,'Patient_010',48,'F','Delhi');

INSERT INTO claims
(claim_id, patient_id, company_id, dept_id, claim_type,
 claimed_amount, approved_amount, paid_amount, status,
 submission_date, decision_date, rejection_reason)
VALUES
(1001,1,1,1,'INPATIENT', 120000,100000,100000,'SETTLED', '2025-01-05','2025-01-20',NULL),
(1002,2,2,2,'OUTPATIENT', 25000, 20000, 20000,'APPROVED','2025-01-08','2025-01-18',NULL),
(1003,3,3,3,'INPATIENT', 200000,     0,     0,'DENIED',  '2025-01-10','2025-02-20','Pre-authorization missing'),
(1004,4,4,4,'INPATIENT', 350000,300000,280000,'APPROVED','2025-01-12','2025-02-15',NULL),
(1005,5,5,5,'OUTPATIENT', 40000,     0,     0,'PENDING', '2025-01-15',NULL,NULL),
(1006,6,1,6,'OUTPATIENT', 15000, 12000, 12000,'APPROVED','2025-01-20','2025-01-25',NULL),
(1007,7,2,1,'INPATIENT', 180000,150000,150000,'SETTLED', '2025-01-22','2025-02-05',NULL),
(1008,8,3,2,'INPATIENT', 220000,     0,     0,'DENIED',  '2025-01-25','2025-03-05','Non-covered procedure'),
(1009,9,4,3,'OUTPATIENT', 30000, 25000, 25000,'APPROVED','2025-01-28','2025-02-02',NULL),
(1010,10,5,4,'INPATIENT', 500000,450000,400000,'APPROVED','2025-02-01','2025-03-10',NULL),
(1011,1,1,1,'OUTPATIENT', 20000, 18000, 18000,'APPROVED','2025-02-03','2025-02-08',NULL),
(1012,2,2,5,'INPATIENT', 150000,     0,     0,'DENIED',  '2025-02-05','2025-03-20','Duplicate claim'),
(1013,3,3,6,'OUTPATIENT', 10000,  9000,  9000,'APPROVED','2025-02-08','2025-02-12',NULL),
(1014,4,4,2,'INPATIENT', 260000,220000,220000,'SETTLED', '2025-02-10','2025-02-25',NULL),
(1015,5,5,3,'OUTPATIENT', 35000,     0,     0,'PENDING', '2025-02-12',NULL,NULL);

INSERT INTO claim_status_history (claim_id, status, changed_date) VALUES
(1001,'SUBMITTED','2025-01-05'),
(1001,'APPROVED', '2025-01-15'),
(1001,'SETTLED',  '2025-01-20'),
(1003,'SUBMITTED','2025-01-10'),
(1003,'DENIED',   '2025-02-20'),
(1005,'SUBMITTED','2025-01-15');
GO