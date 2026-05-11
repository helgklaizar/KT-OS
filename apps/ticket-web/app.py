import streamlit as st
import requests
import time

st.set_page_config(page_title="OmniSupport AI Dashboard", page_icon="🧠", layout="centered")

st.title("🧠 OmniSupport AI Ecosystem")
st.markdown("Enter a customer support query below. The system will first route it via **CatBoost**, and optionally resolve it using the **LLM Agent**.")

query = st.text_area("Customer Query:", "How many people work in the Sales department?", height=100)

col1, col2 = st.columns(2)

# API Endpoints
ROUTING_URL = "http://localhost:8000/predict"
AGENT_URL = "http://localhost:8001/ask"

if st.button("🚀 Process Ticket"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        # Phase 1: Predictive AI (Routing)
        st.subheader("Tier 1: Predictive Routing (CatBoost)")
        with st.spinner("Routing..."):
            start_time = time.time()
            try:
                res = requests.post(ROUTING_URL, json={"text": query})
                route_time = time.time() - start_time
                if res.status_code == 200:
                    data = res.json()
                    department = data.get("department", "Unknown")
                    confidence = data.get("confidence", 0.0)
                    
                    st.success(f"**Routed to:** {department} (Confidence: {confidence:.2f})")
                    st.caption(f"⚡️ Inference time: {route_time*1000:.2f} ms")
                else:
                    st.error("Routing Engine Error. Is port 8000 running?")
            except Exception as e:
                st.error(f"Failed to connect to Routing Engine: {e}")
                
        st.divider()

        # Phase 2: Generative AI (Agent)
        st.subheader("Tier 2: Cognitive Resolution (LLM Agent)")
        with st.spinner("Agent is reasoning (SQL/RAG)..."):
            start_time = time.time()
            try:
                res = requests.post(AGENT_URL, json={"text": query})
                agent_time = time.time() - start_time
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("response", "No response")
                    
                    st.info(f"**Agent Response:**\n\n{answer}")
                    st.caption(f"🧠 Resolution time: {agent_time:.2f} seconds")
                else:
                    st.error("Cognitive Agent Error. Is port 8001 running?")
            except Exception as e:
                st.error(f"Failed to connect to Cognitive Agent: {e}")
