# Port of Vancouver AI Workshop - Hands-On Lab Guide
## Managing Canada's Pacific Gateway with Snowflake AI

> **Format**: Each session below contains numbered prompts to paste into Cortex Code.
> Copy each prompt exactly, run it, and observe the results before moving to the next.
> All prompts build on each other sequentially through the day.

---

## Pre-Workshop: Facilitator Setup

> **Important**: The facilitator should run this first prompt before the workshop begins to ensure the environment is ready.

---

# SESSION 1: Building AI & ML Solutions with the End in Mind
**9:15 - 9:45 AM | 30 min**

> *What we're building*: The foundational database, schema, and warehouse for our Port of Vancouver AI platform. We'll also create the core reference tables that every subsequent session depends on.

### Prompt 1.1 - Create the Foundation

```
Create a Snowflake database called PORT_AI_DEMO with a schema called PORT_OPS and a warehouse called PORT_AI_WH (size MEDIUM). Add a brief comment on the database: "Port of Vancouver AI/ML Workshop - Pacific Gateway Operations". Then create the following reference/lookup tables with realistic sample data:

1. VESSELS - 25 rows of vessels that frequent the Port of Vancouver. Include: vessel_id, vessel_name, vessel_type (container, bulk carrier, tanker, cruise, car carrier), flag_country, dwt_tonnes, loa_meters, beam_meters, max_draft_meters, shipping_line, imo_number. Use real shipping lines like Maersk, MSC, COSCO, Hapag-Lloyd, ONE, Evergreen, CMA CGM, and cruise lines like Holland America and Princess Cruises.

2. TERMINALS - 8 rows representing real Port of Vancouver terminals: Deltaport (container), Vanterm (container), Centerm (container), Neptune Terminals (bulk), Richardson International (grain), Pacific Elevators (grain), Westshore Terminals (coal), Canada Place (cruise). Include: terminal_id, terminal_name, terminal_type, latitude, longitude (use real coordinates), num_berths, max_vessel_draft_meters, annual_capacity_tonnes.

3. TRADE_PARTNERS - 15 rows of major trading partners. Include: partner_id, country, region (Asia-Pacific, Americas, Europe), primary_exports_to_canada, primary_imports_from_canada, annual_trade_value_cad_billions. Focus on China, Japan, South Korea, India, USA, Australia, etc.

Make sure to USE the database and schema after creation. Execute all the SQL.
```

### Prompt 1.2 - Verify and Explore the Foundation

```
Show me the row counts for all three tables we just created (VESSELS, TERMINALS, TRADE_PARTNERS) in PORT_AI_DEMO.PORT_OPS, and show a sample of 3 rows from each table so I can verify the data looks right.
```

---

# SESSION 2: Preparing Data for AI & Feature Engineering
**9:45 - 10:15 AM | 30 min**

> *What we're building*: All the operational data tables - structured shipping data, unstructured text documents, time-series sensor data, and geospatial tracking data. This is the raw material for every AI use case.

### Prompt 2.1 - Structured Operational Data

```
In PORT_AI_DEMO.PORT_OPS, create and populate these structured operational tables with realistic synthetic data:

1. CONTAINER_MANIFESTS - 200 rows of container shipping manifests. Columns: manifest_id, vessel_id (FK to VESSELS), voyage_number, bill_of_lading_number, container_count, teu_count, origin_port (Asian ports like Shanghai, Busan, Yokohama, Hong Kong, Singapore, Kaohsiung), destination_terminal (FK to TERMINALS), cargo_category (electronics, automotive parts, textiles, machinery, consumer goods, furniture, chemicals), declared_value_cad, weight_tonnes, cbsa_declaration_status (cleared, pending, held_for_inspection, released), arrival_date (between 2025-01-01 and 2026-04-06), estimated_berth_time_hours, actual_berth_time_hours. Make arrival patterns heavier in Oct-Dec (peak Asia-Pacific trade season).

2. CARGO_INVOICES - 300 rows of commercial invoices tied to manifests. Columns: invoice_id, manifest_id (FK), shipper_name, consignee_name, consignee_city (Canadian cities: Vancouver, Calgary, Edmonton, Toronto, Montreal, Saskatoon, Winnipeg, Surrey, Richmond), commodity_hs_code, commodity_description, quantity, unit_price_cad, total_value_cad, currency_original, exchange_rate, payment_terms, invoice_date.

3. RAIL_SCHEDULES - 150 rows of CN/CP Rail intermodal schedules. Columns: schedule_id, railway (CN or CP), train_number, origin_terminal (Vancouver terminals), destination_city (Calgary, Edmonton, Saskatoon, Regina, Winnipeg, Toronto, Montreal), departure_datetime, estimated_arrival_datetime, actual_arrival_datetime, num_containers, num_rail_cars, cargo_type, status (scheduled, in_transit, arrived, delayed), delay_reason (NULL, weather, track_maintenance, congestion, mechanical).

Execute all SQL to create and populate these tables.
```

### Prompt 2.2 - Time-Series Sensor and Tracking Data

```
In PORT_AI_DEMO.PORT_OPS, create and populate these time-series tables:

1. CONTAINER_GPS_TRACKING - 500 rows of GPS pings for containers moving through Burrard Inlet and to distribution centers. Columns: tracking_id, container_id, manifest_id, timestamp (every 15 min intervals over the past 30 days), latitude (range: 49.15 to 49.35 for Vancouver/Burrard Inlet area), longitude (range: -123.30 to -122.90), speed_knots, status (at_sea, anchored, berthed, on_truck, on_rail, at_warehouse), location_description (Burrard Inlet, English Bay Anchorage, Deltaport, Surrey Distribution Center, Richmond Warehouse, CN Intermodal Yard).

2. CRANE_UTILIZATION - 400 rows of crane metrics at container terminals. Columns: metric_id, terminal_id, crane_id, timestamp (hourly over past 14 days), moves_per_hour, utilization_pct (0-100), idle_time_minutes, container_lifts, status (operating, idle, maintenance), operator_shift (day, evening, night).

3. TRUCK_QUEUE_TIMES - 300 rows at Deltaport truck gate. Columns: queue_id, terminal_id, timestamp (every 30 min over past 14 days), trucks_in_queue, avg_wait_minutes, max_wait_minutes, gate_lanes_open, weather_condition (clear, rain, fog, snow), is_peak_hour BOOLEAN.

4. CARGO_TEMPERATURE_SENSORS - 200 rows for temperature-sensitive shipments (grain, potash, perishables). Columns: sensor_id, container_id, cargo_type (grain, potash, frozen_seafood, fresh_produce, pharmaceuticals), timestamp, temperature_celsius, humidity_pct, acceptable_range_min, acceptable_range_max, alert_triggered BOOLEAN.

Execute all SQL.
```

### Prompt 2.3 - Unstructured Text Data for AI

```
In PORT_AI_DEMO.PORT_OPS, create and populate these unstructured/text data tables:

1. BILLS_OF_LADING_TEXT - 30 rows simulating extracted text from bill of lading documents. Columns: document_id, manifest_id, raw_text (generate realistic multi-paragraph bill of lading text including shipper, consignee, notify party, port of loading, port of discharge, description of goods, container numbers, weight, measurement, freight terms, date), extraction_date, document_type.

2. CBSA_INSPECTION_REPORTS - 25 rows of Canada Border Services Agency inspection reports. Columns: report_id, manifest_id, inspection_date, inspector_id, inspection_type (routine, targeted, random, referred), findings_text (detailed paragraph about inspection findings - some clean, some with discrepancies in declared vs actual cargo, some with documentation issues), risk_score (1-10), outcome (released, detained, re_exported, penalty_assessed), penalty_amount_cad.

3. PORT_INCIDENT_LOGS - 40 rows of Port Authority incident/safety logs. Columns: incident_id, incident_date, terminal_id, severity (low, medium, high, critical), category (safety, environmental, security, equipment, weather, marine), description_text (detailed paragraph about each incident - spills, equipment failures, weather delays, security alerts, marine incidents in the Burrard Inlet), resolution_text, days_to_resolve.

4. SHIPPING_PARTNER_EMAILS - 35 rows of email correspondence. Columns: email_id, from_company, to_company, subject, email_body (realistic email text about shipping delays, customs issues, rate negotiations, schedule changes, storm warnings - some in English, some in French for bilingual content), sent_date, category (operations, customs, commercial, weather_alert, scheduling), language (en, fr).

5. MARINE_SAFETY_REPORTS - 20 rows. Columns: report_id, vessel_id, report_date, report_type (navigation, pollution, accident, near_miss, weather), location_description, report_text (detailed safety narrative), recommended_actions, status (open, investigating, closed).

Make sure the text fields contain substantial, realistic content (at least 100 words each). Execute all SQL.
```

### Prompt 2.4 - Verify All Data Tables

```
Run a query in PORT_AI_DEMO.PORT_OPS that shows every table name and its row count, ordered by row count descending. Format it nicely.
```

---

# SESSION 3: Security and Governance for AI Workloads
**10:15 - 10:40 AM | 25 min**

> *What we're building*: Role-based access control, data masking policies, and object tagging to demonstrate how AI workloads should be governed - showing that sensitive cargo values, shipper identities, and CBSA data can be protected while still enabling AI/ML.

### Prompt 3.1 - RBAC for Port Operations

```
In PORT_AI_DEMO, create the following roles and grant structure to demonstrate governance for AI workloads:

1. Create roles: PORT_DATA_ENGINEER, PORT_DATA_SCIENTIST, PORT_ANALYST, PORT_CUSTOMS_OFFICER
2. Grant the following access pattern:
   - PORT_DATA_ENGINEER: full access to PORT_OPS schema (all tables, create)
   - PORT_DATA_SCIENTIST: SELECT on all tables, plus USAGE on PORT_AI_WH, plus ability to use Cortex functions (grant SNOWFLAKE.CORTEX_USER database role)
   - PORT_ANALYST: SELECT on CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, TERMINALS, VESSELS, TRADE_PARTNERS (no access to CBSA reports or incident logs)
   - PORT_CUSTOMS_OFFICER: SELECT on CBSA_INSPECTION_REPORTS, CONTAINER_MANIFESTS, BILLS_OF_LADING_TEXT only

3. Grant all roles to my current user (OBENNING) so I can test them.

Execute all the SQL and show me a summary of what was granted.
```

### Prompt 3.2 - Data Masking and Tagging

```
In PORT_AI_DEMO.PORT_OPS, implement the following governance controls:

1. Create a tag called SENSITIVITY_LEVEL with allowed values: 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED'.

2. Apply tags:
   - CARGO_INVOICES.total_value_cad -> CONFIDENTIAL
   - CARGO_INVOICES.consignee_name -> INTERNAL
   - CBSA_INSPECTION_REPORTS.findings_text -> RESTRICTED
   - CBSA_INSPECTION_REPORTS.risk_score -> CONFIDENTIAL
   - CONTAINER_MANIFESTS.declared_value_cad -> CONFIDENTIAL

3. Create a dynamic masking policy called MASK_FINANCIAL_DATA that:
   - Shows full values for PORT_DATA_ENGINEER and PORT_CUSTOMS_OFFICER roles
   - Shows '***MASKED***' for all other roles
   Apply it to CARGO_INVOICES.consignee_name.

4. Create a masking policy called MASK_DOLLAR_VALUES that:
   - Shows full values for PORT_DATA_ENGINEER and PORT_CUSTOMS_OFFICER
   - Shows 0.00 for all other roles
   Apply it to CARGO_INVOICES.total_value_cad.

Execute all SQL. Then demonstrate the masking by querying CARGO_INVOICES as the current role and show the tag assignments.
```

### Prompt 3.3 - Verify Governance

```
Run these governance verification queries in PORT_AI_DEMO.PORT_OPS:

1. Show all tag references on the PORT_OPS schema using INFORMATION_SCHEMA.TAG_REFERENCES for our SENSITIVITY_LEVEL tag
2. Show all masking policies applied using INFORMATION_SCHEMA.POLICY_REFERENCES  
3. Query 5 rows from CARGO_INVOICES to show which columns are masked for the current role

Show the results.
```

---

> **10:40 - 10:55 AM | BREAK**

---

# SESSION 4: Snowpark ML & Model Development
**10:55 - 11:25 AM | 30 min**

> *What we're building*: A machine learning model that predicts port congestion (whether berth time will exceed estimated time) using container manifest features. We'll create a feature engineering view, train a model, and register it in the Snowflake Model Registry.

### Prompt 4.1 - Feature Engineering View

```
In PORT_AI_DEMO.PORT_OPS, create a view called CONGESTION_FEATURES that joins CONTAINER_MANIFESTS with TERMINALS and builds features for predicting whether actual_berth_time_hours will exceed estimated_berth_time_hours by more than 20%. Include these features:

- container_count, teu_count, weight_tonnes, declared_value_cad
- terminal_type (from TERMINALS)
- num_berths (from TERMINALS) 
- cargo_category
- arrival_month (extracted from arrival_date)
- arrival_day_of_week
- is_peak_season (1 if month in 10,11,12 else 0)
- cbsa_declaration_status
- A target column called IS_CONGESTED (1 if actual_berth_time_hours > estimated_berth_time_hours * 1.2, else 0)

Only include rows where both actual and estimated berth times are not null. Execute the SQL, then show me the feature distribution: count of congested vs not congested, and the average values of key features for each class.
```

### Prompt 4.2 - Train a Classification Model

```
In PORT_AI_DEMO.PORT_OPS, use Snowpark ML to train a classification model to predict IS_CONGESTED from our CONGESTION_FEATURES view. Write and execute a Snowflake SQL script that:

1. Creates a TRAIN_DATA and TEST_DATA split (80/20) from CONGESTION_FEATURES using a random seed
2. Uses Snowflake's built-in ML Classification:
   
   CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION PORT_CONGESTION_MODEL(
     INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'CONGESTION_FEATURES_TRAIN'),
     TARGET_COLNAME => 'IS_CONGESTED',
     CONFIG_OBJECT => {'on_error': 'skip'}
   );

First create the train/test views, then train the model, then run predictions on the test set and show the confusion matrix results (predicted vs actual counts). Also show the feature importances if available.
```

### Prompt 4.3 - Evaluate the Model

```
Using the PORT_CONGESTION_MODEL we just trained in PORT_AI_DEMO.PORT_OPS:

1. Run predictions on the test data view and store results in a table called CONGESTION_PREDICTIONS
2. Calculate and display:
   - Overall accuracy
   - Precision and recall for the congested class
   - A confusion matrix showing TP, FP, TN, FN counts
3. Show the evaluation metrics from the model object itself using PORT_CONGESTION_MODEL!SHOW_EVALUATION_METRICS()
4. Show feature importances using PORT_CONGESTION_MODEL!SHOW_FEATURE_IMPORTANCE()

Execute all SQL and show results.
```

---

# SESSION 5: Real-time Inference with Dynamic Tables
**11:25 - 11:45 AM | 20 min**

> *What we're building*: A dynamic table that automatically re-scores new container manifests as they arrive, creating a real-time congestion risk pipeline. This shows how to operationalize ML models with zero-maintenance refresh.

### Prompt 5.1 - Create Dynamic Table for Live Scoring

```
In PORT_AI_DEMO.PORT_OPS, create a dynamic table called LIVE_CONGESTION_SCORES that:

1. Uses a TARGET_LAG of '1 minute' and the PORT_AI_WH warehouse
2. Joins CONTAINER_MANIFESTS with TERMINALS (same join as CONGESTION_FEATURES)
3. Computes the same features as our CONGESTION_FEATURES view
4. Calls PORT_CONGESTION_MODEL!PREDICT() to score every manifest
5. Includes columns: manifest_id, vessel_id, destination_terminal, arrival_date, cargo_category, predicted_congestion_class, predicted_congestion_probability, teu_count, cbsa_declaration_status

Execute the CREATE DYNAMIC TABLE statement, then query it to show the top 10 highest-risk shipments (sorted by congestion probability descending).
```

### Prompt 5.2 - Simulate New Data and Watch Refresh

```
In PORT_AI_DEMO.PORT_OPS:

1. Insert 5 new rows into CONTAINER_MANIFESTS with arrival_date = CURRENT_DATE, representing new vessels arriving today with varying characteristics (some high-risk: peak season, large TEU, pending CBSA status; some low-risk)
2. Wait a moment, then query LIVE_CONGESTION_SCORES to show these 5 new manifests are now scored
3. Also show the DYNAMIC_TABLE_REFRESH_HISTORY for LIVE_CONGESTION_SCORES to demonstrate the automatic refresh

Execute all SQL and show results.
```

---

# SESSION 6: Cortex LLM Functions & Model Comparison
**11:45 AM - 12:10 PM | 25 min**

> *What we're building*: Using Snowflake Cortex AI SQL functions to analyze port operations text data - sentiment analysis on partner emails, translation of French correspondence, summarization of incident reports, and a side-by-side model comparison.

### Prompt 6.1 - Sentiment, Summarize, Translate

```
In PORT_AI_DEMO.PORT_OPS, run the following Cortex LLM function queries:

1. SENTIMENT ANALYSIS: Run SNOWFLAKE.CORTEX.SENTIMENT() on the email_body column of SHIPPING_PARTNER_EMAILS. Show the email subject, from_company, category, and sentiment score for all rows. Order by sentiment score ascending (most negative first).

2. SUMMARIZATION: Run SNOWFLAKE.CORTEX.SUMMARIZE() on the 5 longest PORT_INCIDENT_LOGS description_text entries. Show incident_id, severity, category, and the summarized text.

3. TRANSLATION: Find all French emails in SHIPPING_PARTNER_EMAILS (where language='fr') and use SNOWFLAKE.CORTEX.TRANSLATE(email_body, 'fr', 'en') to translate them to English. Show original subject, original body (first 200 chars), and translated text.

Execute all three queries and show results.
```

### Prompt 6.2 - AI Complete for Analysis and Model Comparison

```
In PORT_AI_DEMO.PORT_OPS, demonstrate SNOWFLAKE.CORTEX.COMPLETE() with a model comparison:

1. Take the 3 most critical (severity='critical' or 'high') incidents from PORT_INCIDENT_LOGS. For each, use COMPLETE() with TWO different models to generate a risk assessment and recommended actions:
   - Model A: 'claude-3-5-sonnet' 
   - Model B: 'llama3.1-70b'
   
   Use this prompt template for each incident:
   "You are a port safety analyst at the Port of Vancouver. Analyze this incident report and provide: 1) Risk level assessment 2) Root cause analysis 3) Three recommended preventive actions. Incident: {description_text}"

2. Show the results side-by-side: incident_id, severity, model_a_response, model_b_response

Execute the query and show the comparison.
```

### Prompt 6.3 - Classify and Extract

```
In PORT_AI_DEMO.PORT_OPS:

1. Use SNOWFLAKE.CORTEX.CLASSIFY_TEXT() on the CBSA_INSPECTION_REPORTS findings_text to classify each report into risk categories. Use this prompt:
   Classify each inspection finding as one of: 'Documentation Issue', 'Cargo Discrepancy', 'Security Concern', 'Regulatory Violation', 'Clean Inspection'. 

   SELECT report_id, inspection_type, 
          SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', 
            'Classify this CBSA inspection finding into exactly one category: Documentation Issue, Cargo Discrepancy, Security Concern, Regulatory Violation, or Clean Inspection. Return ONLY the category name. Finding: ' || findings_text
          ) as ai_classification,
          outcome, risk_score
   FROM CBSA_INSPECTION_REPORTS;

2. Use CORTEX.COMPLETE to extract structured key entities from 5 BILLS_OF_LADING_TEXT entries. Extract: shipper_name, consignee_name, port_of_loading, cargo_description, container_count as a JSON object.

Execute and show results.
```

---

> **12:10 - 12:55 PM | LUNCH**

---

# SESSION 7: Unstructured Data Extraction with Document AI
**12:55 - 1:25 PM | 30 min**

> *What we're building*: Using Snowflake's AI_EXTRACT and AI_PARSE_DOCUMENT functions to extract structured data from unstructured bill of lading text and inspection reports, simulating a document processing pipeline.

### Prompt 7.1 - Extract Structured Data from Bills of Lading

```
In PORT_AI_DEMO.PORT_OPS, use SNOWFLAKE.CORTEX.COMPLETE() to simulate document AI extraction on our BILLS_OF_LADING_TEXT table. For each of the first 10 documents:

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

Execute and show the extracted structured data.
```

### Prompt 7.2 - Build an Extraction Pipeline Table

```
In PORT_AI_DEMO.PORT_OPS:

1. Create a table called EXTRACTED_BOL_DATA that stores the flattened extracted fields from our bill of lading extraction. Use a CREATE TABLE AS SELECT that:
   - Runs the extraction on all BILLS_OF_LADING_TEXT rows
   - Flattens the JSON into individual columns: document_id, manifest_id, shipper_name, consignee_name, port_of_loading, port_of_discharge, vessel_name, cargo_description, gross_weight_kg, freight_terms, extraction_timestamp (CURRENT_TIMESTAMP)

2. Then compare the AI-extracted data against our original CONTAINER_MANIFESTS data by joining on manifest_id. Show any discrepancies between declared cargo in manifests vs extracted cargo descriptions.

Execute all SQL and show 10 rows from EXTRACTED_BOL_DATA plus the comparison results.
```

### Prompt 7.3 - Inspection Report Extraction

```
In PORT_AI_DEMO.PORT_OPS, create a table called EXTRACTED_INSPECTION_FINDINGS from CBSA_INSPECTION_REPORTS using SNOWFLAKE.CORTEX.COMPLETE to extract:

- report_id
- inspection_type
- items_inspected (array of items checked)
- discrepancies_found (array of issues)
- compliance_status (compliant, minor_violation, major_violation)  
- recommended_actions (array)
- estimated_resolution_days (number)
- risk_category (low, medium, high, critical)

Store these as properly typed columns (using TRY_PARSE_JSON where needed). Then run a summary query showing the distribution of risk_category and compliance_status across all reports.

Execute all SQL and show results.
```

---

# SESSION 8: Cortex Search & RAG Architecture Patterns
**1:25 - 1:55 PM | 30 min**

> *What we're building*: A Cortex Search service over port incident logs and marine safety reports, then a RAG (Retrieval Augmented Generation) pattern that retrieves relevant documents and generates contextual answers about port safety.

### Prompt 8.1 - Create Cortex Search Service

```
In PORT_AI_DEMO.PORT_OPS:

1. First, create a unified text table for search called PORT_KNOWLEDGE_BASE that combines:
   - PORT_INCIDENT_LOGS: incident_id as doc_id, 'incident_log' as doc_type, description_text || ' Resolution: ' || resolution_text as content, category as metadata_category, severity as metadata_priority, incident_date as doc_date
   - MARINE_SAFETY_REPORTS: report_id as doc_id, 'safety_report' as doc_type, report_text || ' Recommended: ' || recommended_actions as content, report_type as metadata_category, status as metadata_priority, report_date as doc_date
   - CBSA_INSPECTION_REPORTS: report_id as doc_id, 'inspection_report' as doc_type, findings_text as content, inspection_type as metadata_category, outcome as metadata_priority, inspection_date as doc_date

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE port_knowledge_search
     ON content
     ATTRIBUTES metadata_category, metadata_priority, doc_type
     WAREHOUSE = PORT_AI_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_category, metadata_priority, doc_date
       FROM PORT_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify the service is created by running SHOW CORTEX SEARCH SERVICES.
```

### Prompt 8.2 - Query the Search Service

```
In PORT_AI_DEMO.PORT_OPS, query our port_knowledge_search service using SEARCH_PREVIEW with these searches:

1. Search: "equipment failure crane" - show top 3 results
2. Search: "oil spill environmental" - show top 3 results  
3. Search: "customs cargo discrepancy" filtered to doc_type = 'inspection_report' - show top 3 results
4. Search: "winter storm weather delay" - show top 3 results

Use this pattern for each:
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'PORT_AI_DEMO.PORT_OPS.port_knowledge_search',
    '{
      "query": "<search_query>",
      "columns": ["doc_id", "doc_type", "content", "metadata_category"],
      "limit": 3
    }'
  )
)['results'] as results;

Execute all 4 searches and show results.
```

### Prompt 8.3 - RAG Pattern: Search + Generate

```
In PORT_AI_DEMO.PORT_OPS, implement a RAG pattern that:

1. Takes a user question: "What are the most common safety incidents at Vancouver port terminals and what preventive measures have been effective?"

2. First retrieves the top 5 most relevant documents from port_knowledge_search using SEARCH_PREVIEW

3. Then passes the retrieved context + question to SNOWFLAKE.CORTEX.COMPLETE() to generate a grounded answer:

WITH search_results AS (
    SELECT PARSE_JSON(
        SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
            'PORT_AI_DEMO.PORT_OPS.port_knowledge_search',
            '{
                "query": "common safety incidents terminals preventive measures",
                "columns": ["doc_id", "doc_type", "content", "metadata_category"],
                "limit": 5
            }'
        )
    )['results'] AS results
),
context AS (
    SELECT LISTAGG(r.value:content::STRING, '\n\n---\n\n') AS combined_context
    FROM search_results, LATERAL FLATTEN(input => results) r
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'You are a port safety expert at the Port of Vancouver. Based ONLY on the following source documents, answer the user question. Cite specific incidents by their doc_id when referencing findings. If the documents do not contain enough information, say so.

SOURCE DOCUMENTS:
' || combined_context || '

USER QUESTION: What are the most common safety incidents at Vancouver port terminals and what preventive measures have been effective?

Provide a structured answer with: 1) Common incident types, 2) Root causes, 3) Effective preventive measures, 4) Recommendations.'
) AS rag_response
FROM context;

Execute and show the RAG response.
```

---

# SESSION 9: Vector Embeddings Deep Dive
**1:55 - 2:15 PM | 20 min**

> *What we're building*: Understanding vector embeddings by generating them directly, building a custom similarity search, and visualizing embedding distances between different cargo types and incident categories.

### Prompt 9.1 - Generate and Compare Embeddings

```
In PORT_AI_DEMO.PORT_OPS:

1. Generate vector embeddings for 10 sample texts from different port domain areas using SNOWFLAKE.CORTEX.EMBED_TEXT_1024('snowflake-arctic-embed-l-v2.0', text):
   - 'Container ship delayed due to heavy fog in Burrard Inlet'
   - 'Crane malfunction at Deltaport Terminal berth 3'
   - 'Grain shipment temperature exceeded safe threshold'
   - 'CBSA inspection found undeclared electronics in container'
   - 'Oil sheen detected near Neptune Terminals'
   - 'Truck queue time at Deltaport exceeded 3 hours'
   - 'CN Rail intermodal train delayed due to track maintenance near Kamloops'
   - 'Cruise ship Princess Marguerite arriving Canada Place'
   - 'Container vessel MSC Rosaria requesting emergency berth allocation'
   - 'Potash export shipment scheduled for Roberts Bank terminal'

2. Store these in a table called EMBEDDING_EXAMPLES with columns: text_id, text_content, embedding (VECTOR(FLOAT, 1024)), category (weather, equipment, safety, customs, environmental, logistics, rail, cruise, operations, export)

3. Then compute the cosine similarity between ALL pairs and show the top 10 most similar pairs and the top 5 least similar pairs using VECTOR_COSINE_SIMILARITY().

Execute all SQL and show results.
```

### Prompt 9.2 - Semantic Search with Custom Embeddings

```
In PORT_AI_DEMO.PORT_OPS, build a custom semantic search using our embeddings:

1. Generate embeddings for all PORT_INCIDENT_LOGS description_text entries and store in a table called INCIDENT_EMBEDDINGS (incident_id, description_text, embedding VECTOR(FLOAT, 1024))

2. Write a semantic search query that takes the user query "What incidents involved environmental contamination or spills?" and:
   - Generates an embedding for the query text
   - Computes cosine similarity against all incident embeddings
   - Returns the top 5 most semantically similar incidents with their similarity scores

3. Compare this to a simple ILIKE keyword search for '%spill%' OR '%contamination%' OR '%environmental%' on the same data. Show which incidents the vector search found that keyword search missed, and vice versa.

Execute all SQL and show the comparison.
```

---

> **2:15 - 2:30 PM | BREAK**

---

# SESSION 10: Cortex Analyst: Natural Language to SQL
**2:30 - 2:55 PM | 25 min**

> *What we're building*: A semantic model YAML file that describes our port operations data, then using Cortex Analyst to convert natural language questions into SQL queries automatically.

### Prompt 10.1 - Create the Semantic Model

```
Create a Cortex Analyst semantic model YAML file for our Port of Vancouver data. Save it to a Snowflake stage.

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

Execute all SQL and show confirmation.
```

### Prompt 10.2 - Query with Natural Language

```
Using the semantic model we just created at @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml, ask Cortex Analyst these natural language questions and show both the generated SQL and the results:

1. "What are the top 5 terminals by total TEU volume?"
2. "Show me monthly container arrivals for 2025 with the busiest months highlighted"
3. "Which cargo categories have the highest average declared value?"
4. "What percentage of CBSA declarations are still pending by shipping line?"
5. "Compare CN Rail vs CP Rail on-time performance to Calgary"
```

### Prompt 10.3 - Advanced Analyst Queries

```
Ask Cortex Analyst these more complex questions using our semantic model at @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml:

1. "What is the correlation between container count and berth time delays? Are larger shipments more likely to cause congestion?"
2. "Show the seasonal pattern of trade - which months have the highest total cargo value and how does it compare to crane utilization?"
3. "Which consignee cities receive the most valuable shipments and via which terminals?"
```

---

# SESSION 11: AI-Generated Semantic Models
**2:55 - 3:15 PM | 20 min**

> *What we're building*: Using Cortex to auto-generate and iterate on semantic model definitions, showing how AI can bootstrap the creation of semantic layers.

### Prompt 11.1 - Auto-Generate a Semantic Model

```
In PORT_AI_DEMO.PORT_OPS, I want to auto-generate an improved semantic model. 

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

Execute and show the generated model.
```

### Prompt 11.2 - Validate and Test the Generated Model

```
Test the AI-generated semantic model (v2) by asking Cortex Analyst these questions using @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model_v2.yaml:

1. "What is the average truck queue wait time during peak hours vs off-peak?"
2. "Show crane utilization rates by terminal and shift"
3. "Which terminals have the best ratio of estimated vs actual berth times?"

Compare the quality of SQL generated vs our manually-created model from Session 10. Note any differences in query accuracy.
```

---

# SESSION 12: Building Agentic Systems with Cortex Agent API
**3:15 - 3:45 PM | 30 min**

> *What we're building*: A Cortex Agent that combines Cortex Analyst (for structured data queries) and Cortex Search (for unstructured document retrieval) into a single conversational interface for port operations staff.

### Prompt 12.1 - Create the Cortex Agent

```
In PORT_AI_DEMO.PORT_OPS, create a Cortex Agent that port operations staff can use to ask questions about both structured data and unstructured documents.

1. First, ensure we have both tools ready:
   - Cortex Analyst semantic model at @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml
   - Cortex Search service: port_knowledge_search

2. Create the agent using SQL:

CREATE OR REPLACE AGENT PORT_AI_DEMO.PORT_OPS.PORT_OPS_AGENT
  MODEL = 'claude-3-5-sonnet'
  TOOLS = (
    PORT_AI_DEMO.PORT_OPS.port_knowledge_search,
    @PORT_AI_DEMO.PORT_OPS.SEMANTIC_MODELS/port_operations_model.yaml
  )
  INSTRUCTIONS = 'You are the Port of Vancouver Operations Assistant. You help port staff, terminal operators, customs officers, and logistics coordinators with questions about:
- Container shipping volumes, berth times, and cargo data (use the structured data tool)
- Safety incidents, inspection reports, and marine safety documents (use the search tool)
- Trade patterns and logistics coordination

Always be specific with numbers and cite your sources. When discussing safety issues, emphasize preventive measures. Support both English and French queries as this is a Canadian federal port.

Key context: The Port of Vancouver is Canadas largest port, handling over $200B in annual trade. Key terminals include Deltaport, Vanterm, and Centerm for containers, and Roberts Bank for bulk cargo.'
  SAMPLE_QUESTIONS = (
    'What were the top incidents at Deltaport this year?',
    'Show me total TEU volume by shipping line for Q4 2025',
    'Are there any CBSA inspection reports with major discrepancies?',
    'Quel est le volume total de conteneurs pour le terminal Centerm?'
  );

Execute and show confirmation.
```

### Prompt 12.2 - Test the Agent with Mixed Queries

```
Test our PORT_OPS_AGENT in PORT_AI_DEMO.PORT_OPS with a series of questions that exercise both tools. Run each as a separate agent interaction:

1. Structured data query: "What are the busiest terminals by TEU count this year and which shipping lines dominate each terminal?"

2. Unstructured search query: "Have there been any environmental incidents near Neptune Terminals? What was done about them?"

3. Mixed query: "Which terminals have had both the highest cargo volume AND the most safety incidents? Is there a correlation?"

4. Bilingual query: "Quels sont les principaux problemes de securite signales au port cette annee?"

For each, show the agent's response and note which tools it chose to use.
```

### Prompt 12.3 - Agent with Custom Tool

```
In PORT_AI_DEMO.PORT_OPS, enhance our agent by adding a custom tool. 

1. Create a UDF that calculates estimated port congestion risk:

CREATE OR REPLACE FUNCTION PORT_AI_DEMO.PORT_OPS.CALCULATE_CONGESTION_RISK(
    terminal_name VARCHAR,
    teu_count NUMBER,
    arrival_month NUMBER
)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
    SELECT OBJECT_CONSTRUCT(
        'terminal', terminal_name,
        'teu_count', teu_count,
        'risk_score', 
            CASE 
                WHEN arrival_month IN (10,11,12) AND teu_count > 1000 THEN 'HIGH'
                WHEN arrival_month IN (10,11,12) OR teu_count > 1000 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
        'recommendation',
            CASE 
                WHEN arrival_month IN (10,11,12) AND teu_count > 1000 THEN 'Pre-allocate additional berth slots and crane resources'
                WHEN arrival_month IN (10,11,12) OR teu_count > 1000 THEN 'Monitor queue times and prepare standby resources'
                ELSE 'Standard operations'
            END
    )
$$;

2. Test the UDF with sample inputs.

3. Create an updated agent that includes this custom tool alongside the existing tools.

Execute all SQL and test the updated agent with: "What is the congestion risk for a 2000 TEU shipment arriving at Deltaport in November?"
```

---

# SESSION 13: Deploying AI Apps with Streamlit
**3:45 - 4:05 PM | 20 min**

> *What we're building*: A Streamlit in Snowflake application that provides a unified operations dashboard with a chat interface powered by our Cortex Agent, real-time congestion scores, and key port metrics.

### Prompt 13.1 - Create the Streamlit App

```
Create a Streamlit in Snowflake app called PORT_OPS_DASHBOARD in PORT_AI_DEMO.PORT_OPS that provides:

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

Create the Streamlit app using SQL (CREATE STREAMLIT) and write the Python code.
```

### Prompt 13.2 - Test the Streamlit App

```
Show me the SQL to verify the Streamlit app was created:

1. SHOW STREAMLITS IN SCHEMA PORT_AI_DEMO.PORT_OPS;
2. Describe the streamlit PORT_OPS_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight.
```

---

# SESSION 14: AI Observability, Monitoring & Cost Optimization
**4:05 - 4:30 PM | 25 min**

> *What we're building*: Monitoring dashboards for our AI workloads - tracking Cortex function usage, credit consumption, model accuracy over time, and search service health.

### Prompt 14.1 - Monitor AI Function Usage

```
In PORT_AI_DEMO.PORT_OPS, run these observability queries:

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

Execute all queries and show results.
```

### Prompt 14.2 - Cost Optimization Analysis

```
In PORT_AI_DEMO.PORT_OPS, analyze our workshop's AI cost footprint:

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

Show the cost analysis and AI-generated optimization recommendations.
```

### Prompt 14.3 - Workshop Summary Query

```
In PORT_AI_DEMO.PORT_OPS, create a final summary of everything we built today:

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

Execute and show the complete inventory.
```

---

# WRAP-UP & CLEANUP

> **4:30 - 4:40 PM**

### Optional: Cleanup Prompt

```
If you want to clean up all workshop resources, run:

DROP DATABASE PORT_AI_DEMO;
DROP WAREHOUSE PORT_AI_WH;
DROP ROLE PORT_DATA_ENGINEER;
DROP ROLE PORT_DATA_SCIENTIST;
DROP ROLE PORT_ANALYST;
DROP ROLE PORT_CUSTOMS_OFFICER;

-- Only run this if you want to remove everything!
```

---

# Quick Reference: Session-to-Prompt Map

| Session | Time | Topic | Prompts | What's Created |
|---------|------|-------|---------|----------------|
| 1 | 9:15-9:45 | AI/ML with End in Mind | 1.1, 1.2 | Database, schema, warehouse, reference tables |
| 2 | 9:45-10:15 | Data Prep & Feature Eng. | 2.1-2.4 | 12 operational data tables (structured, time-series, unstructured, geospatial) |
| 3 | 10:15-10:40 | Security & Governance | 3.1-3.3 | 4 roles, masking policies, sensitivity tags |
| 4 | 10:55-11:25 | Snowpark ML & Models | 4.1-4.3 | Feature view, ML classification model, evaluation metrics |
| 5 | 11:25-11:45 | Dynamic Tables for Inference | 5.1-5.2 | Dynamic table for live congestion scoring |
| 6 | 11:45-12:10 | Cortex LLM Functions | 6.1-6.3 | Sentiment, translate, summarize, classify, model comparison |
| 7 | 12:55-1:25 | Document AI Extraction | 7.1-7.3 | Extracted BOL data table, inspection findings table |
| 8 | 1:25-1:55 | Cortex Search & RAG | 8.1-8.3 | Knowledge base table, Cortex Search service, RAG query |
| 9 | 1:55-2:15 | Vector Embeddings | 9.1-9.2 | Embedding examples table, semantic search comparison |
| 10 | 2:30-2:55 | Cortex Analyst | 10.1-10.3 | Semantic model YAML, natural language queries |
| 11 | 2:55-3:15 | AI-Generated Semantic Models | 11.1-11.2 | Auto-generated semantic model v2, validation |
| 12 | 3:15-3:45 | Cortex Agent API | 12.1-12.3 | Agent with Analyst + Search + custom tool |
| 13 | 3:45-4:05 | Streamlit App | 13.1-13.2 | 3-page operations dashboard app |
| 14 | 4:05-4:30 | Observability & Cost | 14.1-14.3 | Usage monitoring, cost analysis, workshop inventory |

---

**Total Prompts: 33**
**Total Time: ~6 hours of hands-on content**
**Scenario: Port of Vancouver - Canada's Pacific Gateway ($200B annual trade)**
