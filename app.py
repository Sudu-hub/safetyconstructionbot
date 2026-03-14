import sys
import os

sys.path.append(os.path.abspath("src"))

import streamlit as st
import pandas as pd

from main import (
    ask_rag_question,
    handle_csv_query,
    handle_analytics_query
)

from router.intent_router import detect_intent
from rag.vector_store import load_vector_store


DATA_FILE = "data/construction_monthly_metrics_numeric.csv"


st.set_page_config(
    page_title="Construction Safety AI",
    layout="wide"
)

st.title("🏗️ Construction Safety Intelligence Platform")

st.write(
"""
AI assistant for construction safety documentation, risk analytics,
and trend monitoring.
"""
)

# Load vector store
vs = load_vector_store()

# Sidebar
st.sidebar.header("About System")

st.sidebar.write(
"""
Capabilities:
- 📄 Safety Document Q&A (RAG)
- 📊 Safety Metrics Queries
- 📈 Risk Trend Detection
- 🤖 AI Safety Insights
"""
)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask a safety question")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    intent = detect_intent(prompt)

    if intent == "TXT":
        answer = ask_rag_question(vs, prompt)

    elif intent == "CSV":
        answer = handle_csv_query(prompt)

    elif intent == "ANALYTICS":
        answer = handle_analytics_query(prompt)

    else:
        answer = "Query type not recognized."

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# -----------------------------------
# Risk Trend Dashboard
# -----------------------------------

st.header("📊 Risk Trend Dashboard")

df = pd.read_csv(DATA_FILE)

topics = df["topic_name"].unique()

selected_topic = st.selectbox("Select Safety Topic", topics)

topic_df = df[df["topic_name"] == selected_topic]

chart = topic_df[["period_month", "risk_index"]]

st.line_chart(chart.set_index("period_month"))