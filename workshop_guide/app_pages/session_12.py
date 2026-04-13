import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(12, "Deploying AI Apps with Streamlit", "3:20 - 3:40 PM", "20 min", "3-page operations dashboard with chat interface")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on container runtime with full Python package support, access data natively via Snowpark, and inherit Snowflake's security model.", "icon": "web"},
    {"name": "Compute Pool", "description": "A managed pool of container nodes that powers SiS apps on the container runtime. Provides GPU/CPU resources, auto-scales, and supports any Python package from pip or conda.", "icon": "memory"},
    {"name": "st.connection(\"snowflake\")", "description": "The Streamlit connection API for Snowflake on container runtime. Returns a connection object with a .session() method for Snowpark SQL, and a .cursor() method for raw queries. No credentials needed — inherits the logged-in user's session.", "icon": "terminal"},
])


PROMPT_12_1 = """In PORT_AI_DEMO.PORT_OPS, create a Streamlit app called PORT_OPS_DASHBOARD that runs on the container runtime (not the legacy warehouse runtime).

First, create a compute pool for the app:
- Name: PORT_AI_COMPUTE_POOL
- Use the CPU_X64_S instance family
- Min and max nodes of 1

Then create the Streamlit app on that compute pool with these 3 pages:

PAGE 1 - Operations Dashboard:
- KPI cards at the top showing: Total TEUs this month, Active Vessels, Avg Wait Time (from TRUCK_QUEUE_TIMES), CBSA Clearance Rate (% cleared from CONTAINER_MANIFESTS)
- A map of terminal locations (Deltaport, Vanterm, Centerm, Fraser Surrey) with markers sized by current TEU volume. Use st.pydeck_chart with a ScatterplotLayer — hardcode the terminal lat/lon coordinates for the Port of Vancouver area
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

Important for container runtime:
- First, create an External Access Integration that allows access to pypi.org and files.pythonhosted.org so the app can install pip packages. Create a network rule for these hosts, then an integration referencing it, and set EXTERNAL_ACCESS_INTEGRATIONS on the Streamlit app
- Do NOT use ROOT_LOCATION — use versioned stage syntax (CREATE STREAMLIT ... FROM '@stage' with VERSION)
- Write files to the stage using COPY INTO with a SELECT, for example: COPY INTO @stage/file.toml FROM (SELECT '...' AS content) OVERWRITE = TRUE
- Include a pyproject.toml in the stage with this exact structure:
  [project]
  name = "port-operations-dashboard"
  version = "1.0.0"
  requires-python = ">=3.11"
  dependencies = ["streamlit[snowflake]>=1.50.0", "pydeck", "plotly"]
- Use st.connection("snowflake") for the Snowflake connection (not get_active_session)

Make it visually clean with st.columns for layout."""

render_prompt("Prompt 12.1", "Create the Streamlit App", PROMPT_12_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake (SiS)** application running on the **container runtime**:

**Container runtime vs warehouse runtime**:
- **Container runtime** (current): Runs on a compute pool, supports any Python package, GPU access, and full pip/conda installs
- **Warehouse runtime** (legacy): Limited to pre-installed packages, no custom dependencies

**Step 1 - Create a compute pool**:
```sql
CREATE COMPUTE POOL PORT_AI_COMPUTE_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;
```

**Step 2 - Create an External Access Integration** so the container can reach PyPI to install pip packages:
```sql
CREATE OR REPLACE NETWORK RULE pypi_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE;
```
Then reference it on the Streamlit app with `EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration)`.

**Step 3 - Write files to the stage** using `COPY INTO` with a SELECT (most reliable in Cortex Code):
```sql
COPY INTO @PORT_AI_DEMO.PORT_OPS.STREAMLIT_STAGE/pyproject.toml
FROM (SELECT '[project]
name = "port-operations-dashboard"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = ["streamlit[snowflake]>=1.50.0", "pydeck", "plotly"]
' AS content)
OVERWRITE = TRUE;
```

**Step 4 - Deploy with versioned stage syntax** (container runtime does not support ROOT_LOCATION):
```sql
CREATE OR REPLACE STREAMLIT PORT_AI_DEMO.PORT_OPS.PORT_OPS_DASHBOARD
  FROM '@PORT_AI_DEMO.PORT_OPS.STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  COMPUTE_POOL = PORT_AI_COMPUTE_POOL
  EXTERNAL_ACCESS_INTEGRATIONS = (pypi_access_integration);
```

**Page 1 - Operations Dashboard** pattern:
```python
conn = st.connection("snowflake")
session = conn.session()

col1, col2, col3, col4 = st.columns(4)
teu_df = session.sql("SELECT SUM(teu_count) FROM CONTAINER_MANIFESTS WHERE ...").collect()
col1.metric("Total TEUs", f"{teu_df[0][0]:,.0f}")
```

**Page 2 - Chat interface** uses `st.chat_input` and `st.chat_message` with Cortex LLM functions.

**Page 3 - Safety dashboard** with conditional severity styling.

**Key SiS advantages**:
- **No data movement**: App runs inside Snowflake, queries data directly
- **Security**: Inherits the user's role and permissions (including masking policies from Session 3)
- **Sharing**: Grant USAGE on the streamlit to share with other roles
- **No infrastructure**: Compute pool auto-manages scaling and lifecycle
""")


PROMPT_12_2 = """Show me the SQL to verify the Streamlit app and compute pool were created:

1. SHOW COMPUTE POOLS;
2. SHOW STREAMLITS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
3. Describe the streamlit PORT_OPS_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight."""

render_prompt("Prompt 12.2", "Test the Streamlit App", PROMPT_12_2)

render_explanation("What this prompt does", """
Verification and access:

**SHOW COMPUTE POOLS** lists compute pools with:
- Name, state (ACTIVE/SUSPENDED), instance family
- Min/max nodes, current node count
- Auto-suspend and auto-resume settings

**SHOW STREAMLITS** lists all Streamlit apps in the schema with:
- Name, database, schema
- URL endpoint
- Creation date, owner role

**DESCRIBE STREAMLIT** shows:
- Main file location
- Root stage location
- Compute pool assigned (not warehouse — this confirms container runtime)
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
    {"term": "Container Runtime", "definition": "The current SiS execution environment. Apps run on a compute pool (managed container nodes) instead of a warehouse. Supports any Python package via pip/conda, GPU access, and higher resource limits. Uses versioned stage syntax (FROM '@stage') instead of the legacy ROOT_LOCATION."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes (CREATE COMPUTE POOL). You choose an instance family (CPU_X64_S, GPU_NV_S, etc.), set min/max nodes for auto-scaling, and Snowflake handles provisioning. Multiple Streamlit apps and services can share the same pool."},
    {"term": "pyproject.toml", "definition": "Required configuration file for container runtime SiS apps. Uses the [project] section with name, version, requires-python, and dependencies list. Must include streamlit[snowflake] and any other pip packages. Upload to the stage alongside the app code."},
    {"term": "Streamlit in Snowflake (SiS)", "definition": "Snowflake's native app framework for building Python data apps. Apps run on Snowflake compute, access data via Snowpark, and inherit Snowflake's security model. Deployed as first-class Snowflake objects with RBAC."},
    {"term": "st.connection(\"snowflake\")", "definition": "The Streamlit connection API for container runtime SiS apps. Call .session() for a Snowpark session or .cursor() for a raw DB-API cursor. Replaces the legacy get_active_session() pattern used in warehouse runtime."},
    {"term": "External Access Integration", "definition": "Required for container runtime apps that install pip packages. Container nodes cannot reach the internet by default — you must create a network rule allowing egress to pypi.org and files.pythonhosted.org, then wrap it in an External Access Integration and attach it to the Streamlit app."},
])

render_what_you_built([
    "PORT_AI_COMPUTE_POOL - compute pool for container runtime apps",
    "PORT_OPS_DASHBOARD - 3-page Streamlit app on container runtime",
    "Operations Dashboard with KPIs, charts, and congestion scores",
    "AI-powered chat interface with model selection",
    "Safety & Compliance page with incident tracking",
])
