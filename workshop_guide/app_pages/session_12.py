import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(12, "Building Agentic Systems with Cortex Agent API", "3:15 - 3:45 PM", "30 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF or stored procedure as a tool, enabling custom business logic, calculations, or external integrations.", "icon": "build"},
])


PROMPT_12_1 = """In PORT_AI_DEMO.PORT_OPS, create a Cortex Agent that port operations staff can use to ask questions about both structured data and unstructured documents.

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

Execute and show confirmation."""

render_prompt("Prompt 12.1", "Create the Cortex Agent", PROMPT_12_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** - an AI orchestrator that combines multiple data tools:

**CREATE AGENT anatomy**:

- **MODEL**: The LLM used for orchestration (planning, reflection, response generation). `claude-3-5-sonnet` is recommended for its strong reasoning.

- **TOOLS**: The capabilities the agent can use:
  - **Cortex Search service** (`port_knowledge_search`): For searching unstructured documents
  - **Semantic model** (YAML on stage): For generating SQL queries from natural language
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
""")


PROMPT_12_2 = """Test our PORT_OPS_AGENT in PORT_AI_DEMO.PORT_OPS with a series of questions that exercise both tools. Run each as a separate agent interaction:

1. Structured data query: "What are the busiest terminals by TEU count this year and which shipping lines dominate each terminal?"

2. Unstructured search query: "Have there been any environmental incidents near Neptune Terminals? What was done about them?"

3. Mixed query: "Which terminals have had both the highest cargo volume AND the most safety incidents? Is there a correlation?"

4. Bilingual query: "Quels sont les principaux problemes de securite signales au port cette annee?"

For each, show the agent's response and note which tools it chose to use."""

render_prompt("Prompt 12.2", "Test the Agent with Mixed Queries", PROMPT_12_2)

render_explanation("What this prompt does", """
Tests the Agent's **tool selection and orchestration** across four question types:

**Query 1 - Pure structured**: The Agent should route entirely to Cortex Analyst, which generates SQL with GROUP BY terminal and shipping line.

**Query 2 - Pure unstructured**: The Agent should route to Cortex Search, searching for environmental incidents near Neptune Terminals.

**Query 3 - Mixed (the real test)**: This requires BOTH tools:
1. Analyst: Get cargo volume by terminal (SQL)
2. Search: Find safety incidents by terminal (document retrieval)
3. Combine: Compare the two datasets and analyze correlation

The Agent should split this into sub-tasks and use both tools.

**Query 4 - Bilingual**: Tests French language handling. The Agent should understand French, route to appropriate tools (which operate on English data), and respond in French.

**What to observe**:
- The Agent emits **thinking events** showing its reasoning
- You can see which tools were called and in what order
- The response synthesizes data from potentially multiple tool calls
- Responses include citations (doc_ids from Search, SQL results from Analyst)
""")


PROMPT_12_3 = """In PORT_AI_DEMO.PORT_OPS, enhance our agent by adding a custom tool. 

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

Execute all SQL and test the updated agent with: "What is the congestion risk for a 2000 TEU shipment arriving at Deltaport in November?\""""

render_prompt("Prompt 12.3", "Agent with Custom Tool", PROMPT_12_3)

render_explanation("What this prompt does", """
Extends the Agent with a **custom UDF tool**:

**Custom tools** allow Agents to go beyond Search and Analyst:
- Business calculations (congestion risk scoring)
- External API calls (via external access integrations)
- Data transformations (formatting, currency conversion)
- Workflow triggers (creating tickets, sending notifications)

**The UDF** implements a simple rule-based congestion risk calculator. In production, this could call our ML model instead.

**Adding the UDF to the Agent**:
```sql
CREATE OR REPLACE AGENT PORT_OPS_AGENT
  MODEL = 'claude-3-5-sonnet'
  TOOLS = (
    port_knowledge_search,
    @SEMANTIC_MODELS/port_operations_model.yaml,
    CALCULATE_CONGESTION_RISK  -- Custom tool added
  )
  INSTRUCTIONS = '...'
```

**How the Agent uses custom tools**: When the user asks about congestion risk, the Agent:
1. Recognizes this matches the CALCULATE_CONGESTION_RISK function
2. Extracts parameters from the question (terminal=Deltaport, TEU=2000, month=November)
3. Calls the UDF with those parameters
4. Incorporates the result into its response

**This is the "agentic" pattern**: The Agent doesn't just retrieve data - it takes actions, calls functions, and orchestrates workflows. Custom tools are what make Agents truly powerful for enterprise use cases.
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
