import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(11, "AI-Generated Semantic Models", "2:55 - 3:15 PM", "20 min", "Auto-generated semantic model v2 and validation")

render_technologies_used([
    {"name": "INFORMATION_SCHEMA", "description": "Snowflake's metadata layer providing schema details for all objects. COLUMNS view gives column names, types, and ordinal positions for any table.", "icon": "info"},
    {"name": "LLM-Generated YAML", "description": "Using CORTEX.COMPLETE() to generate a complete semantic model YAML from table schemas. The LLM understands both YAML syntax and data modeling best practices.", "icon": "auto_fix_high"},
    {"name": "Model Comparison", "description": "Running the same questions against two different semantic models to compare SQL quality and accuracy. This is how you iterate on semantic model design.", "icon": "compare_arrows"},
])


PROMPT_11_1 = """In PORT_AI_DEMO.PORT_OPS, I want to auto-generate an improved semantic model. 

1. First, query INFORMATION_SCHEMA.COLUMNS to get the full schema of these tables: CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, CRANE_UTILIZATION, TRUCK_QUEUE_TIMES, TERMINALS, VESSELS

2. Then use SNOWFLAKE.CORTEX.COMPLETE() to generate a comprehensive semantic model YAML by passing the schema information to the LLM with this prompt:

"You are a Snowflake Cortex Analyst expert. Generate a complete semantic model YAML file for a Port of Vancouver logistics operation. Here are the table schemas: {schema_info}

The semantic model should include:
- Proper table descriptions explaining the business context
- Column descriptions with business meaning
- Correct data types and semantic roles (dimension, measure, time_dimension)  
- Relationships/joins between tables
- At least 10 sample questions covering operational KPIs
- Aggregation expressions for common metrics (avg berth time, total TEU, on-time %)
- Filters for common dimensions

Return ONLY valid YAML."

3. Store the generated YAML and upload it to the SEMANTIC_MODELS stage as port_operations_model_v2.yaml

Execute and show the generated model."""

render_prompt("Prompt 11.1", "Auto-Generate a Semantic Model", PROMPT_11_1)

render_explanation("What this prompt does", """
Uses an LLM to **auto-generate** a semantic model from database metadata:

**Step 1 - Schema extraction**:
```sql
SELECT table_name, column_name, data_type, ordinal_position
FROM PORT_AI_DEMO.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'PORT_OPS'
  AND table_name IN ('CONTAINER_MANIFESTS', 'CARGO_INVOICES', ...)
ORDER BY table_name, ordinal_position;
```

**Step 2 - LLM generation**: The full schema (table names, column names, data types) is passed to CORTEX.COMPLETE() with a detailed prompt. The LLM:
- Infers business meaning from column names (e.g., `teu_count` -> "Twenty-foot Equivalent Units")
- Classifies columns as measures, dimensions, or time dimensions
- Detects likely join keys from naming conventions (e.g., `terminal_id` in MANIFESTS -> `terminal_id` in TERMINALS)
- Generates sample questions based on the data domain

**Step 3 - Upload**: The generated YAML is written to the stage for Cortex Analyst to use.

**Why this is powerful**:
- Bootstraps a semantic model in seconds vs. hours of manual work
- Includes tables we didn't cover in Session 10 (CRANE_UTILIZATION, TRUCK_QUEUE_TIMES)
- Generates more sample questions for better Analyst accuracy

**Limitations**:
- LLM may not understand domain-specific nuances
- Join keys may be incorrect for non-obvious relationships
- Measure aggregation types may need manual review
- Always validate the generated model before production use
""")


PROMPT_11_2 = """Test the AI-generated semantic model (v2) by asking Cortex Analyst these questions using @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model_v2.yaml:

1. "What is the average truck queue wait time during peak hours vs off-peak?"
2. "Show crane utilization rates by terminal and shift"
3. "Which terminals have the best ratio of estimated vs actual berth times?"

Compare the quality of SQL generated vs our manually-created model from Session 10. Note any differences in query accuracy."""

render_prompt("Prompt 11.2", "Validate and Test the Generated Model", PROMPT_11_2)

render_explanation("What this prompt does", """
Validates the AI-generated model by testing questions that specifically target **new tables** (CRANE_UTILIZATION, TRUCK_QUEUE_TIMES) not in the v1 model:

**Question 1** tests TRUCK_QUEUE_TIMES with conditional aggregation (peak vs off-peak).

**Question 2** tests CRANE_UTILIZATION with multi-dimensional grouping (terminal + shift).

**Question 3** tests a calculated metric across CONTAINER_MANIFESTS and TERMINALS.

**Comparison methodology**:
- Does v2 generate correct SQL for these queries? (v1 can't - it doesn't have these tables)
- For shared queries (available in both models), does v2 generate better or worse SQL?
- Are the column descriptions and join paths correct?

**Iterative model improvement**: This demonstrates the semantic model development lifecycle:
1. Auto-generate a starting point with AI
2. Test with representative questions
3. Fix issues (wrong joins, missing descriptions, incorrect aggregations)
4. Add verified queries (VQRs) for questions that matter most
5. Repeat

In production, teams typically start with AI generation, then spend 80% of their time refining the model based on actual user questions.
""")


render_key_concepts([
    {"term": "Schema Introspection", "definition": "Querying INFORMATION_SCHEMA to discover table structures programmatically. This metadata becomes input for AI-generated configurations, documentation, and semantic models."},
    {"term": "AI-Generated Configuration", "definition": "Using LLMs to generate configuration files (YAML, JSON, SQL) from metadata. Powerful for bootstrapping but always requires human review. The pattern: extract metadata -> prompt LLM -> validate output -> iterate."},
    {"term": "Semantic Model Versioning", "definition": "Maintaining multiple versions of a semantic model (v1, v2) on stages allows A/B testing, rollback, and iterative improvement. Upload new versions without disrupting existing users."},
])

render_what_you_built([
    "Auto-generated semantic model v2 with 7 tables (vs 6 in v1)",
    "AI-inferred column descriptions and join relationships",
    "10+ auto-generated sample questions",
    "Validation results comparing v1 vs v2 model quality",
])
