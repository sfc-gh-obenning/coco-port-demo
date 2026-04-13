import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(11, "Building Agentic Systems with Cortex Agent API", "2:50 - 3:20 PM", "30 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF or stored procedure as a tool, enabling custom business logic, calculations, or external integrations.", "icon": "build"},
])


PROMPT_11_1 = """In PORT_AI_DEMO.PORT_OPS, create a Cortex Agent called PORT_OPS_AGENT that port operations staff can use to ask questions about both structured data and unstructured documents.

It should:
- Use claude-sonnet-4-6 as the orchestration model
- Have two tools: the PORT_OPERATIONS_VIEW semantic view (for structured data queries) and the port_knowledge_search Cortex Search service (for safety docs and inspection reports)
- Include instructions that define it as the Port of Vancouver Operations Assistant, guiding it to use the right tool for the question type — structured data tool for numbers/volumes/metrics, search tool for incidents/reports/documents
- Mention key domain context in the instructions: Canada's largest port, $200B annual trade, key terminals (Deltaport, Vanterm, Centerm), and support for English and French
- Include 3-4 sample questions that span both tools (e.g. TEU volumes, incident reports, CBSA inspections)

Execute and show confirmation."""

render_prompt("Prompt 11.1", "Create the Cortex Agent", PROMPT_11_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** - an AI orchestrator that combines multiple data tools:

**CREATE AGENT anatomy**:

- **MODEL**: The LLM used for orchestration (planning, reflection, response generation). `claude-sonnet-4-6` is recommended for its strong reasoning.

- **TOOLS**: The capabilities the agent can use:
  - **Cortex Search service** (`port_knowledge_search`): For searching unstructured documents
  - **Semantic view** (`PORT_OPERATIONS_VIEW`): For generating SQL queries from natural language
  - Custom UDFs/procedures can be added too

- **INSTRUCTIONS**: System prompt that shapes the agent's behavior, tone, and priorities. Key elements:
  - Role definition ("You are the Port of Vancouver Operations Assistant")
  - Tool routing guidance ("use the structured data tool" for numbers)
  - Behavioral guidelines (cite sources, emphasize safety)
  - Bilingual support (English + French)

- **SAMPLE_QUESTIONS**: Seed questions shown to users in the UI. Help users understand what the agent can do.

**How the Agent orchestrates**:
1. **Planning**: Receives user question, decides which tool(s) to use
2. **Tool execution**: Calls Analyst (generates + runs SQL) or Search (retrieves documents)
3. **Reflection**: Evaluates tool results - are they sufficient? Need another tool?
4. **Response**: Synthesizes a natural language answer from tool outputs

**Agent vs. RAG**: The RAG pattern in Session 8 was a single retrieve-then-generate pipeline. An Agent is smarter - it can decide to use Search, then Analyst, then Search again based on the question. It can also split complex questions into sub-tasks.

**Semantic view as a tool**: The Agent uses the semantic view (from Sessions 10-11) as its structured data tool. When a question requires SQL, the Agent routes to Cortex Analyst which uses the semantic view's definitions to generate the query.
""")


PROMPT_11_2 = """Test our PORT_OPS_AGENT by running queries through SNOWFLAKE.CORTEX.DATA_AGENT_RUN(). This function lets us call the agent via SQL and get a JSON response.

Run these four queries one at a time, parsing the response with TRY_PARSE_JSON:

1. Structured data query: "What are the busiest terminals by TEU count this year and which shipping lines dominate each terminal?"
2. Unstructured search query: "Have there been any environmental incidents near Neptune Terminals? What was done about them?"
3. Mixed query (should use both tools): "Which terminals have had both the highest cargo volume AND the most safety incidents? Is there a correlation?"
4. Bilingual query: "Quels sont les principaux problemes de securite signales au port cette annee?"

For each, show the full response including which tools the agent chose to use."""

render_prompt("Prompt 11.2", "Test the Agent", PROMPT_11_2)

render_explanation("What this prompt does", """
Tests the Agent via `SNOWFLAKE.CORTEX.DATA_AGENT_RUN()` — a SQL function that runs an existing agent object and returns JSON:

```sql
SELECT TRY_PARSE_JSON(
  SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'PORT_AI_DEMO.PORT_OPS.PORT_OPS_AGENT',
    $${ "messages": [{ "role": "user", "content": [{ "type": "text", "text": "your question here" }] }] }$$
  )
) AS resp;
```

**Four question types test different tool routing**:

1. **Pure structured** — routes to Cortex Analyst, generates SQL with GROUP BY terminal and shipping line
2. **Pure unstructured** — routes to Cortex Search, retrieves environmental incident documents
3. **Mixed** — requires BOTH tools: Analyst for cargo volume, Search for safety incidents, then combines results
4. **Bilingual** — French question routed to English-language tools, response synthesized in French

**What to look for in the JSON response**:
- `content` array contains thinking steps, tool_use entries, and the final text response
- Tool use entries show which tools were called and with what parameters
- The `metadata` section includes token usage for cost tracking
""")


PROMPT_11_3 = """In PORT_AI_DEMO.PORT_OPS, enhance our agent by adding a custom tool. 

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

3. Recreate PORT_OPS_AGENT to include CALCULATE_CONGESTION_RISK as an additional tool alongside the existing Analyst and Search tools."""

render_prompt("Prompt 11.3", "Agent with Custom Tool", PROMPT_11_3)

render_explanation("What this prompt does", """
Extends the Agent with a **custom UDF tool**:

**Custom tools** allow Agents to go beyond Search and Analyst:
- Business calculations (congestion risk scoring)
- External API calls (via external access integrations)
- Data transformations (formatting, currency conversion)
- Workflow triggers (creating tickets, sending notifications)

**The UDF** implements a simple rule-based congestion risk calculator. In production, this could call our ML model instead.

**How the Agent uses custom tools**: When the user asks about congestion risk, the Agent:
1. Recognizes this matches the CALCULATE_CONGESTION_RISK function
2. Extracts parameters from the question (terminal=Deltaport, TEU=2000, month=November)
3. Calls the UDF with those parameters
4. Incorporates the result into its response

**This is the "agentic" pattern**: The Agent doesn't just retrieve data - it takes actions, calls functions, and orchestrates workflows. Custom tools are what make Agents truly powerful for enterprise use cases.
""")

PROMPT_11_4 = """Test the enhanced PORT_OPS_AGENT (now with 3 tools) using SNOWFLAKE.CORTEX.DATA_AGENT_RUN(). Run these queries that exercise the new custom tool:

1. "What is the congestion risk for a 2000 TEU shipment arriving at Deltaport in November?"
2. "What are the current TEU volumes at each terminal, and what would the congestion risk be if volumes doubled during peak season?"
3. "For Vanterm, show me the current cargo volume, any recent safety incidents, and the congestion risk assessment for next month."

Show the parsed JSON responses and note which tools the agent selected for each."""

render_prompt("Prompt 11.4", "Test the Enhanced Agent", PROMPT_11_4)

render_explanation("What this prompt does", """
Tests the enhanced Agent's ability to use the **new custom tool** alongside Analyst and Search:

**Query 1 - Custom tool only**: The Agent should extract parameters (terminal=Deltaport, TEU=2000, month=11) and call CALCULATE_CONGESTION_RISK directly. Expect a HIGH risk result with a recommendation to pre-allocate resources.

**Query 2 - Custom + Analyst**: The Agent should first query current TEU volumes via Analyst, then call the congestion risk UDF with doubled values for each terminal.

**Query 3 - All three tools**: The Agent should orchestrate all three tools:
1. Analyst for cargo volume data
2. Search for safety incident documents
3. Custom UDF for congestion risk scoring

Watch the `tool_use` entries in the JSON response to see how the Agent plans and sequences the tool calls.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs, Cortex Analyst, Cortex Search, and custom tools to answer complex questions. Supports planning, tool use, reflection, and multi-turn conversations via threads."},
    {"term": "Tool Routing", "definition": "The Agent's ability to select the appropriate tool for each question or sub-task. Structured data queries -> Analyst, unstructured search -> Search, calculations -> custom UDFs. The LLM decides routing based on the question and tool descriptions."},
    {"term": "Agent Threads", "definition": "Persistent conversation contexts that maintain history across multiple interactions. A thread allows the Agent to reference previous questions and answers, enabling follow-up questions and contextual conversations."},
    {"term": "Custom Tools", "definition": "SQL UDFs or stored procedures registered as Agent tools. The Agent can call them with extracted parameters. Enables custom business logic, external integrations, and workflow automation within the Agent framework."},
])

render_domain_glossary([
    {"term": "Port Operations Staff", "definition": "Includes terminal operators (manage cranes and berths), vessel traffic controllers (manage ship movements), logistics coordinators (manage rail and truck connections), and customs officers (CBSA clearances). The Agent serves all these personas."},
    {"term": "Congestion Risk Assessment", "definition": "The custom UDF (CALCULATE_CONGESTION_RISK) models a simplified version of how port planners assess risk: high TEU count + peak season = high risk. Real systems use ML models and dozens of variables."},
])

render_what_you_built([
    "PORT_OPS_AGENT - Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, mixed, and bilingual queries",
    "CALCULATE_CONGESTION_RISK UDF as a custom tool",
    "Enhanced agent with three tool types (Analyst + Search + custom)",
])
