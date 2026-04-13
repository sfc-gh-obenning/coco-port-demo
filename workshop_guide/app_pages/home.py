import streamlit as st

st.title("Port of Vancouver AI Workshop")
st.markdown("Managing Canada's Pacific Gateway with Snowflake AI")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Annual trade", "$200B+", help="Port of Vancouver annual trade value")
col2.metric("Sessions", "14", help="Hands-on lab sessions")
col3.metric("Prompts", "40", help="Total Cortex Code prompts")
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

st.markdown("#### Scenario deep dive")

st.markdown("""
The Port of Vancouver operates four major container terminals along Burrard Inlet and the Fraser River delta: **Deltaport** (the largest, handling 1.8M+ TEUs annually), **Vanterm** and **Centerm** (inner harbour terminals), and **Fraser Surrey Docks** (river terminal). Each terminal is operated by a different company under lease from the Vancouver Fraser Port Authority (VFPA), creating a complex multi-stakeholder environment where data silos are the norm.
""")

with st.container(border=True):
    st.markdown("##### The operational challenge")
    st.markdown("""
On any given day, the port authority must coordinate:

- **40-60 vessels** at anchor, at berth, or in transit through the First and Second Narrows
- **Thousands of containers** moving between ship, rail, and truck — each with customs declarations, safety inspections, and commercial documentation
- **CBSA (Canada Border Services Agency)** inspections that can hold entire shipments at the border
- **CN and CP Rail** intermodal yards that connect the port to inland distribution centres across Canada
- **Trucking queues** at terminal gates where wait times directly impact driver availability and freight costs

When a vessel is delayed — by weather, congestion, mechanical issues, or a customs hold — the ripple effects cascade: berth schedules shift, rail slots are missed, truck appointments expire, and downstream warehouses face inventory gaps. A single day of port congestion can cost the Canadian economy **$20-40 million** in delayed goods.
""")

with st.container(border=True):
    st.markdown("##### What we're building and why")
    st.markdown("""
Throughout this workshop, we build a complete AI-powered operations platform that addresses real challenges faced by port authorities, terminal operators, and logistics partners:

**Predicting congestion before it happens** (Sessions 4-5)
We train ML models to predict whether a vessel's actual berth time will exceed its estimate by more than 20% — the definition of congestion. Using Snowflake's Feature Store, we manage features like TEU count, terminal capacity, cargo type, and seasonal patterns. The best model is registered in Snowflake's Model Registry and deployed as a SQL function, so any analyst can score incoming vessels without writing Python. A Dynamic Table continuously re-scores as new data arrives, giving operations teams a live congestion risk feed.

**Understanding unstructured operational data** (Sessions 6-9)
Ports generate enormous volumes of unstructured data: bills of lading PDFs, CBSA inspection reports, incident logs, partner correspondence. We use Cortex LLM functions to extract structured fields from PDFs (Document AI), build a searchable knowledge base over safety documents (Cortex Search), and create vector embeddings for semantic similarity search. This transforms filing cabinets of documents into queryable intelligence.

**Natural language access to operational data** (Sessions 10-11)
Terminal operators and port authority staff shouldn't need SQL skills to answer questions like "What are the busiest terminals by TEU count?" or "Which shipping lines have the most pending CBSA declarations?" We build a Semantic View over eight operational tables and connect it to Cortex Analyst for text-to-SQL. Then we build a Cortex Agent that combines structured data queries with document search — a single assistant that can answer both "How many TEUs did Deltaport handle last month?" and "Have there been any environmental incidents near Neptune Terminals?"

**An operations dashboard accessible to everyone** (Session 12)
We deploy a Streamlit app inside Snowflake with live KPIs, terminal maps, a chat interface powered by Cortex, and a safety compliance tracker. Because it runs on Snowflake's container runtime, it inherits all the security policies we set up earlier — masking sensitive financial data, restricting access by role — without any additional configuration.

**Governance and security from day one** (Session 3)
Before building any AI, we establish RBAC roles (PORT_ADMIN, PORT_ANALYST, PORT_VIEWER), column-level masking on sensitive financial data, and tagging policies. Every model, dashboard, and agent we build respects these boundaries automatically — a PORT_VIEWER sees masked values in the Streamlit app, and a PORT_ANALYST can query the agent but won't see financial details they're not authorized for.
""")

with st.container(border=True):
    st.markdown("##### Why this scenario matters")
    st.markdown("""
This isn't just a demo — it models a real pattern that applies across industries:

- **Multi-source data integration**: Structured tables, PDFs, time-series sensors, and geospatial coordinates — all in one platform
- **ML that operations teams can actually use**: Models registered as SQL functions, not locked inside data science notebooks
- **AI assistants grounded in your data**: Agents that combine structured queries with document search, not generic chatbots
- **Security that scales**: Governance policies set once and enforced everywhere — in dashboards, agents, and ad-hoc queries
- **Zero infrastructure management**: Feature stores, model registries, search services, and apps all running inside Snowflake with no external services to maintain

The port scenario makes these patterns tangible: every table, model, and agent maps to a real operational need. By the end of the day, you'll have built the same architecture that applies to healthcare operations, financial services, manufacturing, retail supply chains, or any domain with complex, multi-modal data.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role — see **Getting Started** in the sidebar to provision a free trial
- **Cortex Code** open in Snowsight and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.space("medium")
st.caption("Built for the April 14, 2026 workshop  :material/location_on:  Port of Vancouver, BC, Canada")
