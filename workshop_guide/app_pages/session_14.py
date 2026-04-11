import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(14, "AI Observability, Monitoring & Cost Optimization", "4:05 - 4:30 PM", "25 min", "Usage monitoring, cost analysis, and workshop inventory")

render_technologies_used([
    {"name": "ACCOUNT_USAGE Views", "description": "Snowflake's comprehensive usage tracking in the SNOWFLAKE database. Covers query history, warehouse credits, Cortex function usage, login history, and more. Data retained for 365 days.", "icon": "monitoring"},
    {"name": "Credit Tracking", "description": "Snowflake billing is credit-based. Warehouses, Cortex functions, Search services, and other serverless features all consume credits. Understanding credit allocation is key to cost optimization.", "icon": "payments"},
    {"name": "INFORMATION_SCHEMA", "description": "Real-time metadata about objects in any database. Combined with ACCOUNT_USAGE, provides a complete picture of what exists, who uses it, and what it costs.", "icon": "info"},
])


PROMPT_14_1 = """In PORT_AI_DEMO.PORT_OPS, run these observability queries:

1. Query SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY (or the equivalent view) to show:
   - Total Cortex function calls today/this session
   - Breakdown by function type (COMPLETE, SENTIMENT, TRANSLATE, SUMMARIZE, EMBED_TEXT)
   - Credits consumed by each function type

2. Query SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY to show:
   - Credits used by PORT_AI_WH today
   - AI Services credits separately

3. Check the health of our Cortex Search service:
   - DESCRIBE CORTEX SEARCH SERVICE port_knowledge_search
   - Show refresh history and status

4. Query the QUERY_HISTORY to show all Cortex-related queries run during our workshop, their execution times, and credit costs. Order by credits_used descending.

Execute all queries and show results."""

render_prompt("Prompt 14.1", "Monitor AI Function Usage", PROMPT_14_1)

render_explanation("What this prompt does", """
Comprehensive **AI observability** across four monitoring dimensions:

**1. Cortex function usage**:
```sql
SELECT
  function_name,
  COUNT(*) AS call_count,
  SUM(tokens) AS total_tokens,
  SUM(credits_used) AS total_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY
WHERE start_time >= CURRENT_DATE()
GROUP BY function_name
ORDER BY total_credits DESC;
```

This tells you exactly which AI functions are consuming credits. COMPLETE() calls are typically the most expensive due to LLM inference costs.

**2. Warehouse metering**:
```sql
SELECT
  warehouse_name,
  SUM(credits_used) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
WHERE usage_date = CURRENT_DATE()
  AND warehouse_name = 'PORT_AI_WH'
GROUP BY warehouse_name;
```

**3. Search service health**: `DESCRIBE` shows the service definition, while refresh history shows if the search index is up-to-date with source data.

**4. Query history**: The `QUERY_HISTORY` view captures every SQL statement executed, with timing, cost, and resource metrics. Filtering for Cortex-related queries shows the AI workload footprint.

**Why observability matters**: AI workloads can be expensive. A single complex COMPLETE() call with a large context window can cost more than hours of warehouse compute. Understanding your cost profile is essential for production deployment.
""")


PROMPT_14_2 = """In PORT_AI_DEMO.PORT_OPS, analyze our workshop's AI cost footprint:

1. Calculate the total estimated cost breakdown of everything we built today:
   - Warehouse compute credits (PORT_AI_WH usage)
   - Cortex LLM function credits (based on token usage)
   - Cortex Search serving credits
   - Dynamic table refresh credits
   - ML model training credits

2. Generate recommendations for production optimization:
   Use SNOWFLAKE.CORTEX.COMPLETE() to analyze our usage patterns and suggest:
   - Which LLM model to use for each use case (cost vs quality tradeoff)
   - Optimal warehouse size for different workloads
   - Recommended Cortex Search TARGET_LAG for our data freshness needs
   - Whether to use dynamic tables vs scheduled tasks for the congestion scoring

Show the cost analysis and AI-generated optimization recommendations."""

render_prompt("Prompt 14.2", "Cost Optimization Analysis", PROMPT_14_2)

render_explanation("What this prompt does", """
Two-part analysis: **cost accounting** and **AI-generated optimization**:

**Part 1 - Cost breakdown**: Aggregates credits from multiple ACCOUNT_USAGE views to build a total cost picture:

| Component | Typical Workshop Cost |
|-----------|---------------------|
| Warehouse compute (MEDIUM, ~2hrs active) | ~8 credits |
| Cortex COMPLETE() calls (claude-3-5-sonnet) | ~2-5 credits |
| Cortex SENTIMENT/TRANSLATE/SUMMARIZE | ~0.5 credits |
| Cortex Search serving | ~0.5 credits |
| Dynamic table refresh | ~0.5 credits |
| ML model training | ~1 credit |
| **Total** | **~12-15 credits** |

**Part 2 - LLM-generated optimization**: Uses COMPLETE() to analyze the usage data and generate recommendations. This is a "meta" use - using AI to optimize AI costs.

**Key optimization strategies**:

| Use Case | Current | Optimized |
|----------|---------|-----------|
| Classification | claude-3-5-sonnet | llama3.1-8b (10x cheaper for simple classification) |
| Safety analysis | claude-3-5-sonnet | Keep (needs strong reasoning) |
| Sentiment | SENTIMENT() | Keep (purpose-built, cheapest option) |
| Search lag | 1 hour | 1 day (incident data doesn't change often) |
| Dynamic table lag | 1 minute | 5 minutes (sufficient for most operations) |
| Warehouse size | MEDIUM | X-SMALL for queries, MEDIUM only for ML training |

**Production cost management patterns**:
- Use resource monitors to set credit limits
- Suspend warehouses aggressively (1 min auto-suspend)
- Batch Cortex calls where possible
- Use smaller models for high-volume, low-complexity tasks
""")


PROMPT_14_3 = """In PORT_AI_DEMO.PORT_OPS, create a final summary of everything we built today:

1. List all objects in PORT_AI_DEMO.PORT_OPS with their types:
   - Tables (with row counts)
   - Views
   - Dynamic Tables
   - ML Models
   - Cortex Search Services
   - Streamlit Apps
   - Stages
   - UDFs
   - Agents

2. Show a timeline of object creation ordered by created_on timestamp.

3. Generate a brief "what we accomplished" summary using SNOWFLAKE.CORTEX.COMPLETE() that describes the full AI pipeline we built from raw data to deployed applications.

Execute and show the complete inventory."""

render_prompt("Prompt 14.3", "Workshop Summary Query", PROMPT_14_3)

render_explanation("What this prompt does", """
A comprehensive **inventory and reflection** on the workshop:

**Object inventory** uses multiple SHOW commands and INFORMATION_SCHEMA queries:
```sql
SHOW TABLES IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW VIEWS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW DYNAMIC TABLES IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW CORTEX SEARCH SERVICES IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW STREAMLITS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW STAGES IN SCHEMA PORT_AI_DEMO.PORT_OPS;
SHOW USER FUNCTIONS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
```

**Expected inventory**:
- ~15+ tables (reference + operational + extracted)
- 2+ views (feature engineering, train/test splits)
- 1 dynamic table (LIVE_CONGESTION_SCORES)
- 1 ML model (PORT_CONGESTION_MODEL)
- 1 Cortex Search service (port_knowledge_search)
- 1 Streamlit app (PORT_OPS_DASHBOARD)
- 1+ stages (SEMANTIC_MODELS)
- 1 UDF (CALCULATE_CONGESTION_RISK)
- 1 Agent (PORT_OPS_AGENT)

**Creation timeline** shows the progression from data infrastructure to AI applications.

**AI-generated summary**: COMPLETE() reviews all the objects and generates a narrative of what was built - from raw tables to a deployed AI platform. This is itself a demonstration of Cortex AI capabilities.

**The full pipeline we built today**:
```
Raw Data → Feature Engineering → ML Training → Real-time Scoring
                                                     ↓
Text Data → Embedding → Search Index → RAG Pipeline
                                          ↓
Semantic Model → Cortex Analyst → Agent → Streamlit App
```
""")


render_key_concepts([
    {"term": "ACCOUNT_USAGE", "definition": "A Snowflake-provided shared database (SNOWFLAKE.ACCOUNT_USAGE) containing views that track all account activity: queries, logins, warehouse usage, Cortex function calls, storage, and more. Data has a 45-minute latency and is retained for 365 days."},
    {"term": "Credit-based Billing", "definition": "Snowflake charges credits for compute and AI services. 1 credit = $2-4 depending on cloud provider and edition. Warehouses charge by size per second; Cortex functions charge per token; Search services charge per serving hour."},
    {"term": "Resource Monitors", "definition": "Snowflake objects that track credit consumption and take actions (notify, suspend) when thresholds are reached. Essential for preventing runaway costs in AI workloads."},
    {"term": "SHOW Commands", "definition": "Metadata commands (SHOW TABLES, SHOW DYNAMIC TABLES, SHOW STREAMLITS, etc.) that list all objects of a given type. Combined with INFORMATION_SCHEMA, they provide a complete inventory of what exists in a database."},
])

render_domain_glossary([
    {"term": "Full AI Pipeline (Workshop)", "definition": "The end-to-end architecture built across all 14 sessions: data ingestion → feature engineering → ML training → real-time scoring → document extraction → semantic search → RAG → Agent orchestration → app deployment → monitoring."},
    {"term": "Cost Profile of AI Workloads", "definition": "AI workloads have a different cost profile than traditional BI. LLM inference (COMPLETE) is expensive per call; sentiment/translate are cheaper. Understanding which tasks need which models is key to production cost management."},
])

render_what_you_built([
    "Cortex function usage monitoring queries",
    "Warehouse and AI services cost breakdown",
    "Cortex Search health check",
    "Cost optimization recommendations (AI-generated)",
    "Complete workshop object inventory and timeline",
    "Full AI pipeline summary: raw data to deployed applications",
])
