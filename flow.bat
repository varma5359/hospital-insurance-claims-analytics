@echo off

echo Creating Hospital Insurance Claims Analytics project...

mkdir 01_Business_Analysis
mkdir 02_Database
mkdir 03_Python_Analysis
mkdir 03_Python_Analysis\src
mkdir 04_Streamlit
mkdir 05_Testing
mkdir 06_Logs

type nul > README.md

type nul > 01_Business_Analysis\BRD.md
type nul > 01_Business_Analysis\Requirements.md
type nul > 01_Business_Analysis\User_Stories.md
type nul > 01_Business_Analysis\KPI_Business_Rules.md
type nul > 01_Business_Analysis\UAT.md

type nul > 02_Database\database.sql
type nul > 02_Database\analysis_queries.sql

type nul > 03_Python_Analysis\claims_analysis.ipynb
type nul > 03_Python_Analysis\src\data_validation.py
type nul > 03_Python_Analysis\src\kpi_calculation.py
type nul > 03_Python_Analysis\src\database.py

type nul > 04_Streamlit\app.py

type nul > 05_Testing\test_claims.py

type nul > 06_Logs\application.log

type nul > requirements.txt
type nul > .env.example
type nul > .gitignore

echo.
echo ==========================================
echo Project structure created successfully!
echo ==========================================
echo.

tree /F

pause



