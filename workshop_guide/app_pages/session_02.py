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
    session_num=2,
    title="Preparing Data for AI & Feature Engineering",
    time_range="9:45 - 10:15 AM",
    duration="30 min",
    building="12 operational data tables covering structured, time-series, unstructured, and geospatial data",
)

render_technologies_used([
    {"name": "Structured Data Tables", "description": "Traditional relational tables with typed columns, foreign keys, and constraints. These are the backbone of operational analytics.", "icon": "table_chart"},
    {"name": "Time-Series Data", "description": "Sensor readings, GPS pings, and metrics with timestamps. Snowflake handles time-series natively with TIMESTAMP types and window functions.", "icon": "timeline"},
    {"name": "Semi-Structured Text", "description": "Long-form text stored in VARCHAR columns. This unstructured data will be processed by Cortex LLM functions and Cortex Search in later sessions.", "icon": "article"},
])


PROMPT_2_1 = """In PORT_AI_DEMO.PORT_OPS, create and populate these structured operational tables with realistic synthetic data:

1. CONTAINER_MANIFESTS - 200 rows of container shipping manifests. Columns: manifest_id, vessel_id (FK to VESSELS), voyage_number, bill_of_lading_number, container_count, teu_count, origin_port (Asian ports like Shanghai, Busan, Yokohama, Hong Kong, Singapore, Kaohsiung), destination_terminal (FK to TERMINALS), cargo_category (electronics, automotive parts, textiles, machinery, consumer goods, furniture, chemicals), declared_value_cad, weight_tonnes, cbsa_declaration_status (cleared, pending, held_for_inspection, released), arrival_date (between 2025-01-01 and 2026-04-06), estimated_berth_time_hours, actual_berth_time_hours. Make arrival patterns heavier in Oct-Dec (peak Asia-Pacific trade season).

2. CARGO_INVOICES - 300 rows of commercial invoices tied to manifests. Columns: invoice_id, manifest_id (FK), shipper_name, consignee_name, consignee_city (Canadian cities: Vancouver, Calgary, Edmonton, Toronto, Montreal, Saskatoon, Winnipeg, Surrey, Richmond), commodity_hs_code, commodity_description, quantity, unit_price_cad, total_value_cad, currency_original, exchange_rate, payment_terms, invoice_date.

3. RAIL_SCHEDULES - 150 rows of CN/CP Rail intermodal schedules. Columns: schedule_id, railway (CN or CP), train_number, origin_terminal (Vancouver terminals), destination_city (Calgary, Edmonton, Saskatoon, Regina, Winnipeg, Toronto, Montreal), departure_datetime, estimated_arrival_datetime, actual_arrival_datetime, num_containers, num_rail_cars, cargo_type, status (scheduled, in_transit, arrived, delayed), delay_reason (NULL, weather, track_maintenance, congestion, mechanical).

Execute all SQL to create and populate these tables."""

render_prompt("Prompt 2.1", "Structured Operational Data", PROMPT_2_1)

render_explanation("What this prompt does", """
This creates three core **fact tables** that represent the operational heart of port logistics:

- **CONTAINER_MANIFESTS**: The central fact table. Each row is a shipment arriving at the port. The `vessel_id` and `destination_terminal` columns create relationships to our Session 1 dimension tables. The `arrival_date` distribution is intentionally skewed toward Q4 to simulate peak Asia-Pacific trade season.

- **CARGO_INVOICES**: Commercial invoices linked to manifests. The many-to-one relationship (multiple invoices per manifest) is typical of real trade where a single container ship carries goods for many different buyers.

- **RAIL_SCHEDULES**: Intermodal rail connections. After cargo is unloaded at Vancouver terminals, it moves inland by rail. CN and CP are Canada's two major railways.

**Why this matters for AI/ML**: These tables provide the structured features we'll use in Session 4 for ML model training (predicting congestion). The `actual_berth_time_hours` vs `estimated_berth_time_hours` gap becomes our prediction target.

**Data modeling pattern**: This follows a **star schema** design - CONTAINER_MANIFESTS is the central fact table, with VESSELS, TERMINALS, and TRADE_PARTNERS as dimension tables. This is the most common pattern for analytical workloads in Snowflake.
""")


PROMPT_2_2 = """In PORT_AI_DEMO.PORT_OPS, create and populate these time-series tables:

1. CONTAINER_GPS_TRACKING - 500 rows of GPS pings for containers moving through Burrard Inlet and to distribution centers. Columns: tracking_id, container_id, manifest_id, timestamp (every 15 min intervals over the past 30 days), latitude (range: 49.15 to 49.35 for Vancouver/Burrard Inlet area), longitude (range: -123.30 to -122.90), speed_knots, status (at_sea, anchored, berthed, on_truck, on_rail, at_warehouse), location_description (Burrard Inlet, English Bay Anchorage, Deltaport, Surrey Distribution Center, Richmond Warehouse, CN Intermodal Yard).

2. CRANE_UTILIZATION - 400 rows of crane metrics at container terminals. Columns: metric_id, terminal_id, crane_id, timestamp (hourly over past 14 days), moves_per_hour, utilization_pct (0-100), idle_time_minutes, container_lifts, status (operating, idle, maintenance), operator_shift (day, evening, night).

3. TRUCK_QUEUE_TIMES - 300 rows at Deltaport truck gate. Columns: queue_id, terminal_id, timestamp (every 30 min over past 14 days), trucks_in_queue, avg_wait_minutes, max_wait_minutes, gate_lanes_open, weather_condition (clear, rain, fog, snow), is_peak_hour BOOLEAN.

4. CARGO_TEMPERATURE_SENSORS - 200 rows for temperature-sensitive shipments (grain, potash, perishables). Columns: sensor_id, container_id, cargo_type (grain, potash, frozen_seafood, fresh_produce, pharmaceuticals), timestamp, temperature_celsius, humidity_pct, acceptable_range_min, acceptable_range_max, alert_triggered BOOLEAN.

Execute all SQL."""

render_prompt("Prompt 2.2", "Time-Series Sensor and Tracking Data", PROMPT_2_2)

render_explanation("What this prompt does", """
This creates four **time-series tables** representing IoT and operational sensor data:

- **CONTAINER_GPS_TRACKING**: Simulates AIS (Automatic Identification System) data and inland tracking. The coordinates cover the real geographic area from the Strait of Georgia through Burrard Inlet to inland distribution centers.

- **CRANE_UTILIZATION**: Operational metrics from ship-to-shore (STS) gantry cranes. Moves-per-hour is a key KPI - top ports achieve 30+ moves/hour. We'll use this in Session 10 when expanding our semantic view.

- **TRUCK_QUEUE_TIMES**: Gate metrics at Deltaport, which is one of the most congested container terminals in North America. Truck queues directly impact supply chain costs.

- **CARGO_TEMPERATURE_SENSORS**: Cold chain monitoring for perishables and bulk commodity quality. The `alert_triggered` flag indicates when temperatures go outside acceptable ranges.

**Time-series in Snowflake**: Snowflake doesn't have a dedicated time-series engine, but it handles time-series workloads well through:
- Automatic micro-partition pruning on timestamp columns
- Window functions (`LAG`, `LEAD`, `MOVING_AVG`) for temporal analysis
- `TIME_SLICE` function for bucketing timestamps into intervals
""")


PROMPT_2_3 = """In PORT_AI_DEMO.PORT_OPS, create and populate these unstructured/text data tables:

1. BILLS_OF_LADING_TEXT - 30 rows simulating extracted text from bill of lading documents. Columns: document_id, manifest_id, raw_text (generate realistic multi-paragraph bill of lading text including shipper, consignee, notify party, port of loading, port of discharge, description of goods, container numbers, weight, measurement, freight terms, date), extraction_date, document_type.

2. CBSA_INSPECTION_REPORTS - 25 rows of Canada Border Services Agency inspection reports. Columns: report_id, manifest_id, inspection_date, inspector_id, inspection_type (routine, targeted, random, referred), findings_text (detailed paragraph about inspection findings - some clean, some with discrepancies in declared vs actual cargo, some with documentation issues), risk_score (1-10), outcome (released, detained, re_exported, penalty_assessed), penalty_amount_cad.

3. PORT_INCIDENT_LOGS - 40 rows of Port Authority incident/safety logs. Columns: incident_id, incident_date, terminal_id, severity (low, medium, high, critical), category (safety, environmental, security, equipment, weather, marine), description_text (detailed paragraph about each incident - spills, equipment failures, weather delays, security alerts, marine incidents in the Burrard Inlet), resolution_text, days_to_resolve.

4. SHIPPING_PARTNER_EMAILS - 35 rows of email correspondence. Columns: email_id, from_company, to_company, subject, email_body (realistic email text about shipping delays, customs issues, rate negotiations, schedule changes, storm warnings - some in English, some in French for bilingual content), sent_date, category (operations, customs, commercial, weather_alert, scheduling), language (en, fr).

5. MARINE_SAFETY_REPORTS - 20 rows. Columns: report_id, vessel_id, report_date, report_type (navigation, pollution, accident, near_miss, weather), location_description, report_text (detailed safety narrative), recommended_actions, status (open, investigating, closed).

Make sure the text fields contain substantial, realistic content (at least 100 words each). Execute all SQL."""

render_prompt("Prompt 2.3", "Unstructured Text Data for AI", PROMPT_2_3)

render_explanation("What this prompt does", """
This creates five tables of **unstructured text data** - the raw material for Cortex LLM functions, Document AI extraction, Cortex Search, and RAG pipelines:

- **BILLS_OF_LADING_TEXT**: Simulates OCR output from scanned shipping documents. In production, you'd use Snowflake's `AI_PARSE_DOCUMENT` to extract text from actual PDFs stored in a stage.

- **CBSA_INSPECTION_REPORTS**: Canada Border Services Agency inspection findings. These contain free-form text that we'll classify, extract entities from, and search in later sessions.

- **PORT_INCIDENT_LOGS**: Safety and operations incidents. These power our Cortex Search service in Session 8 and RAG pipeline for safety Q&A.

- **SHIPPING_PARTNER_EMAILS**: Includes **bilingual content** (English/French) to demonstrate Cortex translation capabilities. Canada's Official Languages Act requires federal ports to operate bilingually.

- **MARINE_SAFETY_REPORTS**: Vessel safety narratives that we'll use for semantic search and embedding comparisons.

**Why text data matters for AI**: Traditional BI only works with structured data. Modern AI can extract insights from text, classify documents, answer questions from document collections, and detect sentiment - all capabilities we'll build in Sessions 6-9.
""")


PROMPT_2_4 = """Run a query in PORT_AI_DEMO.PORT_OPS that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 2.4", "Verify All Data Tables", PROMPT_2_4)

render_explanation("What this prompt does", """
A quick verification query. Cortex Code will generate something like:

```sql
SELECT table_name, row_count
FROM PORT_AI_DEMO.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'PORT_OPS'
  AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;
```

**`INFORMATION_SCHEMA`** is a standard SQL schema available in every Snowflake database that provides metadata about all objects. The `TABLES` view shows row counts, creation dates, sizes, and more. This is a quick way to audit your data landscape.

You should see approximately **2,400+ total rows** across 12+ tables.
""")


render_key_concepts([
    {"term": "Star Schema", "definition": "A data modeling pattern with a central fact table (CONTAINER_MANIFESTS) surrounded by dimension tables (VESSELS, TERMINALS, TRADE_PARTNERS). Fact tables contain measures and foreign keys; dimension tables contain descriptive attributes. This is the dominant pattern in data warehousing."},
    {"term": "INFORMATION_SCHEMA.TABLES", "definition": "A standard SQL view available in every Snowflake database that provides metadata about all objects — row counts, creation dates, byte sizes, and more. Used to audit and verify data loading."},
    {"term": "Time-series in Snowflake", "definition": "Snowflake handles time-series natively through automatic micro-partition pruning on timestamp columns, window functions (LAG, LEAD, MOVING_AVG), and TIME_SLICE for bucketing timestamps into intervals."},
])

render_domain_glossary([
    {"term": "TEU (Twenty-foot Equivalent Unit)", "definition": "The standard unit for counting container capacity. A standard 20-foot shipping container = 1 TEU. A 40-foot container = 2 TEU. The Port of Vancouver handles about 3.5 million TEUs annually."},
    {"term": "CBSA", "definition": "Canada Border Services Agency — the federal agency responsible for border security, customs, and immigration. All imported cargo must clear CBSA before being released."},
    {"term": "HS Code", "definition": "Harmonized System code — an international standard for classifying traded goods. The first 6 digits are universal; additional digits are country-specific. Used in cargo invoices for customs classification."},
    {"term": "Burrard Inlet", "definition": "The body of water that forms Vancouver's harbour. Ships transit through First Narrows (under Lions Gate Bridge) to reach container terminals at Vanterm, Centerm, and bulk terminals at Neptune."},
    {"term": "CN / CP Rail", "definition": "Canada's two Class I railways. Both operate intermodal terminals in Vancouver, moving containers from the port to inland destinations across western and central Canada."},
])

render_what_you_built([
    "CONTAINER_MANIFESTS - 200 shipping manifests with seasonal patterns",
    "CARGO_INVOICES - 300 commercial invoices linked to manifests",
    "RAIL_SCHEDULES - 150 CN/CP Rail intermodal schedules",
    "CONTAINER_GPS_TRACKING - 500 GPS pings for container movement",
    "CRANE_UTILIZATION - 400 hourly crane performance metrics",
    "TRUCK_QUEUE_TIMES - 300 truck gate queue measurements",
    "CARGO_TEMPERATURE_SENSORS - 200 cold chain sensor readings",
    "BILLS_OF_LADING_TEXT - 30 bill of lading documents",
    "CBSA_INSPECTION_REPORTS - 25 customs inspection reports",
    "PORT_INCIDENT_LOGS - 40 safety/operations incident logs",
    "SHIPPING_PARTNER_EMAILS - 35 bilingual email correspondence",
    "MARINE_SAFETY_REPORTS - 20 marine safety narratives",
])
