import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
)

render_session_header(
    session_num=1,
    title="Building AI & ML Solutions with the End in Mind",
    time_range="9:15 - 9:45 AM",
    duration="30 min",
    building="Database, schema, warehouse, and core reference tables",
)

render_technologies_used([
    {"name": "CREATE DATABASE / SCHEMA", "description": "Snowflake's logical containers for organizing objects. Databases are the top level; schemas group related tables, views, and other objects.", "icon": "database"},
    {"name": "Virtual Warehouses", "description": "Named compute clusters that execute queries. Size (XS to 6XL) determines how many nodes are provisioned. They auto-suspend and auto-resume.", "icon": "memory"},
    {"name": "CREATE TABLE + INSERT", "description": "DDL/DML for defining and populating structured tables. Snowflake uses columnar storage with automatic micro-partitioning.", "icon": "table_chart"},
])


PROMPT_1_1 = """Create a Snowflake database called PORT_AI_DEMO with a schema called PORT_OPS and a warehouse called PORT_AI_WH (size MEDIUM). Add a brief comment on the database: "Port of Vancouver AI/ML Workshop - Pacific Gateway Operations". Then create the following reference/lookup tables with realistic sample data:

1. VESSELS - 25 rows of vessels that frequent the Port of Vancouver. Include: vessel_id, vessel_name, vessel_type (container, bulk carrier, tanker, cruise, car carrier), flag_country, dwt_tonnes, loa_meters, beam_meters, max_draft_meters, shipping_line, imo_number. Use real shipping lines like Maersk, MSC, COSCO, Hapag-Lloyd, ONE, Evergreen, CMA CGM, and cruise lines like Holland America and Princess Cruises.

2. TERMINALS - 8 rows representing real Port of Vancouver terminals: Deltaport (container), Vanterm (container), Centerm (container), Neptune Terminals (bulk), Richardson International (grain), Pacific Elevators (grain), Westshore Terminals (coal), Canada Place (cruise). Include: terminal_id, terminal_name, terminal_type, latitude, longitude (use real coordinates), num_berths, max_vessel_draft_meters, annual_capacity_tonnes.

3. TRADE_PARTNERS - 15 rows of major trading partners. Include: partner_id, country, region (Asia-Pacific, Americas, Europe), primary_exports_to_canada, primary_imports_from_canada, annual_trade_value_cad_billions. Focus on China, Japan, South Korea, India, USA, Australia, etc.

Make sure to USE the database and schema after creation. Execute all the SQL."""

render_prompt("Prompt 1.1", "Create the Foundation", PROMPT_1_1)

render_explanation("What this prompt does", """
This prompt instructs Cortex Code to generate and execute multiple SQL statements that set up the entire environment:

1. **`CREATE DATABASE PORT_AI_DEMO`** - Creates a new database. In Snowflake, a database is the highest-level container for data. The `COMMENT` clause attaches metadata that helps with discovery and documentation.

2. **`CREATE SCHEMA PORT_OPS`** - Creates a schema inside the database. Schemas are the primary way to organize tables, views, stages, and other objects into logical groups.

3. **`CREATE WAREHOUSE PORT_AI_WH WITH WAREHOUSE_SIZE = 'MEDIUM'`** - Provisions a compute cluster. A MEDIUM warehouse has 4 nodes and costs 4 credits/hour. It auto-suspends after 5 minutes of inactivity by default.

4. **`CREATE TABLE` + `INSERT INTO`** - Defines table structures with typed columns and populates them with synthetic but realistic data. Cortex Code generates the INSERT statements with domain-appropriate values.

**Why we start here**: Every subsequent session depends on these foundational objects. The reference tables (VESSELS, TERMINALS, TRADE_PARTNERS) serve as dimension tables that will be joined to fact tables created in Session 2.
""")

render_explanation("Deep dive: Snowflake architecture", """
Snowflake uses a **three-layer architecture**:

- **Cloud Services Layer**: Handles authentication, metadata, query optimization, and transaction management. This is always running.
- **Compute Layer (Virtual Warehouses)**: Executes queries. Warehouses are independent clusters that can be created, resized, suspended, and resumed on demand. Multiple warehouses can access the same data simultaneously.
- **Storage Layer**: Stores data in a proprietary columnar format with automatic compression and micro-partitioning. Data is stored in cloud object storage (S3, Azure Blob, GCS).

**Key concept - Separation of Storage and Compute**: Unlike traditional databases, you can scale compute independently of storage. This means you can have a small warehouse for light queries and a large one for heavy ML training - both reading the same data.

**Micro-partitioning**: Snowflake automatically divides tables into immutable micro-partitions of 50-500 MB. Each partition stores metadata about the min/max values in each column, enabling efficient pruning during queries.
""")


PROMPT_1_2 = """Show me the row counts for all three tables we just created (VESSELS, TERMINALS, TRADE_PARTNERS) in PORT_AI_DEMO.PORT_OPS, and show a sample of 3 rows from each table so I can verify the data looks right."""

render_prompt("Prompt 1.2", "Verify and Explore the Foundation", PROMPT_1_2)

render_explanation("What this prompt does", """
This is a verification step. Cortex Code will generate queries like:

```sql
SELECT 'VESSELS' AS table_name, COUNT(*) AS row_count FROM PORT_AI_DEMO.PORT_OPS.VESSELS
UNION ALL
SELECT 'TERMINALS', COUNT(*) FROM PORT_AI_DEMO.PORT_OPS.TERMINALS
UNION ALL
SELECT 'TRADE_PARTNERS', COUNT(*) FROM PORT_AI_DEMO.PORT_OPS.TRADE_PARTNERS;

SELECT * FROM PORT_AI_DEMO.PORT_OPS.VESSELS LIMIT 3;
```

**Why verify**: It's good practice to confirm that Cortex Code generated the expected number of rows and that the data quality looks right. Since Cortex Code generates synthetic data, you should spot-check that vessel types, terminal names, and trade partner details are realistic.
""")


render_key_concepts([
    {"term": "Virtual Warehouse", "definition": "A named compute cluster in Snowflake. Sizes range from X-Small (1 node, 1 credit/hr) to 6X-Large (512 nodes, 512 credits/hr). Warehouses auto-suspend when idle and auto-resume on query. You can have unlimited warehouses running concurrently."},
    {"term": "Database & Schema", "definition": "Databases are the top-level namespace. Schemas sit inside databases and contain tables, views, stages, functions, and other objects. The fully-qualified name is `DATABASE.SCHEMA.OBJECT`."},
    {"term": "Micro-partitioning", "definition": "Snowflake automatically splits table data into immutable chunks of 50-500 MB called micro-partitions. Each partition has metadata (min/max values, null counts) that enables the query optimizer to skip irrelevant partitions, dramatically speeding up filtered queries."},
])

render_domain_glossary([
    {"term": "Port of Vancouver", "definition": "Canada's largest port and the third-largest in North America. Located on the Pacific coast of British Columbia, it handles over $200 billion in annual trade with Asia-Pacific, the Americas, and Europe."},
    {"term": "Deltaport / Vanterm / Centerm", "definition": "The three container terminals at the Port of Vancouver. Deltaport (at Roberts Bank) is the largest. Vanterm and Centerm are in Burrard Inlet. Together they handle ~3.5 million TEUs annually."},
    {"term": "DWT (Deadweight Tonnage)", "definition": "A measure of how much weight a vessel can carry, including cargo, fuel, crew, and provisions. Larger DWT = larger vessel capacity."},
])

render_what_you_built([
    "PORT_AI_DEMO database with PORT_OPS schema",
    "PORT_AI_WH warehouse (MEDIUM size)",
    "VESSELS table - 25 ships with real shipping line data",
    "TERMINALS table - 8 real Port of Vancouver terminals",
    "TRADE_PARTNERS table - 15 major trading partners with trade values",
])
