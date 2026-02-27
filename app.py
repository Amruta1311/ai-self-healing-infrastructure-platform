import streamlit as st
import time

from engine.k8s_client import KubernetesAdapter
from engine.prom_adapter import PrometheusAdapter
from engine.telemetry import TelemetryEngine
from engine.detector import AnomalyDetector
from engine.reasoner import RootCauseAnalyzer
from engine.healer import RemediationEngine
from engine.impact import ImpactEstimator
from engine.memory import store, history


# Adapters
k8s = KubernetesAdapter()
prom = PrometheusAdapter()

telemetry = TelemetryEngine(k8s, prom)
detector = AnomalyDetector()
rca = RootCauseAnalyzer()
healer = RemediationEngine()
impact = ImpactEstimator()


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

        diagnosis = rca.analyze(anomalies, infra)

        action = healer.execute(diagnosis)

        business = impact.estimate(metrics, diagnosis)

        record = {
            "cause": diagnosis["root_cause"],
            "confidence": diagnosis["confidence"],
            "action": action,
            "sla": business["sla"],
            "loss": business["estimated_loss_usd"],
            "ts": time.time()
        }

        store(record)

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
        st.table(history())

        time.sleep(3)