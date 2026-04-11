import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(7, "Unstructured Data Extraction with Document AI", "12:55 - 1:25 PM", "30 min", "Structured extraction pipelines from unstructured documents")

render_technologies_used([
    {"name": "LLM-based Extraction", "description": "Using CORTEX.COMPLETE() with structured output prompts to extract key fields from unstructured text. Returns JSON that can be parsed into columns.", "icon": "data_object"},
    {"name": "PARSE_JSON / TRY_PARSE_JSON", "description": "Snowflake functions to convert JSON strings into queryable VARIANT objects. TRY_PARSE_JSON handles malformed JSON gracefully by returning NULL.", "icon": "code"},
    {"name": "CTAS (CREATE TABLE AS SELECT)", "description": "Creates a table and populates it in one statement. Used here to materialize extraction results into a persistent, queryable table.", "icon": "add_circle"},
])


PROMPT_7_1 = """In PORT_AI_DEMO.PORT_OPS, use SNOWFLAKE.CORTEX.COMPLETE() to simulate document AI extraction on our BILLS_OF_LADING_TEXT table. For each of the first 10 documents:

1. Extract the following fields from the raw_text into a structured JSON format:
   - shipper_name
   - shipper_address  
   - consignee_name
   - consignee_address
   - notify_party
   - port_of_loading
   - port_of_discharge
   - vessel_name
   - voyage_number
   - container_numbers (as array)
   - cargo_description
   - gross_weight_kg
   - number_of_packages
   - freight_terms (prepaid or collect)
   - date_of_issue

Use this query pattern:
SELECT 
    document_id,
    manifest_id,
    PARSE_JSON(
        SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
            'Extract the following fields from this Bill of Lading document and return ONLY a valid JSON object with these keys: shipper_name, shipper_address, consignee_name, consignee_address, notify_party, port_of_loading, port_of_discharge, vessel_name, voyage_number, container_numbers (array), cargo_description, gross_weight_kg, number_of_packages, freight_terms, date_of_issue. Document: ' || raw_text
        )
    ) as extracted_data
FROM BILLS_OF_LADING_TEXT
LIMIT 10;

Execute and show the extracted structured data."""

render_prompt("Prompt 7.1", "Extract Structured Data from Bills of Lading", PROMPT_7_1)

render_explanation("What this prompt does", """
This demonstrates **document intelligence** - turning unstructured text into structured, queryable data:

The pattern has three layers:
1. **CORTEX.COMPLETE()** sends the document text + extraction instructions to the LLM
2. **PARSE_JSON()** converts the LLM's JSON string response into a Snowflake VARIANT
3. Individual fields are accessed with **dot notation**: `extracted_data:shipper_name::STRING`

**In production, you'd use AI_PARSE_DOCUMENT or AI_EXTRACT**:
- `AI_PARSE_DOCUMENT(stage_file, 'layout')` - Extracts text from actual PDF/image files on a Snowflake stage
- `AI_EXTRACT(text, instructions)` - Extracts specific fields from text using schema-based prompts

We use CORTEX.COMPLETE() here because our documents are already text (not PDFs on a stage), but the extraction pattern is identical.

**Bill of Lading**: The single most important document in international shipping. It serves as:
- Receipt for goods shipped
- Contract of carriage between shipper and carrier
- Document of title (whoever holds it controls the goods)

Automating BOL extraction eliminates hours of manual data entry per shipment.
""")


PROMPT_7_2 = """In PORT_AI_DEMO.PORT_OPS:

1. Create a table called EXTRACTED_BOL_DATA that stores the flattened extracted fields from our bill of lading extraction. Use a CREATE TABLE AS SELECT that:
   - Runs the extraction on all BILLS_OF_LADING_TEXT rows
   - Flattens the JSON into individual columns: document_id, manifest_id, shipper_name, consignee_name, port_of_loading, port_of_discharge, vessel_name, cargo_description, gross_weight_kg, freight_terms, extraction_timestamp (CURRENT_TIMESTAMP)

2. Then compare the AI-extracted data against our original CONTAINER_MANIFESTS data by joining on manifest_id. Show any discrepancies between declared cargo in manifests vs extracted cargo descriptions.

Execute all SQL and show 10 rows from EXTRACTED_BOL_DATA plus the comparison results."""

render_prompt("Prompt 7.2", "Build an Extraction Pipeline Table", PROMPT_7_2)

render_explanation("What this prompt does", """
This builds a **materialized extraction pipeline** and validates its output:

**Step 1 - CTAS with extraction**:
```sql
CREATE TABLE EXTRACTED_BOL_DATA AS
SELECT
  document_id, manifest_id,
  extracted:shipper_name::STRING AS shipper_name,
  extracted:consignee_name::STRING AS consignee_name,
  extracted:port_of_loading::STRING AS port_of_loading,
  ...
FROM (
  SELECT *, PARSE_JSON(SNOWFLAKE.CORTEX.COMPLETE(...)) AS extracted
  FROM BILLS_OF_LADING_TEXT
);
```

**Step 2 - Cross-validation**: Joining extracted data back to the original manifests to find discrepancies. This is a critical pattern in document processing - you always want to validate AI extractions against known structured data.

Common discrepancy types:
- Weight differences between BOL and manifest declaration
- Cargo description mismatches (could indicate fraud or errors)
- Port of loading inconsistencies

**Why materialize (table) vs. view**: Extraction via CORTEX.COMPLETE() is expensive (LLM tokens). A materialized table runs the extraction once and stores results. A view would re-extract on every query. For document processing, tables are almost always the right choice.
""")


PROMPT_7_3 = """In PORT_AI_DEMO.PORT_OPS, create a table called EXTRACTED_INSPECTION_FINDINGS from CBSA_INSPECTION_REPORTS using SNOWFLAKE.CORTEX.COMPLETE to extract:

- report_id
- inspection_type
- items_inspected (array of items checked)
- discrepancies_found (array of issues)
- compliance_status (compliant, minor_violation, major_violation)  
- recommended_actions (array)
- estimated_resolution_days (number)
- risk_category (low, medium, high, critical)

Store these as properly typed columns (using TRY_PARSE_JSON where needed). Then run a summary query showing the distribution of risk_category and compliance_status across all reports.

Execute all SQL and show results."""

render_prompt("Prompt 7.3", "Inspection Report Extraction", PROMPT_7_3)

render_explanation("What this prompt does", """
Applies the same extraction pattern to CBSA inspection reports, but with **array and nested types**:

**TRY_PARSE_JSON** is used instead of PARSE_JSON because LLM output can sometimes be malformed:
```sql
TRY_PARSE_JSON(SNOWFLAKE.CORTEX.COMPLETE(...)) AS extracted
```
If the LLM returns invalid JSON, TRY_PARSE_JSON returns NULL instead of throwing an error. This makes the pipeline resilient.

**Array extraction**: Fields like `items_inspected` and `discrepancies_found` are JSON arrays. In Snowflake, you can:
```sql
extracted:discrepancies_found::ARRAY AS discrepancies_found,
ARRAY_SIZE(extracted:discrepancies_found) AS num_discrepancies
```

**The summary query** provides an analytical view of inspection outcomes, enabling questions like:
- What percentage of inspections find violations?
- Which inspection types have the highest discrepancy rates?
- What's the average resolution time by risk category?

This transforms unstructured government documents into actionable compliance analytics.
""")


render_key_concepts([
    {"term": "Document AI / AI_PARSE_DOCUMENT", "definition": "Snowflake's native capability to extract text and structure from PDFs, images, and other document formats stored on stages. Combines OCR with layout understanding. For already-extracted text, CORTEX.COMPLETE() with structured prompts achieves similar results."},
    {"term": "PARSE_JSON vs TRY_PARSE_JSON", "definition": "PARSE_JSON converts a JSON string to a VARIANT but throws an error on invalid JSON. TRY_PARSE_JSON returns NULL on invalid input. Always use TRY_PARSE_JSON when processing LLM output, which may occasionally produce malformed JSON."},
    {"term": "VARIANT Data Type", "definition": "Snowflake's semi-structured data type that can hold JSON, Avro, or Parquet data. Access nested fields with colon notation (data:field:subfield). Can contain objects, arrays, strings, numbers, and booleans."},
    {"term": "CTAS (CREATE TABLE AS SELECT)", "definition": "Creates a new table and populates it from a query in one statement. In this session, CTAS materializes LLM extraction results so the expensive CORTEX.COMPLETE() calls only run once."},
])

render_domain_glossary([
    {"term": "Bill of Lading (BOL)", "definition": "A legal document between shipper and carrier detailing the type, quantity, and destination of goods. It serves as a receipt, contract, and document of title. Automating BOL extraction is one of the highest-ROI document AI use cases in logistics."},
    {"term": "Shipper vs Consignee", "definition": "The shipper is the party sending goods (exporter). The consignee is the party receiving goods (importer). The notify party is a third party that must be notified upon arrival."},
    {"term": "Freight Terms", "definition": "Prepaid means the shipper pays freight charges before shipment. Collect means the consignee pays upon delivery. Determines who bears the cost of transport."},
])

render_what_you_built([
    "LLM-based extraction of 15 fields from bill of lading documents",
    "EXTRACTED_BOL_DATA table with flattened, typed columns",
    "Cross-validation pipeline comparing extracted vs declared data",
    "EXTRACTED_INSPECTION_FINDINGS with arrays and nested types",
    "Compliance analytics summary across all inspection reports",
])
