"""SQLite storage for submitted requisitions."""
import sqlite3

DB = "requisitions.db"


def _conn():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS requisitions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT, student_name TEXT, roll_no TEXT, semester TEXT, division TEXT,
        email TEXT, mobile TEXT, app_type TEXT, other_type TEXT, purpose TEXT,
        docs_attached TEXT, doc_names TEXT, req_date TEXT, declaration_accepted INTEGER,
        submitted_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return conn


def save(d):
    with _conn() as conn:
        cur = conn.execute(
            """INSERT INTO requisitions(department,student_name,roll_no,semester,division,email,
               mobile,app_type,other_type,purpose,docs_attached,doc_names,req_date,declaration_accepted)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
            (d["department"], d["name"], d["roll"], d["semester"], d["division"], d["email"],
             d["mobile"], d["app_type"], d.get("other_type", ""), d["purpose"],
             d["docs_attached"], d["doc_names"], d["date"]))
        return cur.lastrowid
