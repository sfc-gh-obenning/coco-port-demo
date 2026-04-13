import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(9, "Vector Embeddings Deep Dive", "1:55 - 2:15 PM", "20 min", "Custom embeddings, similarity search, and vector vs keyword comparison")

render_technologies_used([
    {"name": "EMBED_TEXT_1024()", "description": "Generates a 1024-dimensional vector embedding for text input using a specified model. The embedding captures the semantic meaning of the text as a point in high-dimensional space.", "icon": "scatter_plot"},
    {"name": "VECTOR Data Type", "description": "Snowflake's native vector data type. VECTOR(FLOAT, 1024) stores 1024 floating-point numbers. Supports similarity operations directly in SQL.", "icon": "data_array"},
    {"name": "VECTOR_COSINE_SIMILARITY()", "description": "Computes the cosine similarity between two vectors. Returns a value between -1 and 1, where 1 means identical direction (most similar) and 0 means orthogonal (unrelated).", "icon": "compare"},
])


PROMPT_9_1 = """In PORT_AI_DEMO.PORT_OPS:

1. Generate vector embeddings for 18 sample texts using SNOWFLAKE.CORTEX.EMBED_TEXT_1024('snowflake-arctic-embed-l-v2.0', text). Include deliberately similar pairs so we can see high cosine similarity scores:

   Weather delays (similar pair):
   - 'Container ship delayed due to heavy fog in Burrard Inlet'
   - 'Vessel arrival postponed because of dense fog conditions in Burrard Inlet'

   Equipment failures (similar pair):
   - 'Crane malfunction at Deltaport Terminal berth 3'
   - 'Gantry crane mechanical failure reported at Deltaport berth 3'

   Environmental incidents (similar pair):
   - 'Oil sheen detected near Neptune Terminals'
   - 'Petroleum slick observed on water surface adjacent to Neptune Terminals'

   Customs inspections (similar pair):
   - 'CBSA inspection found undeclared electronics in container'
   - 'Canada Border Services Agency discovered unreported electronic goods during container examination'

   Rail logistics (similar pair):
   - 'CN Rail intermodal train delayed due to track maintenance near Kamloops'
   - 'CN intermodal freight train held up by rail track repairs in the Kamloops area'

   Dissimilar texts (no close match to the above):
   - 'Grain shipment temperature exceeded safe threshold'
   - 'Truck queue time at Deltaport exceeded 3 hours'
   - 'Cruise ship Princess Marguerite arriving Canada Place'
   - 'Container vessel MSC Rosaria requesting emergency berth allocation'
   - 'Potash export shipment scheduled for Roberts Bank terminal'
   - 'New collective bargaining agreement ratified by ILWU Local 514'
   - 'Quarterly safety drill conducted across all Burrard Inlet terminals'
   - 'Annual dredging of Second Narrows shipping channel completed'

2. Store these in a table called EMBEDDING_EXAMPLES with columns: text_id, text_content, embedding (VECTOR(FLOAT, 1024)), category (weather, equipment, environmental, customs, rail, safety, logistics, cruise, operations, export, labour, maintenance)

3. Then compute the cosine similarity between ALL pairs and show the top 10 most similar pairs and the top 5 least similar pairs using VECTOR_COSINE_SIMILARITY().

Execute all SQL and show results."""

render_prompt("Prompt 9.1", "Generate and Compare Embeddings", PROMPT_9_1)

render_explanation("What this prompt does", """
This hands-on exercise builds **intuition for how vector embeddings work**:

**Generating embeddings**:
```sql
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_1024(
  'snowflake-arctic-embed-l-v2.0',
  'Container ship delayed due to heavy fog in Burrard Inlet'
) AS embedding;
```
This returns a VECTOR(FLOAT, 1024) - an array of 1024 floating-point numbers that encodes the semantic meaning of the text.

**What makes embeddings powerful**: Texts with similar meanings get similar vectors, even if they use completely different words. For example:
- "Container ship delayed due to fog" and "Vessel arrival postponed by weather"  would have HIGH similarity
- "Container ship delayed due to fog" and "Potash export scheduled" would have LOW similarity

**Pairwise comparison** with VECTOR_COSINE_SIMILARITY:
```sql
SELECT
  a.text_content AS text_a,
  b.text_content AS text_b,
  VECTOR_COSINE_SIMILARITY(a.embedding, b.embedding) AS similarity
FROM EMBEDDING_EXAMPLES a
CROSS JOIN EMBEDDING_EXAMPLES b
WHERE a.text_id < b.text_id
ORDER BY similarity DESC
LIMIT 10;
```

**Expected high-similarity pairs** (these are the deliberately paired texts):
- Fog delay pair (~0.95+): "Container ship delayed due to heavy fog..." vs "Vessel arrival postponed because of dense fog..."
- Crane failure pair (~0.93+): "Crane malfunction at Deltaport..." vs "Gantry crane mechanical failure..."
- Oil spill pair (~0.94+): "Oil sheen detected..." vs "Petroleum slick observed..."
- Customs pair (~0.90+): "CBSA inspection found undeclared electronics..." vs "Canada Border Services Agency discovered unreported electronic goods..."
- Rail delay pair (~0.95+): "CN Rail intermodal train delayed..." vs "CN intermodal freight train held up..."

**Expected moderate-similarity pairs**:
- Cross-category matches like fog delay + rail delay (both about transport delays, ~0.6-0.7)

**Expected low-similarity pairs**:
- "New collective bargaining agreement ratified..." vs "Oil sheen detected..." (~0.3 or lower)
- Cruise ship arrival vs annual dredging (completely different domains)

This exercise demonstrates that embeddings capture **semantic relationships**, not just lexical overlap. Paraphrased sentences score nearly as high as identical text.
""")


PROMPT_9_2 = """In PORT_AI_DEMO.PORT_OPS, build a custom semantic search using our embeddings:

1. Generate embeddings for all PORT_INCIDENT_LOGS description_text entries and store in a table called INCIDENT_EMBEDDINGS (incident_id, description_text, embedding VECTOR(FLOAT, 1024))

2. Write a semantic search query that takes the user query "What incidents involved environmental contamination or spills?" and:
   - Generates an embedding for the query text
   - Computes cosine similarity against all incident embeddings
   - Returns the top 5 most semantically similar incidents with their similarity scores

3. Compare this to a simple ILIKE keyword search for '%spill%' OR '%contamination%' OR '%environmental%' on the same data. Show which incidents the vector search found that keyword search missed, and vice versa.

Execute all SQL and show the comparison."""

render_prompt("Prompt 9.2", "Semantic Search with Custom Embeddings", PROMPT_9_2)

render_explanation("What this prompt does", """
A direct comparison between **semantic (vector) search** and **keyword search**:

**Custom semantic search**:
```sql
WITH query_embedding AS (
  SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_1024(
    'snowflake-arctic-embed-l-v2.0',
    'What incidents involved environmental contamination or spills?'
  ) AS qe
)
SELECT
  i.incident_id, i.description_text,
  VECTOR_COSINE_SIMILARITY(i.embedding, q.qe) AS similarity
FROM INCIDENT_EMBEDDINGS i, query_embedding q
ORDER BY similarity DESC LIMIT 5;
```

**Keyword search**:
```sql
SELECT incident_id, description_text
FROM PORT_INCIDENT_LOGS
WHERE description_text ILIKE '%spill%'
   OR description_text ILIKE '%contamination%'
   OR description_text ILIKE '%environmental%';
```

**What the comparison reveals**:
- **Vector search finds**: Incidents about "discharge," "sheen," "pollution," "hazardous material leak" that don't contain the keywords "spill" or "contamination"
- **Keyword search finds**: Every mention of those exact words, including false positives (e.g., "no contamination was found")
- **Overlap**: Incidents that both methods find

This is precisely why Cortex Search uses **hybrid search** - combining both approaches gets the best results.

**This is the foundation of Session 8**: Cortex Search does all of this automatically. This session shows you what's happening under the hood.
""")


render_key_concepts([
    {"term": "Vector Embedding", "definition": "A fixed-size array of floating-point numbers that represents text in a high-dimensional space. Semantically similar texts are mapped to nearby points. Created by embedding models trained on large text corpora."},
    {"term": "Cosine Similarity", "definition": "Measures the angle between two vectors. Values range from -1 to 1. Score of 1.0 = identical direction (maximally similar), 0.0 = orthogonal (unrelated), -1.0 = opposite direction. The standard metric for comparing text embeddings."},
    {"term": "VECTOR(FLOAT, 1024)", "definition": "Snowflake's native vector data type storing 1024 floating-point dimensions. First-class data type that supports similarity functions, storage, and indexing natively in the database."},
    {"term": "Semantic vs Keyword Search", "definition": "Keyword search matches exact text patterns (LIKE/ILIKE). Semantic search matches meaning by comparing vector embeddings. Keyword catches exact terms; semantic catches synonyms and related concepts. Hybrid search combines both."},
])

render_domain_glossary([
    {"term": "AIS (Automatic Identification System)", "definition": "A maritime tracking system that broadcasts vessel identity, position, speed, and course via VHF radio. All commercial vessels are required to transmit AIS data — this powers the GPS tracking data in our scenario."},
    {"term": "Roberts Bank", "definition": "A causeway-connected terminal complex south of Vancouver. Home to Deltaport (containers) and Westshore Terminals (coal). Separate from the Burrard Inlet terminals."},
])

render_what_you_built([
    "EMBEDDING_EXAMPLES table with 18 domain-specific embeddings",
    "Pairwise similarity matrix showing semantic relationships",
    "INCIDENT_EMBEDDINGS table for all incident logs",
    "Custom semantic search implementation from scratch",
    "Side-by-side comparison of vector vs keyword search results",
])
