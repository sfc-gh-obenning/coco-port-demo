import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(10, "Cortex Analyst & Semantic Views", "2:30 - 2:50 PM", "20 min", "Semantic view creation, AI-assisted expansion, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL. Provides domain context, business rules, and disambiguation hints.", "icon": "auto_fix_high"},
])


PROMPT_10_1 = """In PORT_AI_DEMO.PORT_OPS, create a semantic view called PORT_OPERATIONS_VIEW for use with Cortex Analyst. It should cover these 6 tables: CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, TERMINALS, VESSELS, TRADE_PARTNERS.

Include:
- Proper relationships between the tables (manifests join to terminals via destination_terminal, manifests join to vessels via vessel_id, invoices join to manifests via manifest_id)
- Facts for all key numeric columns: container_count, teu_count, weight_tonnes, declared_value_cad, actual/estimated berth time hours, invoice values, trade partner annual values
- Dimensions for categorical columns like cargo_category, cbsa_declaration_status, terminal_name, shipping_line, railway, country/region, and all date/time columns
- Add useful SYNONYMS on dimensions where users might use different terms (e.g. terminal_name could also be called 'dock' or 'berth', shipping_line could be 'carrier')
- Metrics with pre-aggregated calculations: total TEU, total containers, average berth time, total trade value, shipment count, total invoice value, average unit price
- Descriptive COMMENTs on every table, fact, dimension, and metric explaining the business meaning
- An AI_SQL_GENERATION instruction that provides domain context: this is Port of Vancouver data, CBSA means Canada Border Services Agency, peak season is Oct-Dec, key terminals are Deltaport/Vanterm/Centerm

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 10.1", "Create the Semantic View", PROMPT_10_1)

render_explanation("What this prompt does", """
Creates a **semantic view** - a first-class Snowflake object that enables natural language to SQL:

**Key components of a semantic view**:

- **TABLES**: Logical tables with aliases, primary keys, and comments
- **RELATIONSHIPS**: Foreign key joins between tables (e.g., manifests -> terminals)
- **FACTS**: Raw numeric columns available for computation (container_count, weight_tonnes)
- **DIMENSIONS**: Categorical and temporal columns for grouping/filtering, with optional synonyms
- **METRICS**: Pre-defined aggregations (SUM, AVG, COUNT) that Cortex Analyst can use directly
- **AI_SQL_GENERATION**: Custom instructions that guide how Analyst generates SQL

**Synonyms** help Cortex Analyst understand different ways users refer to the same concept:
```sql
t.terminal_name ... WITH SYNONYMS = ('terminal', 'dock', 'berth')
```
A user asking about "docks" will be matched to the terminal_name dimension.

**Facts vs Metrics**:
- Facts are raw columns (e.g., `teu_count`) — building blocks
- Metrics are pre-defined aggregations (e.g., `SUM(teu_count)`) — ready-to-use calculations
""")


PROMPT_10_2 = """Ask Cortex Analyst these two questions using PORT_AI_DEMO.PORT_OPS.PORT_OPERATIONS_VIEW:

1. "What are the top 5 terminals by total TEU volume?"
2. "What is the average crane utilization rate by terminal during peak hours?"

Show the generated SQL and results for each."""

render_prompt("Prompt 10.2", "Test the Semantic View", PROMPT_10_2)

render_explanation("What this prompt does", """
Tests the semantic view with two deliberately chosen questions:

**Question 1 should work well** — "Top 5 terminals by TEU" maps cleanly to the `total_teu` metric and `terminal_name` dimension we defined. Analyst has everything it needs: the metric, the dimension, and the relationship between manifests and terminals.

**Question 2 should fall short** — "Crane utilization by terminal" references data in the CRANE_UTILIZATION table, which **isn't in our semantic view yet**. Analyst may:
- Return an error saying it can't answer the question
- Attempt an answer using only the tables it knows about, producing incorrect or misleading results
- Hallucinate a plausible-looking but wrong query

**This is the key insight**: A semantic view is only as good as the tables and definitions it contains. When users ask questions outside the view's scope, Analyst can't help — and the failure mode matters. In the next prompt, we'll expand the view to cover this gap.
""")


PROMPT_10_3 = """Now expand our PORT_OPERATIONS_VIEW semantic view in PORT_AI_DEMO.PORT_OPS to include two more tables: CRANE_UTILIZATION and TRUCK_QUEUE_TIMES.

1. Query INFORMATION_SCHEMA.COLUMNS to get the full schema of CRANE_UTILIZATION and TRUCK_QUEUE_TIMES
2. Use SNOWFLAKE.CORTEX.COMPLETE() to generate the additional facts, dimensions, and metrics definitions from those schemas — have it suggest useful synonyms and descriptive comments
3. Recreate PORT_OPERATIONS_VIEW with all original definitions plus the new tables, relationships to TERMINALS via terminal_id, and the AI-generated definitions

Execute and verify with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 10.3", "Expand the Semantic View with AI", PROMPT_10_3)

render_explanation("What this prompt does", """
Uses an LLM to **expand** the semantic view with additional tables:

**Schema extraction** from INFORMATION_SCHEMA gives the LLM the raw column names and types for CRANE_UTILIZATION and TRUCK_QUEUE_TIMES.

**LLM generation** via CORTEX.COMPLETE():
- Infers business meaning from column names (e.g., `moves_per_hour` -> "Crane moves per hour")
- Generates appropriate SYNONYMS (e.g., `queue_time` WITH SYNONYMS = ('wait time', 'gate time'))
- Creates METRICS with useful aggregations (AVG crane utilization, peak hour wait times)
- Suggests RELATIONSHIPS to existing tables

**Why this pattern is powerful**:
- Bootstraps semantic view definitions in seconds vs. hours of manual work
- LLM understands naming conventions and infers domain meaning
- Always review the output — join paths and aggregation types may need adjustment

This demonstrates the **iterative semantic view development cycle**: create a base view, expand with AI assistance, test, and refine.
""")


PROMPT_10_4 = """Using the expanded semantic view PORT_AI_DEMO.PORT_OPS.PORT_OPERATIONS_VIEW, ask Cortex Analyst these natural language questions and show both the generated SQL and the results:

1. "What is the average crane utilization rate by terminal during peak hours?"
2. "What percentage of CBSA declarations are still pending by shipping line?"
3. "What is the average truck queue wait time during peak hours vs off-peak?"
4. "Which consignee cities receive the most valuable shipments and via which terminals?"

Re-ask the crane question from Prompt 10.2 and compare the result now that the table is included."""

render_prompt("Prompt 10.4", "Query with Natural Language", PROMPT_10_4)

render_explanation("What this prompt does", """
Tests Cortex Analyst across both the **original and newly added** tables:

**What to observe for each question**:

1. **"Crane utilization by terminal"** - The same question that failed in Prompt 10.2 — now it should work because CRANE_UTILIZATION is in the view
2. **"% pending CBSA by shipping line"** - Conditional aggregation, join to vessels via relationship (original tables)
3. **"Truck queue wait time peak vs off-peak"** - Tests TRUCK_QUEUE_TIMES (newly added table)
4. **"Most valuable shipments by city and terminal"** - Multi-dimensional GROUP BY across invoices, manifests, and terminals

**The before/after on the crane question** is the payoff — it demonstrates that expanding the semantic view directly improves what Analyst can answer.

**Synonyms in action**: Try asking about "carriers" instead of "shipping lines" — Analyst routes to the correct dimension because of the synonym definition.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, time-series analysis, and more."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions. Replaces the legacy YAML semantic model approach."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (teu_count). Dimensions are categorical/temporal columns for grouping and filtering (terminal_name, arrival_date). Metrics are pre-defined aggregations over facts (SUM(teu_count), AVG(berth_time))."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL. Use this to provide domain-specific context, define business rules, and clarify ambiguous terms."},
])

render_domain_glossary([
    {"term": "Operational KPIs", "definition": "Key Performance Indicators for port operations: TEU throughput, average berth time, CBSA clearance rate, crane moves per hour, truck gate wait time. These are the metrics terminal operators and port authorities track daily."},
    {"term": "Intermodal", "definition": "The movement of cargo using multiple transportation modes (ship -> rail -> truck) without handling the cargo itself. The container is the unit that transfers between modes. CN and CP Rail operate intermodal terminals at the port."},
])

render_what_you_built([
    "PORT_OPERATIONS_VIEW semantic view with 6 tables, relationships, and AI instructions",
    "Tested Analyst on a question it handles well vs one outside the view's scope",
    "AI-expanded view with CRANE_UTILIZATION and TRUCK_QUEUE_TIMES (8 tables total)",
    "4 natural language queries — including a before/after comparison on crane data",
])
