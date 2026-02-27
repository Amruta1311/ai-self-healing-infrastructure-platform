import streamlit as st
import time
import pandas as pd

from engine.k8s_client import KubernetesAdapter
from engine.prom_adapter import PrometheusAdapter
from engine.telemetry import TelemetryEngine
from engine.detector import AnomalyDetector
from engine.reasoner import RootCauseAnalyzer
from engine.healer import RemediationEngine
from engine.impact import ImpactEstimator
from engine.memory import IncidentStore
from engine.llm_rca import handle_incident


# Adapters
k8s = KubernetesAdapter()
prom = PrometheusAdapter()

telemetry = TelemetryEngine(k8s, prom)
detector = AnomalyDetector()
rca = RootCauseAnalyzer()
healer = RemediationEngine()
impact = ImpactEstimator()
store = IncidentStore()

columns = [
    "Incident ID",
    "Root Cause",
    "Confidence",
    "Action",
    "SLA %",
    "Revenue Loss ($)",
    "Error Rate",
    "Latency (ms)",
    "CPU (%)",
    "Timestamp"
]


st.set_page_config("AI Ops Platform", layout="wide")

st.title("🤖 Autonomous Self-Healing AI Platform")

st.caption("Kubernetes + Prometheus Integrated")

run = st.toggle("▶️ Start Platform")


if run:

    while True:

        data = telemetry.collect()

        metrics = data["metrics"]
        infra = data["infra"]

        anomalies = detector.detect(metrics)
        print(f'Anomalies : {anomalies}')

        diagnosis = rca.analyze(anomalies, infra)
        print(f'Diagnosis : {diagnosis}')

        action = healer.execute(diagnosis)
        print(f'Action : {action}')

        business = impact.estimate(metrics, diagnosis)
        print(f'Business : {business}')

        record = {
            "cause": diagnosis["root_cause"],
            "confidence": diagnosis["confidence"],
            "action": action,
            "sla": business["sla"],
            "loss": business["estimated_loss_usd"],
            "ts": time.time()
        }

        record = {
                    "root_cause": diagnosis["root_cause"],
                    "confidence_score": diagnosis["confidence"],
                    "remediation_action": action,
                    "sla_percentage": business["sla"],
                    "estimated_revenue_loss_usd": business["estimated_loss_usd"],
                    "error_rate": metrics["errors"],
                    "avg_latency_ms": metrics["latency"],
                    "avg_cpu_utilization": metrics["cpu"],
                    "created_at": time.time()
                }

        store.store_incident(record)
        # prompt = handle_incident(record, diagnosis, business)
        # st.json(prompt)


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("📊 Prometheus Metrics")
            st.json(metrics)

        with col2:
            st.subheader("☸️ Kubernetes Health")
            st.json(infra)

        with col3:
            st.subheader("🧠 Diagnosis")
            st.json(diagnosis)
            st.success(action)

        with col4:
            st.subheader("💼 Business Impact")
            st.json(business)

        st.subheader("📚 Incident Intelligence")
        rows = store.fetch_recent()

        df = pd.DataFrame(rows, columns=columns)

        st.dataframe(df, use_container_width=True)

        time.sleep(3)