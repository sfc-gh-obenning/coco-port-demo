import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(6, "Cortex LLM Functions & Model Comparison", "11:45 AM - 12:10 PM", "25 min", "Sentiment analysis, translation, summarization, classification, and model comparison")

render_technologies_used([
    {"name": "CORTEX.SENTIMENT()", "description": "Returns a sentiment score between -1 (negative) and 1 (positive) for text input. Runs as a simple SQL function - no model deployment needed.", "icon": "sentiment_satisfied"},
    {"name": "CORTEX.SUMMARIZE()", "description": "Generates concise summaries of long text. Useful for reducing verbose incident reports or documents to key points.", "icon": "summarize"},
    {"name": "CORTEX.TRANSLATE()", "description": "Translates text between languages. Supports 12+ languages. Perfect for Canada's bilingual requirements.", "icon": "translate"},
    {"name": "CORTEX.COMPLETE()", "description": "The most flexible Cortex function. Sends a prompt to any supported LLM model and returns the response. Supports model selection for quality/cost tradeoffs.", "icon": "psychology"},
])


PROMPT_6_1 = """In PORT_AI_DEMO.PORT_OPS, run the following Cortex LLM function queries:

1. SENTIMENT ANALYSIS: Run SNOWFLAKE.CORTEX.SENTIMENT() on the email_body column of SHIPPING_PARTNER_EMAILS. Show the email subject, from_company, category, and sentiment score for all rows. Order by sentiment score ascending (most negative first).

2. SUMMARIZATION: Run SNOWFLAKE.CORTEX.SUMMARIZE() on the 5 longest PORT_INCIDENT_LOGS description_text entries. Show incident_id, severity, category, and the summarized text.

3. TRANSLATION: Find all French emails in SHIPPING_PARTNER_EMAILS (where language='fr') and use SNOWFLAKE.CORTEX.TRANSLATE(email_body, 'fr', 'en') to translate them to English. Show original subject, original body (first 200 chars), and translated text.

Execute all three queries and show results."""

render_prompt("Prompt 6.1", "Sentiment, Summarize, Translate", PROMPT_6_1)

render_explanation("What this prompt does", """
Three Cortex AI SQL functions in action:

**SENTIMENT()** - Analyzes emotional tone of text:
```sql
SELECT subject, from_company, category,
       SNOWFLAKE.CORTEX.SENTIMENT(email_body) AS sentiment_score
FROM SHIPPING_PARTNER_EMAILS
ORDER BY sentiment_score ASC;
```
- Score range: -1.0 (very negative) to +1.0 (very positive)
- Useful for: detecting unhappy customers, flagging escalations, monitoring partner relationships
- **No model selection needed** - Snowflake uses an optimized model automatically

**SUMMARIZE()** - Condenses long text:
```sql
SELECT incident_id, severity,
       SNOWFLAKE.CORTEX.SUMMARIZE(description_text) AS summary
FROM PORT_INCIDENT_LOGS
ORDER BY LENGTH(description_text) DESC LIMIT 5;
```
- Produces 2-3 sentence summaries of multi-paragraph text
- Great for: executive dashboards, alert notifications, quick-scan reports

**TRANSLATE()** - Machine translation:
```sql
SELECT subject,
       SNOWFLAKE.CORTEX.TRANSLATE(email_body, 'fr', 'en') AS english_translation
FROM SHIPPING_PARTNER_EMAILS WHERE language = 'fr';
```
- The Port of Vancouver is a federal facility and must support both English and French
- Supports: en, fr, de, es, it, ja, ko, pl, pt, ru, sv, zh

**Key advantage**: All three functions run as SQL - they can be embedded in views, dynamic tables, WHERE clauses, and JOINs. No external API calls, no data leaving Snowflake.
""")


PROMPT_6_2 = """In PORT_AI_DEMO.PORT_OPS, demonstrate SNOWFLAKE.CORTEX.COMPLETE() with a model comparison:

1. Take the 3 most critical (severity='critical' or 'high') incidents from PORT_INCIDENT_LOGS. For each, use COMPLETE() with TWO different models to generate a risk assessment and recommended actions:
   - Model A: 'claude-3-5-sonnet' 
   - Model B: 'llama3.1-70b'
   
   Use this prompt template for each incident:
   "You are a port safety analyst at the Port of Vancouver. Analyze this incident report and provide: 1) Risk level assessment 2) Root cause analysis 3) Three recommended preventive actions. Incident: {description_text}"

2. Show the results side-by-side: incident_id, severity, model_a_response, model_b_response

Execute the query and show the comparison."""

render_prompt("Prompt 6.2", "AI Complete for Analysis and Model Comparison", PROMPT_6_2)

render_explanation("What this prompt does", """
This demonstrates **CORTEX.COMPLETE()** - the most versatile Cortex function - with a side-by-side model comparison:

```sql
SELECT
  incident_id, severity,
  SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', prompt) AS model_a_response,
  SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', prompt) AS model_b_response
FROM (
  SELECT *, 'You are a port safety analyst...' || description_text AS prompt
  FROM PORT_INCIDENT_LOGS
  WHERE severity IN ('critical', 'high')
  LIMIT 3
);
```

**Available models in Snowflake Cortex** (as of April 2026):
| Model | Provider | Strengths | Cost |
|-------|----------|-----------|------|
| claude-3-5-sonnet | Anthropic | Strong reasoning, instruction following | Higher |
| llama3.1-70b | Meta | Good general performance, open weights | Lower |
| mistral-large2 | Mistral | European language support | Medium |
| llama3.1-8b | Meta | Fast, good for simple tasks | Lowest |

**Why compare models**: Different models excel at different tasks. For safety analysis, you want strong reasoning. For simple classification, a smaller model may suffice at lower cost.

**Cost implications**: Each COMPLETE() call is billed per token (input + output). Running the same prompt through two models doubles the cost. In production, you'd pick one model per use case after comparison.
""")


PROMPT_6_3 = """In PORT_AI_DEMO.PORT_OPS:

1. Use SNOWFLAKE.CORTEX.CLASSIFY_TEXT() on the CBSA_INSPECTION_REPORTS findings_text to classify each report into risk categories. Use this prompt:
   Classify each inspection finding as one of: 'Documentation Issue', 'Cargo Discrepancy', 'Security Concern', 'Regulatory Violation', 'Clean Inspection'. 

   SELECT report_id, inspection_type, 
          SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', 
            'Classify this CBSA inspection finding into exactly one category: Documentation Issue, Cargo Discrepancy, Security Concern, Regulatory Violation, or Clean Inspection. Return ONLY the category name. Finding: ' || findings_text
          ) as ai_classification,
          outcome, risk_score
   FROM CBSA_INSPECTION_REPORTS;

2. Use CORTEX.COMPLETE to extract structured key entities from 5 BILLS_OF_LADING_TEXT entries. Extract: shipper_name, consignee_name, port_of_loading, cargo_description, container_count as a JSON object.

Execute and show results."""

render_prompt("Prompt 6.3", "Classify and Extract", PROMPT_6_3)

render_explanation("What this prompt does", """
Two advanced LLM patterns using CORTEX.COMPLETE():

**Zero-shot classification**: We ask the LLM to categorize text without any training examples. The prompt constrains the output to exactly one of five categories. This is called "zero-shot" because the model hasn't been fine-tuned on our specific categories.

**Structured extraction**: We ask the LLM to extract specific fields from unstructured text and return them as JSON. This is a precursor to the more formal Document AI extraction in Session 7.

**Prompt engineering tips shown here**:
- "Return ONLY the category name" - Constrains output format
- Listing the exact categories - Prevents the model from inventing new ones
- "as a JSON object" - Requests structured output for programmatic parsing

**The extraction pattern** is particularly powerful:
```sql
PARSE_JSON(
  SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
    'Extract these fields as JSON: shipper_name, consignee_name... Text: ' || raw_text
  )
) AS extracted
```

This turns unstructured text into queryable structured data, all within SQL.
""")


render_key_concepts([
    {"term": "Cortex AI SQL Functions", "definition": "SQL-callable AI functions that run LLMs within Snowflake. SENTIMENT, SUMMARIZE, TRANSLATE are task-specific; COMPLETE is general-purpose. All process data without it leaving Snowflake's security perimeter."},
    {"term": "Zero-shot Classification", "definition": "Using an LLM to classify text into categories without any training examples. The categories are specified in the prompt. Works well for common classification tasks but less reliable for highly domain-specific categories."},
    {"term": "Prompt Engineering", "definition": "The art of crafting inputs to LLMs to get desired outputs. Key techniques: role setting ('You are a port safety analyst'), output constraints ('Return ONLY...'), structured output requests ('as JSON'), and few-shot examples."},
    {"term": "Cross-region Inference", "definition": "Snowflake account parameter that allows Cortex functions to route to models hosted in other regions. Required when a specific model isn't available in your account's region."},
])

render_domain_glossary([
    {"term": "Official Languages Act", "definition": "Canadian federal law requiring federal institutions (including port authorities) to provide services in both English and French. This drives the bilingual requirement for AI applications at the Port of Vancouver."},
    {"term": "Incident Severity Levels", "definition": "Port incidents are classified as low, medium, high, or critical. Critical incidents (e.g., major spills, vessel groundings) require immediate response and regulatory reporting to Transport Canada."},
])

render_what_you_built([
    "Sentiment analysis across all partner emails",
    "Automated summarization of incident reports",
    "French-to-English translation of bilingual correspondence",
    "Side-by-side model comparison (Claude vs Llama)",
    "Zero-shot classification of inspection reports",
    "Structured entity extraction from bills of lading",
])
