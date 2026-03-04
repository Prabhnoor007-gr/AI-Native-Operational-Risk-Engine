import streamlit as st
import time
from alert_generator import generate_alert
from risk_engine import classify_alert
from ticketing import create_ticket
from correlation_engine import correlate_alerts
from known_patterns import is_known_benign

st.set_page_config(page_title="AI Operational Risk Engine", layout="wide")

st.title("🚨 AI-Native Operational Risk Engine")

CONFIDENCE_THRESHOLD = 0.75

if "alert_history" not in st.session_state:
    st.session_state.alert_history = []

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total": 0,
        "auto_handled": 0,
        "human_review": 0,
        "p1_count": 0,
        "regulatory_flags": 0
    }

if st.button("Simulate 5 Alerts"):

    for _ in range(5):
        alert = generate_alert()
        st.session_state.alert_history.append(alert)

        classification = classify_alert(alert)

        # Governance Layer
        if classification["confidence"] < CONFIDENCE_THRESHOLD:
            classification["requires_human_review"] = True

        ticket = create_ticket(alert, classification)

        # Metrics tracking
        st.session_state.metrics["total"] += 1

        if classification["severity"] == "P1":
            st.session_state.metrics["p1_count"] += 1

        if classification["regulatory_risk"]:
            st.session_state.metrics["regulatory_flags"] += 1

        if classification["requires_human_review"]:
            st.session_state.metrics["human_review"] += 1
        else:
            st.session_state.metrics["auto_handled"] += 1

        st.subheader("New Alert")
        st.json(alert)

        st.subheader("AI Decision")
        st.json(classification)

        if classification["requires_human_review"]:
            st.error("⚠ Escalated to Human Review")
        else:
            st.success("✓ Fully Autonomous Resolution")

        st.subheader("Generated Ticket")
        st.json(ticket)

        st.markdown("---")
        time.sleep(0.5)

    correlated = correlate_alerts(st.session_state.alert_history)

    if correlated:
        st.warning("⚠ Correlated Incident Detected")
        st.json(correlated)

correlated = correlate_alerts(st.session_state.alert_history)

if correlated:
    st.warning("⚠ Correlated Incident Detected")
    st.json(correlated)

# Metrics Dashboard
st.subheader("📊 Operational Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Alerts", st.session_state.metrics["total"])
col2.metric("Auto-Handled", st.session_state.metrics["auto_handled"])
col3.metric("Human Review", st.session_state.metrics["human_review"])
col4.metric("P1 Incidents", st.session_state.metrics["p1_count"])
col5.metric("Regulatory Flags", st.session_state.metrics["regulatory_flags"])
