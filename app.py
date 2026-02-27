import streamlit as st
import time

from engine.monitor import generate_metrics, generate_logs
from engine.detector import detect_anomaly
from engine.reasoner import reason
from engine.healer import apply_fix
from engine.memory import store_incident, fetch_history


st.set_page_config("Self-Healing AI Infra", layout="wide")

st.title("🤖 Autonomous Self-Healing Infrastructure Platform")

run = st.toggle("▶️ Start System")


col1, col2, col3 = st.columns(3)

log_box = st.empty()
decision_box = st.empty()
history_box = st.empty()


if run:

    while True:

        metrics = generate_metrics()
        logs = generate_logs(metrics)

        anomalies = detect_anomaly(metrics)

        reasoning = reason(anomalies, logs)

        fix_result = apply_fix(reasoning["fix"])

        store_incident(
            reasoning["cause"],
            reasoning["fix"],
            reasoning["confidence"],
            metrics["timestamp"]
        )

        # UI Updates
        with col1:
            st.subheader("📊 Metrics")
            st.json(metrics)

        with col2:
            st.subheader("📜 Logs")
            for l in logs:
                st.write(l)

        with col3:
            st.subheader("🧠 AI Diagnosis")
            st.json(reasoning)
            st.success(fix_result)

        history = fetch_history()

        history_box.subheader("📚 Incident Memory")
        history_box.table(history)

        time.sleep(3)