import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(13, "Deploying AI Apps with Streamlit", "3:45 - 4:05 PM", "20 min", "3-page operations dashboard with chat interface")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on Snowflake compute, access data natively via Snowpark, and inherit Snowflake's security model. No external hosting needed.", "icon": "web"},
    {"name": "Snowpark Session", "description": "The Python interface to Snowflake within SiS apps. Provides get_active_session() for running SQL, reading tables, and calling Cortex functions from Python without managing connections.", "icon": "terminal"},
    {"name": "CREATE STREAMLIT", "description": "DDL to deploy a Streamlit app as a Snowflake object. The app lives in a schema, has permissions, and can be shared like any other Snowflake object.", "icon": "rocket_launch"},
])


PROMPT_13_1 = """Create a Streamlit in Snowflake app called PORT_OPS_DASHBOARD in PORT_AI_DEMO.PORT_OPS that provides:

PAGE 1 - Operations Dashboard:
- KPI cards at the top showing: Total TEUs this month, Active Vessels, Avg Wait Time (from TRUCK_QUEUE_TIMES), CBSA Clearance Rate (% cleared from CONTAINER_MANIFESTS)
- A bar chart of TEU volume by terminal
- A line chart showing daily container arrivals over the past 90 days
- A table of the top 10 highest congestion risk scores from LIVE_CONGESTION_SCORES

PAGE 2 - Port Intelligence Chat:
- A chat interface where users can type natural language questions
- Uses SNOWFLAKE.CORTEX.COMPLETE() to answer questions with context from our data
- Shows recent CBSA inspection summary stats in a sidebar
- Has a dropdown to select which LLM model to use

PAGE 3 - Safety & Compliance:
- Summary cards: Total incidents this month, Critical incidents, Open investigations
- A table of recent PORT_INCIDENT_LOGS with severity color coding
- A pie chart of incidents by category

Use the Snowpark session (from snowflake.snowpark.context import get_active_session). Make it visually clean with st.columns for layout.

Create the Streamlit app using SQL (CREATE STREAMLIT) and write the Python code."""

render_prompt("Prompt 13.1", "Create the Streamlit App", PROMPT_13_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake (SiS)** application - a 3-page data app:

**How SiS deployment works**:
1. Cortex Code generates the Python code for the Streamlit app
2. The code is written to a stage (auto-created or specified)
3. `CREATE STREAMLIT` registers the app as a Snowflake object

```sql
CREATE OR REPLACE STREAMLIT PORT_AI_DEMO.PORT_OPS.PORT_OPS_DASHBOARD
  ROOT_LOCATION = '@PORT_AI_DEMO.PORT_OPS.STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = PORT_AI_WH;
```

**Page 1 - Operations Dashboard** pattern:
```python
from snowflake.snowpark.context import get_active_session
session = get_active_session()

col1, col2, col3, col4 = st.columns(4)
teu_df = session.sql("SELECT SUM(teu_count) FROM CONTAINER_MANIFESTS WHERE ...").collect()
col1.metric("Total TEUs", f"{teu_df[0][0]:,.0f}")
```

**Page 2 - Chat interface** uses `st.chat_input` and `st.chat_message`:
```python
if prompt := st.chat_input("Ask about port operations..."):
    response = session.sql(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{prompt}')").collect()
    st.chat_message("assistant").write(response[0][0])
```

**Page 3 - Safety dashboard** with conditional styling:
```python
incidents_df = session.sql("SELECT * FROM PORT_INCIDENT_LOGS ORDER BY incident_date DESC").to_pandas()
```

**Key SiS advantages**:
- **No data movement**: App runs inside Snowflake, queries data directly
- **Security**: Inherits the user's role and permissions (including masking policies from Session 3)
- **Sharing**: Grant USAGE on the streamlit to share with other roles
- **No infrastructure**: No server to manage, scale, or secure
""")


PROMPT_13_2 = """Show me the SQL to verify the Streamlit app was created:

1. SHOW STREAMLITS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
2. Describe the streamlit PORT_OPS_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight."""

render_prompt("Prompt 13.2", "Test the Streamlit App", PROMPT_13_2)

render_explanation("What this prompt does", """
Verification and access:

**SHOW STREAMLITS** lists all Streamlit apps in the schema with:
- Name, database, schema
- URL endpoint
- Creation date, owner role

**DESCRIBE STREAMLIT** shows:
- Main file location
- Root stage location
- Query warehouse assigned
- Current status

**Accessing the app**: SiS apps are accessible via Snowsight at:
```
https://app.snowflake.com/<account>/#/streamlit-apps/PORT_AI_DEMO.PORT_OPS.PORT_OPS_DASHBOARD
```

**Sharing the app**:
```sql
GRANT USAGE ON STREAMLIT PORT_OPS_DASHBOARD TO ROLE PORT_ANALYST;
```

Now the PORT_ANALYST role can access the dashboard - but they'll see masked financial data (from Session 3's masking policies) and won't have access to CBSA reports. The app automatically respects row-level and column-level security.
""")


render_key_concepts([
    {"term": "Streamlit in Snowflake (SiS)", "definition": "Snowflake's native app framework for building Python data apps. Apps run on Snowflake compute, access data via Snowpark, and inherit Snowflake's security model. Deployed as first-class Snowflake objects with RBAC."},
    {"term": "get_active_session()", "definition": "The Snowpark function that returns the current Snowflake session inside a SiS app. No connection parameters needed - it automatically uses the logged-in user's credentials and role."},
    {"term": "CREATE STREAMLIT", "definition": "DDL statement to register a Streamlit app in Snowflake. Points to Python source code on a stage, assigns a warehouse for execution, and creates a shareable URL."},
])

render_what_you_built([
    "PORT_OPS_DASHBOARD - 3-page Streamlit app deployed to Snowflake",
    "Operations Dashboard with KPIs, charts, and congestion scores",
    "AI-powered chat interface with model selection",
    "Safety & Compliance page with incident tracking",
])
