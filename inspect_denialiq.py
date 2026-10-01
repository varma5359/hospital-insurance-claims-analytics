"""
inspect_denialiq.py
-------------------
One-time script to print the DenialIQ CSV structure so we can
map columns correctly.
"""
import pandas as pd

path = "data/claims_main.csv"
df = pd.read_csv(path, nrows=1000, low_memory=False)

print("=== SHAPE (first 1000) ===")
print(df.shape)

print("\n=== COLUMNS ===")
for c in df.columns:
    print(" •", c)

print("\n=== DTYPES ===")
print(df.dtypes)

print("\n=== SAMPLE (3 rows) ===")
print(df.head(3).to_string())

print("\n=== UNIQUE STATUS VALUES ===")
status_cols = [c for c in df.columns if "status" in c.lower()]
for c in status_cols:
    print(f"{c}: {df[c].dropna().unique()[:20]}")

print("\n=== DATA DICTIONARY ===")
try:
    dd = pd.read_csv("data/data_dictionary.csv")
    print(dd.to_string())
except Exception as e:
    print("(no data dictionary)", e)