import sqlite3

conn = sqlite3.connect("incidents.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY,
    cause TEXT,
    confidence REAL,
    action TEXT,
    sla REAL,
    loss REAL,
    timestamp REAL
)
""")
conn.commit()


def store(record):

    cur.execute("""
    INSERT INTO incidents VALUES
    (NULL,?,?,?,?,?,?)
    """, (
        record["cause"],
        record["confidence"],
        record["action"],
        record["sla"],
        record["loss"],
        record["ts"]
    ))

    conn.commit()


def history(limit=25):

    cur.execute("""
    SELECT * FROM incidents
    ORDER BY id DESC LIMIT ?
    """, (limit,))

    return cur.fetchall()