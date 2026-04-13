import streamlit as st
from components import render_session_header, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(14, "Free-form Exploration", "4:05 - 4:30 PM", "25 min", "Open-ended experimentation with everything you've built")

render_technologies_used([
    {"name": "Cortex Code", "description": "Use natural language prompts to explore, extend, and experiment with all the objects you've built throughout the day. This is your sandbox time.", "icon": "code"},
    {"name": "Everything You Built", "description": "Tables, views, ML models, dynamic tables, search services, semantic views, agents, and Streamlit apps — all available to combine in new ways.", "icon": "construction"},
    {"name": "Your Own Questions", "description": "No scripts, no prompts to copy. Ask Cortex Code whatever you're curious about and see what it can do with your data.", "icon": "explore"},
])

st.markdown("#### This session is unstructured")

st.markdown("""
You've built a complete AI platform over the past 13 sessions. Now it's your turn to explore freely.
Use Cortex Code to ask your own questions, extend what you've built, or try things that caught your attention earlier.
""")

st.markdown("#### Ideas to try")

with st.container(border=True):
    st.markdown("""
**Extend the data**
- Add new tables (weather data, fuel prices, exchange rates) and see how they integrate
- Generate more synthetic data for a specific scenario you want to test
- Create new feature engineering views for different prediction targets

**Push the AI further**
- Ask the Cortex Agent complex multi-step questions that require both structured and unstructured data
- Try breaking the semantic view — ask questions it can't answer and see what happens
- Compare different LLM models on the same prompt and evaluate quality vs speed

**Build something new**
- Create a second Streamlit app focused on a specific persona (customs officer, terminal operator)
- Build a new Cortex Search service over a different document set
- Train a different ML model (e.g., predict cargo value instead of congestion)
- Add a new custom tool to the Cortex Agent

**Go deeper on governance**
- Create additional masking policies for different roles
- Test what the PORT_ANALYST role can and can't see through the Streamlit app
- Add object tags to track data lineage across the pipeline
""")

st.space("small")

st.markdown("#### What you've built today")
with st.container(border=True):
    st.markdown("""
```
Raw Data → Feature Engineering → ML Training → Real-time Scoring
                                                     ↓
Text Data → Embedding → Search Index → RAG Pipeline
                                          ↓
Semantic View → Cortex Analyst → Agent → Streamlit App
```
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tables", "~15")
col2.metric("AI services", "5+", help="ML model, Search, Analyst, Agent, LLM functions")
col3.metric("Apps", "1", help="PORT_OPS_DASHBOARD Streamlit app")
col4.metric("Roles & policies", "6", help="4 roles + 2 masking policies")

render_key_concepts([
    {"term": "Iterative Development with Cortex Code", "definition": "Cortex Code is most powerful when you iterate: try a prompt, see the result, refine, and try again. The objects you've built today form a foundation — the real value comes from extending them to fit your specific use cases."},
    {"term": "Composability", "definition": "Snowflake's AI features are designed to compose together. A semantic view feeds Cortex Analyst, which becomes a tool for an Agent, which powers a Streamlit app. Each piece works alone but becomes more powerful in combination."},
])

render_what_you_built([
    "Whatever you explored during this free-form session",
])
