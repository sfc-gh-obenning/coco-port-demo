import streamlit as st

st.title("Workshop agenda")

AGENDA = [
    ("8:30 - 9:00 AM", "Arrival, Registration & Coffee", None, None),
    ("9:00 - 9:15 AM", "Welcome & Workshop Overview", None, None),
    ("9:15 - 9:45 AM", "Session 1: Building AI & ML Solutions with the End in Mind", "30 min", "1"),
    ("9:45 - 10:15 AM", "Session 2: Preparing Data for AI & Feature Engineering", "30 min", "2"),
    ("10:15 - 10:40 AM", "Session 3: Security and Governance for AI Workloads", "25 min", "3"),
    ("10:40 - 10:55 AM", ":orange-badge[BREAK]", None, None),
    ("10:55 - 11:25 AM", "Session 4: Snowpark ML & Model Development", "30 min", "4"),
    ("11:25 - 11:45 AM", "Session 5: Real-time Inference with Dynamic Tables", "20 min", "5"),
    ("11:45 AM - 12:10 PM", "Session 6: Cortex LLM Functions & Model Comparison", "25 min", "6"),
    ("12:10 - 12:55 PM", ":orange-badge[LUNCH]", None, None),
    ("12:55 - 1:25 PM", "Session 7: Unstructured Data Extraction with Document AI", "30 min", "7"),
    ("1:25 - 1:55 PM", "Session 8: Cortex Search & RAG Architecture Patterns", "30 min", "8"),
    ("1:55 - 2:15 PM", "Session 9: Vector Embeddings Deep Dive", "20 min", "9"),
    ("2:15 - 2:30 PM", ":orange-badge[BREAK]", None, None),
    ("2:30 - 2:50 PM", "Session 10: Cortex Analyst & Semantic Views", "20 min", "10"),
    ("2:50 - 3:20 PM", "Session 11: Building Agentic Systems with Cortex Agent API", "30 min", "11"),
    ("3:20 - 3:40 PM", "Session 12: Deploying AI Apps with Streamlit", "20 min", "12"),
    ("3:40 - 4:05 PM", "Session 13: AI Observability, Monitoring & Cost Optimization", "25 min", "13"),
    ("4:05 - 4:30 PM", "Session 14: Free-form Exploration", "25 min", "14"),
    ("4:30 - 4:40 PM", "Wrap-up & Next Steps", None, None),
]

for time, title, duration, session_num in AGENDA:
    if session_num:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":material/play_circle: **{title}** :gray-badge[{duration}]")
    elif "BREAK" in title or "LUNCH" in title:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f"{title}")
    else:
        col1, col2 = st.columns([1, 4])
        col1.markdown(f"**{time}**")
        col2.markdown(f":gray[{title}]")

st.space("medium")

st.markdown("##### What you'll build by end of day")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | ~15 | Container manifests, GPS tracking, incident logs, extracted data |
| **Views** | 2+ | Feature engineering, congestion features |
| **Dynamic Tables** | 1 | Live congestion scoring pipeline |
| **ML Models** | 2+ | Congestion classification (AutoML + notebook with XGBoost/RF/LR) |
| **Cortex Search Services** | 1 | Port knowledge base search |
| **Semantic Views** | 1 | PORT_OPERATIONS_VIEW with 8 tables, metrics, and AI instructions |
| **Cortex Agents** | 1 | Port operations agent |
| **Streamlit Apps** | 1 | Operations dashboard |
| **Roles & Policies** | 4 roles, 2 masking policies | RBAC + data governance |
""")
