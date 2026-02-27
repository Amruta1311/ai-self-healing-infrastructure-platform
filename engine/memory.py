import sqlite3

conn = sqlite3.connect("incidents.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY,
    cause TEXT,
    fix TEXT,
    confidence REAL,
    timestamp REAL
)
""")
conn.commit()


def store_incident(cause, fix, confidence, ts):
    cur.execute(
        "INSERT INTO incidents VALUES (NULL,?,?,?,?)",
        (cause, fix, confidence, ts)
    )
    conn.commit()


def fetch_history():
    cur.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 20")
    return cur.fetchall()