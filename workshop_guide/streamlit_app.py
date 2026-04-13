from pathlib import Path

import streamlit as st

from components import is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="Port of Vancouver AI Workshop",
    page_icon=":material/anchor:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Morning Block 1": [
            st.Page("app_pages/session_01.py", title=_title(1, "AI/ML with End in Mind"), icon=":material/architecture:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Data Prep & Features"), icon=":material/database:"),
            st.Page("app_pages/session_03.py", title=_title(3, "Security & Governance"), icon=":material/shield:"),
        ],
        "Morning Block 2": [
            st.Page("app_pages/session_04.py", title=_title(4, "Snowpark ML"), icon=":material/model_training:"),
            st.Page("app_pages/session_05.py", title=_title(5, "Dynamic Tables"), icon=":material/sync:"),
            st.Page("app_pages/session_06.py", title=_title(6, "Cortex LLM Functions"), icon=":material/psychology:"),
        ],
        "Afternoon Block 1": [
            st.Page("app_pages/session_07.py", title=_title(7, "Document AI"), icon=":material/description:"),
            st.Page("app_pages/session_08.py", title=_title(8, "Cortex Search & RAG"), icon=":material/search:"),
            st.Page("app_pages/session_09.py", title=_title(9, "Vector Embeddings"), icon=":material/scatter_plot:"),
        ],
        "Afternoon Block 2": [
            st.Page("app_pages/session_10.py", title=_title(10, "Cortex Analyst & Semantic Views"), icon=":material/chat:"),
            st.Page("app_pages/session_11.py", title=_title(11, "Cortex Agents"), icon=":material/smart_toy:"),
            st.Page("app_pages/session_12.py", title=_title(12, "Streamlit Apps"), icon=":material/web:"),
            st.Page("app_pages/session_13.py", title=_title(13, "Observability & Cost"), icon=":material/monitoring:"),
            st.Page("app_pages/session_14.py", title=_title(14, "Free-form Exploration"), icon=":material/explore:"),
        ],
    },
    position="sidebar",
)

page.run()
