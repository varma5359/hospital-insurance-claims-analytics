"""
quick_load.py
-------------
Load DenialIQ CSV into SQL Server using pandas + pyodbc.
Handles all CSV quirks automatically.

Run:
    python quick_load.py
"""
import pandas as pd
import pyodbc

CSV_PATH = "data/claims_main.csv"
TABLE = "claims_denialiq"

# ---------- Read CSV ----------
print("Reading CSV...")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Shape: {df.shape}")

# Convert everything to strings (matches VARCHAR staging table)
df = df.astype(str).replace({"nan": None, "None": None, "<NA>": None})

# ---------- Connect ----------
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=hospital_claims;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;",
    timeout=15,
)
cur = conn.cursor()
cur.fast_executemany = True

# ---------- Clear ----------
cur.execute(f"TRUNCATE TABLE {TABLE}")
conn.commit()

# ---------- Build insert ----------
cols = df.columns.tolist()
placeholders = ",".join(["?"] * len(cols))
sql = f"INSERT INTO {TABLE} ({','.join(cols)}) VALUES ({placeholders})"

rows = [tuple(r) for r in df.itertuples(index=False, name=None)]

# ---------- Batch insert ----------
batch = 1000
for i in range(0, len(rows), batch):
    cur.executemany(sql, rows[i:i + batch])
    conn.commit()
    print(f"  {min(i + batch, len(rows))} / {len(rows)}")

print(f"✅ Done. Total rows: {len(rows)}")