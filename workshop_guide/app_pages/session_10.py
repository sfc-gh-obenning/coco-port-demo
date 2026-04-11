import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(10, "Cortex Analyst: Natural Language to SQL", "2:30 - 2:55 PM", "25 min", "Semantic model YAML and natural language SQL queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic model to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic Model (YAML)", "description": "A YAML file that describes your data in business terms: table descriptions, column meanings, metrics/measures, dimensions, joins, and sample questions. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "Snowflake Stages", "description": "Cloud storage locations in Snowflake for files. Internal stages store files within Snowflake; external stages reference S3/Azure/GCS. We use a stage to host our semantic model YAML.", "icon": "cloud_upload"},
])


PROMPT_10_1 = """Create a Cortex Analyst semantic model YAML file for our Port of Vancouver data. Save it to a Snowflake stage.

1. First create a stage: CREATE OR REPLACE STAGE PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS;

2. Create a semantic model YAML file that covers these tables:
   - CONTAINER_MANIFESTS: with meaningful descriptions for each column, including time dimensions on arrival_date, measures on container_count/teu_count/weight_tonnes/declared_value_cad
   - CARGO_INVOICES: measures on total_value_cad/quantity/unit_price_cad, dimensions on consignee_city/commodity_description
   - RAIL_SCHEDULES: dimensions on railway/destination_city/status, time dimensions on departure_datetime
   - TERMINALS: dimensions on terminal_name/terminal_type
   - VESSELS: dimensions on vessel_name/vessel_type/shipping_line
   - TRADE_PARTNERS: dimensions on country/region, measures on annual_trade_value_cad_billions

   Include proper joins between the tables (manifests->terminals, manifests->vessels, invoices->manifests).
   
   Name the model: port_operations_model
   Add sample_questions like:
   - "What are the total TEUs by terminal for Q4 2025?"
   - "Which shipping lines have the most delayed CBSA declarations?"
   - "Show monthly trade value trends for Asia-Pacific partners"
   - "What is the average berth time by cargo category?"

3. Upload the YAML to the stage.

Execute all SQL and show confirmation."""

render_prompt("Prompt 10.1", "Create the Semantic Model", PROMPT_10_1)

render_explanation("What this prompt does", """
Creates a **Cortex Analyst semantic model** - the layer that enables natural language to SQL:

**Semantic Model YAML structure**:
```yaml
name: port_operations_model
description: Port of Vancouver operations analytics
tables:
  - name: CONTAINER_MANIFESTS
    description: Container shipping manifests arriving at port
    columns:
      - name: teu_count
        description: Number of Twenty-foot Equivalent Units
        semantic_type: measure
        aggregation: sum
      - name: arrival_date
        description: Date the vessel arrived at port
        semantic_type: time_dimension
      - name: cargo_category
        description: Type of cargo being shipped
        semantic_type: dimension
    joins:
      - to_table: TERMINALS
        on: destination_terminal = terminal_id
        relationship: many_to_one
sample_questions:
  - "What are the total TEUs by terminal for Q4 2025?"
```

**Key semantic model concepts**:
- **Measures**: Numeric columns meant to be aggregated (SUM, AVG, COUNT). E.g., `teu_count`, `declared_value_cad`
- **Dimensions**: Categorical columns for grouping/filtering. E.g., `cargo_category`, `terminal_name`
- **Time dimensions**: Date/timestamp columns for time-based analysis. E.g., `arrival_date`
- **Joins**: Relationships between tables so Analyst can auto-join when needed
- **Sample questions**: Help Analyst understand the types of questions users will ask

**Stages**: The YAML file is uploaded to a Snowflake internal stage. Cortex Analyst reads it directly from there - no external hosting needed.
""")


PROMPT_10_2 = """Using the semantic model we just created at @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml, ask Cortex Analyst these natural language questions and show both the generated SQL and the results:

1. "What are the top 5 terminals by total TEU volume?"
2. "Show me monthly container arrivals for 2025 with the busiest months highlighted"
3. "Which cargo categories have the highest average declared value?"
4. "What percentage of CBSA declarations are still pending by shipping line?"
5. "Compare CN Rail vs CP Rail on-time performance to Calgary\""""

render_prompt("Prompt 10.2", "Query with Natural Language", PROMPT_10_2)

render_explanation("What this prompt does", """
Tests Cortex Analyst with five natural language questions of increasing complexity:

**How Cortex Analyst works**:
1. Your question is parsed and understood in context of the semantic model
2. The semantic model provides table/column descriptions, valid joins, and metric definitions
3. Analyst generates SQL that answers the question
4. The SQL is executed and results are returned

**What to observe for each question**:

1. **"Top 5 terminals by TEU"** - Simple aggregation + join (MANIFESTS -> TERMINALS) + ORDER BY + LIMIT
2. **"Monthly arrivals for 2025"** - Time extraction (EXTRACT MONTH), filtering (WHERE year = 2025), GROUP BY
3. **"Highest avg declared value by category"** - AVG aggregation on a measure, grouped by dimension
4. **"% pending CBSA by shipping line"** - Conditional aggregation (CASE WHEN / COUNT), percentage calculation, join to VESSELS
5. **"CN vs CP on-time to Calgary"** - Filters (railway, destination_city), calculated field (actual vs estimated arrival), comparison

**The generated SQL is visible** - this transparency is critical for trust. Business users can see exactly what query was run, verify it, and learn SQL patterns.

**Sample questions in the YAML** help Analyst understand expected query patterns. The more diverse your sample questions, the better Analyst handles novel questions.
""")


PROMPT_10_3 = """Ask Cortex Analyst these more complex questions using our semantic model at @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml:

1. "What is the correlation between container count and berth time delays? Are larger shipments more likely to cause congestion?"
2. "Show the seasonal pattern of trade - which months have the highest total cargo value and how does it compare to crane utilization?"
3. "Which consignee cities receive the most valuable shipments and via which terminals?\""""

render_prompt("Prompt 10.3", "Advanced Analyst Queries", PROMPT_10_3)

render_explanation("What this prompt does", """
These complex questions push Cortex Analyst to its limits:

1. **Correlation question** - Requires computing a statistical relationship. Analyst may use window functions, CORR() aggregate, or binned analysis.

2. **Cross-table seasonal comparison** - Requires joining MANIFESTS with CRANE_UTILIZATION and aligning on month. This tests multi-table reasoning.

3. **Multi-dimensional breakdown** - GROUP BY two dimensions (city + terminal) with an aggregated measure (total value). Tests proper join path selection.

**What can go wrong**:
- Analyst may misinterpret column names without good descriptions in the YAML
- Complex statistical questions may get simplified
- Cross-table joins may not work if the semantic model doesn't define the path

**This is why semantic model quality matters**: The YAML is the "brain" of Cortex Analyst. Poor descriptions, missing joins, or unclear measures lead to incorrect SQL. In Session 11, we'll use AI to improve our model.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic model for context. Supports aggregations, joins, filtering, time-series analysis, and more."},
    {"term": "Semantic Model (YAML)", "definition": "A YAML file that maps database objects to business concepts. Contains table descriptions, column semantic types (measure/dimension/time), joins, metrics, filters, and sample questions. This is what separates good text-to-SQL from bad."},
    {"term": "Measure vs Dimension", "definition": "Measures are numeric values meant to be aggregated (SUM revenue, AVG wait time). Dimensions are categorical values for grouping and filtering (terminal name, cargo type). Time dimensions are dates/timestamps for temporal analysis."},
    {"term": "Verified Queries (VQR)", "definition": "Sample question-SQL pairs in the semantic model that serve as few-shot examples for Analyst. When a user question is similar to a VQR, Analyst uses the verified SQL as a template, improving accuracy."},
])

render_domain_glossary([
    {"term": "Operational KPIs", "definition": "Key Performance Indicators for port operations: TEU throughput, average berth time, CBSA clearance rate, crane moves per hour, truck gate wait time. These are the metrics terminal operators and port authorities track daily."},
    {"term": "Intermodal", "definition": "The movement of cargo using multiple transportation modes (ship → rail → truck) without handling the cargo itself. The container is the unit that transfers between modes. CN and CP Rail operate intermodal terminals at the port."},
])

render_what_you_built([
    "SEMANTIC_MODELS stage for hosting YAML files",
    "port_operations_model.yaml with 6 tables, joins, and sample questions",
    "5 basic natural language queries with generated SQL",
    "3 advanced analytical queries testing multi-table reasoning",
])
