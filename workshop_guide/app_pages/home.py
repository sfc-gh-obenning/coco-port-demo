import streamlit as st

st.title("Port of Vancouver AI Workshop")
st.markdown("Managing Canada's Pacific Gateway with Snowflake AI")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Annual trade", "$200B+", help="Port of Vancouver annual trade value")
col2.metric("Sessions", "14", help="Hands-on lab sessions")
col3.metric("Prompts", "33", help="Total Cortex Code prompts")
col4.metric("Duration", "~6 hrs", help="Total hands-on content time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code**.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

All prompts build on each other sequentially — run them in order throughout the day.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
The **Port of Vancouver** is Canada's largest port and the third-largest in North America,
handling over **$200 billion in annual trade**. As the Pacific Gateway, it connects Canadian
exporters of grain, potash, lumber, and coal with Asia-Pacific markets, while importing
electronics, automotive parts, textiles, and consumer goods.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Container manifests, shipping schedules, CBSA declarations, cargo invoices, CN/CP Rail schedules |
| **Unstructured** | Bills of lading PDFs, CBSA inspection reports, partner emails, incident logs |
| **Time series** | Container GPS tracking, crane utilization, truck queue times, temperature sensors |
| **Geospatial** | Vessel routes through Burrard Inlet, terminal coordinates, truck routing |
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role (or equivalent privileges)
- **Cortex Code** installed and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.space("medium")
st.caption("Built for the April 14, 2026 workshop  :material/location_on:  Port of Vancouver, BC, Canada")
