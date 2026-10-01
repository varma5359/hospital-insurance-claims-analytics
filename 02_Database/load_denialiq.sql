USE hospital_claims;
GO

TRUNCATE TABLE claims_denialiq;
GO

BULK INSERT claims_denialiq
FROM 'C:\Ravi\hospital-insurance-claims-analytics\data\claims_main.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    TABLOCK
);
GO

SELECT COUNT(*) AS loaded_rows FROM claims_denialiq;
GO