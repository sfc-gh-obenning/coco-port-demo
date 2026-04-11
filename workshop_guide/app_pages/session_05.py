import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(5, "Real-time Inference with Dynamic Tables", "11:25 - 11:45 AM", "20 min", "Dynamic table for live congestion scoring")

render_technologies_used([
    {"name": "Dynamic Tables", "description": "Declarative data pipelines that automatically refresh when upstream data changes. Define the transformation as a query and Snowflake handles the rest - scheduling, incremental refresh, and dependency management.", "icon": "sync"},
    {"name": "Model Inference (PREDICT)", "description": "Calling a trained model's PREDICT method directly in SQL. The model runs inside Snowflake's compute layer - no external serving infrastructure needed.", "icon": "bolt"},
    {"name": "TARGET_LAG", "description": "The maximum acceptable staleness for a dynamic table. Snowflake automatically determines when to refresh based on upstream changes and this lag setting.", "icon": "timer"},
])


PROMPT_5_1 = """In PORT_AI_DEMO.PORT_OPS, create a dynamic table called LIVE_CONGESTION_SCORES that:

1. Uses a TARGET_LAG of '1 minute' and the PORT_AI_WH warehouse
2. Joins CONTAINER_MANIFESTS with TERMINALS (same join as CONGESTION_FEATURES)
3. Computes the same features as our CONGESTION_FEATURES view
4. Calls PORT_CONGESTION_MODEL!PREDICT() to score every manifest
5. Includes columns: manifest_id, vessel_id, destination_terminal, arrival_date, cargo_category, predicted_congestion_class, predicted_congestion_probability, teu_count, cbsa_declaration_status

Execute the CREATE DYNAMIC TABLE statement, then query it to show the top 10 highest-risk shipments (sorted by congestion probability descending)."""

render_prompt("Prompt 5.1", "Create Dynamic Table for Live Scoring", PROMPT_5_1)

render_explanation("What this prompt does", """
This creates a **dynamic table** that operationalizes our ML model:

```sql
CREATE OR REPLACE DYNAMIC TABLE LIVE_CONGESTION_SCORES
  TARGET_LAG = '1 minute'
  WAREHOUSE = PORT_AI_WH
AS
  SELECT
    m.manifest_id,
    m.vessel_id,
    t.terminal_name AS destination_terminal,
    m.arrival_date,
    m.cargo_category,
    PORT_CONGESTION_MODEL!PREDICT(...) AS prediction,
    ...
  FROM CONTAINER_MANIFESTS m
  JOIN TERMINALS t ON m.destination_terminal = t.terminal_id;
```

**Dynamic Tables vs. Traditional ETL**:

| Traditional | Dynamic Tables |
|-------------|---------------|
| Write scheduled tasks/stored procedures | Declare the desired state as SQL |
| Manage dependencies manually | Auto-detects upstream changes |
| Full refresh or complex incremental logic | Automatic incremental refresh |
| Separate monitoring/alerting | Built-in refresh history & health |

**TARGET_LAG = '1 minute'**: This means the dynamic table will never be more than 1 minute behind its source data. When new rows are inserted into CONTAINER_MANIFESTS, Snowflake detects the change and triggers a refresh within 1 minute.

**Why this is powerful**: The entire pipeline - feature engineering + model inference - runs automatically. There's no Airflow DAG, no cron job, no orchestrator. Snowflake handles it all.

**Cost consideration**: A 1-minute lag means the warehouse stays active for frequent refreshes. In production, you'd typically set this to 5-15 minutes depending on your freshness requirements.
""")


PROMPT_5_2 = """In PORT_AI_DEMO.PORT_OPS:

1. Insert 5 new rows into CONTAINER_MANIFESTS with arrival_date = CURRENT_DATE, representing new vessels arriving today with varying characteristics (some high-risk: peak season, large TEU, pending CBSA status; some low-risk)
2. Wait a moment, then query LIVE_CONGESTION_SCORES to show these 5 new manifests are now scored
3. Also show the DYNAMIC_TABLE_REFRESH_HISTORY for LIVE_CONGESTION_SCORES to demonstrate the automatic refresh

Execute all SQL and show results."""

render_prompt("Prompt 5.2", "Simulate New Data and Watch Refresh", PROMPT_5_2)

render_explanation("What this prompt does", """
This demonstrates the **real-time nature** of dynamic tables:

1. **Insert new data**: We add 5 new container manifests representing today's arrivals.

2. **Observe auto-refresh**: Within ~1 minute, the LIVE_CONGESTION_SCORES table automatically refreshes and scores the new manifests.

3. **Refresh history**: The `DYNAMIC_TABLE_REFRESH_HISTORY` function shows:
   - When each refresh started and completed
   - Whether it was incremental or full
   - How many rows were added/updated
   - Compute resources consumed

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'PORT_AI_DEMO.PORT_OPS.LIVE_CONGESTION_SCORES'
))
ORDER BY refresh_start_time DESC
LIMIT 5;
```

**This is the "aha moment"**: You insert data into a source table, and downstream scoring happens automatically with no code, no scheduling, no orchestration. This is what "declarative data pipelines" means in practice.
""")


render_key_concepts([
    {"term": "Dynamic Tables", "definition": "A Snowflake table type defined by a SQL query that automatically maintains its contents as source data changes. Think of it as a materialized view that Snowflake keeps up-to-date for you, with configurable freshness guarantees."},
    {"term": "TARGET_LAG", "definition": "The maximum acceptable time between when source data changes and when the dynamic table reflects those changes. Set to '1 minute' for near-real-time, or '1 hour' / '1 day' for less time-sensitive pipelines."},
    {"term": "Incremental Refresh", "definition": "Dynamic tables can detect which source rows changed and only process the delta, rather than reprocessing the entire dataset. This is dramatically more efficient for large tables with small change volumes."},
])

render_what_you_built([
    "LIVE_CONGESTION_SCORES dynamic table with 1-minute lag",
    "Automated ML scoring pipeline (no orchestrator needed)",
    "5 new test records showing real-time scoring",
])
