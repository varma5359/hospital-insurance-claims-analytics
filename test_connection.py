"""Quick check: can we connect to SQL Server?"""
from dotenv import load_dotenv
import pyodbc, os

load_dotenv()

driver   = os.getenv("DB_DRIVER")
server   = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
user     = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
trusted  = os.getenv("DB_TRUSTED_CONNECTION", "no").lower() == "yes"

base = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Encrypt=yes;TrustServerCertificate=yes;"
)
conn_str = base + ("Trusted_Connection=yes;" if trusted
                   else f"UID={user};PWD={password};")

try:
    conn = pyodbc.connect(conn_str, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM claims")
    print("✅ Connected. Claims rows:", cur.fetchone()[0])
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)