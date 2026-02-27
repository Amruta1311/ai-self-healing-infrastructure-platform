import sqlite3


class IncidentStore:

    def __init__(self, db_path="incidents.db"):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self._init_schema()


    def _init_schema(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS incident_intelligence (

            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,

            root_cause TEXT NOT NULL,

            confidence_score REAL NOT NULL,

            remediation_action TEXT NOT NULL,

            sla_percentage REAL NOT NULL,

            estimated_revenue_loss_usd REAL NOT NULL,

            error_rate REAL NOT NULL,

            avg_latency_ms REAL NOT NULL,

            avg_cpu_utilization REAL NOT NULL,

            created_at REAL NOT NULL
        )
        """)

        self.conn.commit()


    def store_incident(self, record: dict):

        self.cursor.execute("""
        INSERT INTO incident_intelligence (

            root_cause,
            confidence_score,
            remediation_action,
            sla_percentage,
            estimated_revenue_loss_usd,
            error_rate,
            avg_latency_ms,
            avg_cpu_utilization,
            created_at

        ) VALUES (?,?,?,?,?,?,?,?,?)
        """, (

            record["root_cause"],
            record["confidence_score"],
            record["remediation_action"],
            record["sla_percentage"],
            record["estimated_revenue_loss_usd"],
            record["error_rate"],
            record["avg_latency_ms"],
            record["avg_cpu_utilization"],
            record["created_at"]

        ))

        self.conn.commit()


    def fetch_recent(self, limit=25):

        self.cursor.execute("""
        SELECT
            incident_id,
            root_cause,
            confidence_score,
            remediation_action,
            sla_percentage,
            estimated_revenue_loss_usd,
            error_rate,
            avg_latency_ms,
            avg_cpu_utilization,
            created_at
        FROM incident_intelligence
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()
    
    def fetch_training_data(self):
        self.cursor.execute("""
                                SELECT
                                    root_cause,
                                    avg_cpu_utilization,
                                    avg_latency_ms,
                                    error_rate,
                                FROM incident_intelligence
                                """)

        rows = self.cursor.fetchall()

        data = []

        for r in rows:
            data.append({
                "root_cause": r[0],
                "avg_cpu_utilization": r[1],
                "avg_latency_ms": r[2],
                "error_rate": r[3]
            })

        return data