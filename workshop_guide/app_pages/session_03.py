import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(
    session_num=3,
    title="Security and Governance for AI Workloads",
    time_range="10:15 - 10:40 AM",
    duration="25 min",
    building="4 roles, masking policies, and sensitivity tags",
)

render_technologies_used([
    {"name": "Role-Based Access Control", "description": "Snowflake's RBAC model uses roles as the primary access control mechanism. Privileges are granted to roles, and roles are granted to users. Supports hierarchical role inheritance.", "icon": "admin_panel_settings"},
    {"name": "Dynamic Data Masking", "description": "Column-level security policies that transform data at query time based on the querying user's role. The underlying data is never modified - masking happens on-the-fly.", "icon": "visibility_off"},
    {"name": "Object Tagging", "description": "Metadata tags that can be applied to databases, schemas, tables, and columns. Tags enable data classification, lineage tracking, and policy-based governance at scale.", "icon": "label"},
])


PROMPT_3_1 = """In PORT_AI_DEMO, create the following roles and grant structure to demonstrate governance for AI workloads:

1. Create roles: PORT_DATA_ENGINEER, PORT_DATA_SCIENTIST, PORT_ANALYST, PORT_CUSTOMS_OFFICER
2. Grant the following access pattern:
   - PORT_DATA_ENGINEER: full access to PORT_OPS schema (all tables, create)
   - PORT_DATA_SCIENTIST: SELECT on all tables, plus USAGE on PORT_AI_WH, plus ability to use Cortex functions (grant SNOWFLAKE.CORTEX_USER database role)
   - PORT_ANALYST: SELECT on CONTAINER_MANIFESTS, CARGO_INVOICES, RAIL_SCHEDULES, TERMINALS, VESSELS, TRADE_PARTNERS (no access to CBSA reports or incident logs)
   - PORT_CUSTOMS_OFFICER: SELECT on CBSA_INSPECTION_REPORTS, CONTAINER_MANIFESTS, BILLS_OF_LADING_TEXT only

3. Grant all roles to my current user (OBENNING) so I can test them.

Execute all the SQL and show me a summary of what was granted."""

render_prompt("Prompt 3.1", "RBAC for Port Operations", PROMPT_3_1)

render_explanation("What this prompt does", """
This creates a realistic **Role-Based Access Control (RBAC)** hierarchy:

**PORT_DATA_ENGINEER** - Full access. Can create, modify, and delete objects. This is the "builder" role.

**PORT_DATA_SCIENTIST** - Read access to all data plus Cortex AI function access. The `SNOWFLAKE.CORTEX_USER` database role is critical - it grants access to all Cortex LLM functions (COMPLETE, SENTIMENT, TRANSLATE, etc.). Without this role, Cortex calls fail.

**PORT_ANALYST** - Limited to operational/commercial data. No access to sensitive CBSA reports or incident logs. This demonstrates the principle of least privilege.

**PORT_CUSTOMS_OFFICER** - Focused access to customs-related data only. Cannot see commercial invoices or crane metrics.

**Key SQL patterns**:
```sql
CREATE ROLE PORT_DATA_SCIENTIST;
GRANT USAGE ON DATABASE PORT_AI_DEMO TO ROLE PORT_DATA_SCIENTIST;
GRANT USAGE ON SCHEMA PORT_AI_DEMO.PORT_OPS TO ROLE PORT_DATA_SCIENTIST;
GRANT SELECT ON ALL TABLES IN SCHEMA PORT_AI_DEMO.PORT_OPS TO ROLE PORT_DATA_SCIENTIST;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE PORT_DATA_SCIENTIST;
```

**Why this matters for AI**: AI workloads access more data than traditional BI. A single Cortex Agent might query across all tables. Proper RBAC ensures that even AI-powered applications respect data boundaries.
""")


PROMPT_3_2 = """In PORT_AI_DEMO.PORT_OPS, implement the following governance controls:

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

Execute all SQL. Then demonstrate the masking by querying CARGO_INVOICES as the current role and show the tag assignments."""

render_prompt("Prompt 3.2", "Data Masking and Tagging", PROMPT_3_2)

render_explanation("What this prompt does", """
This implements two critical governance features:

**Object Tagging** (`CREATE TAG`): Tags are key-value metadata attached to Snowflake objects. They're used for:
- Data classification (PII, confidential, public)
- Regulatory compliance tracking (GDPR, CCPA, PIPEDA)
- Automated policy enforcement via tag-based masking
- Data catalog enrichment

```sql
CREATE OR REPLACE TAG PORT_AI_DEMO.PORT_OPS.SENSITIVITY_LEVEL
  ALLOWED_VALUES 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED';

ALTER TABLE CARGO_INVOICES MODIFY COLUMN total_value_cad
  SET TAG SENSITIVITY_LEVEL = 'CONFIDENTIAL';
```

**Dynamic Data Masking** (`CREATE MASKING POLICY`): Masking policies use conditional logic based on `CURRENT_ROLE()` to decide what the user sees:

```sql
CREATE OR REPLACE MASKING POLICY MASK_FINANCIAL_DATA AS (val STRING)
  RETURNS STRING ->
    CASE
      WHEN CURRENT_ROLE() IN ('PORT_DATA_ENGINEER', 'PORT_CUSTOMS_OFFICER') THEN val
      ELSE '***MASKED***'
    END;
```

The policy is then attached to a column. **The underlying data is never changed** - masking happens at query time. This means the same query returns different results for different roles.

**Tag-based masking**: In production, you can combine tags and masking policies so that any column tagged `CONFIDENTIAL` automatically gets masked. This scales governance across thousands of columns.
""")


PROMPT_3_3 = """Run these governance verification queries in PORT_AI_DEMO.PORT_OPS:

1. Show all tag references on the PORT_OPS schema using INFORMATION_SCHEMA.TAG_REFERENCES for our SENSITIVITY_LEVEL tag
2. Show all masking policies applied using INFORMATION_SCHEMA.POLICY_REFERENCES  
3. Query 5 rows from CARGO_INVOICES to show which columns are masked for the current role

Show the results."""

render_prompt("Prompt 3.3", "Verify Governance", PROMPT_3_3)

render_explanation("What this prompt does", """
Verification queries using Snowflake's **INFORMATION_SCHEMA** governance views:

- **TAG_REFERENCES**: Shows every object and column that has a tag applied, along with the tag value. This is how you audit data classification across your account.

- **POLICY_REFERENCES**: Shows which masking (and row access) policies are attached to which columns. Critical for compliance auditing.

- **Querying masked data**: When you query `CARGO_INVOICES` as `ACCOUNTADMIN`, you'll see the raw data. If you `USE ROLE PORT_ANALYST` first, the `consignee_name` column will show `***MASKED***` and `total_value_cad` will show `0.00`.

These views are part of Snowflake's **Horizon** governance framework, which provides centralized visibility into data access, classification, and policy enforcement.
""")


render_key_concepts([
    {"term": "RBAC (Role-Based Access Control)", "definition": "Snowflake's security model where all access is mediated through roles. Users are granted roles, roles are granted privileges on objects, and roles can be granted to other roles (hierarchy). ACCOUNTADMIN is the top-level role."},
    {"term": "Dynamic Data Masking", "definition": "A column-level security feature that uses masking policies to conditionally replace column values at query time. The policy is a SQL function that receives the column value and returns either the real value or a masked version based on CURRENT_ROLE() or other context functions."},
    {"term": "Object Tagging", "definition": "Key-value metadata that can be applied to any Snowflake object (database, schema, table, column, warehouse, user, etc.). Tags enable classification, governance automation, and cost attribution. Tags propagate through lineage - a tag on a source column can be tracked to downstream objects."},
    {"term": "SNOWFLAKE.CORTEX_USER", "definition": "A database role that grants access to Snowflake Cortex AI functions. Without this role, users cannot call functions like COMPLETE(), SENTIMENT(), TRANSLATE(), or EMBED_TEXT(). It must be explicitly granted to user roles."},
])

render_domain_glossary([
    {"term": "Principle of Least Privilege", "definition": "A security best practice where users are granted only the minimum access required for their job function. PORT_ANALYST can see commercial data but not CBSA reports; PORT_CUSTOMS_OFFICER can see inspection data but not commercial invoices."},
    {"term": "PIPEDA", "definition": "The Personal Information Protection and Electronic Documents Act — Canada's federal privacy law governing how private-sector organizations collect, use, and disclose personal information. Relevant to port operations handling shipper/consignee personal data."},
    {"term": "CBSA Inspection Reports", "definition": "Confidential government documents produced by Canada Border Services Agency during cargo inspections. These contain sensitive findings about cargo discrepancies, security concerns, and regulatory violations."},
])

render_what_you_built([
    "4 custom roles: PORT_DATA_ENGINEER, PORT_DATA_SCIENTIST, PORT_ANALYST, PORT_CUSTOMS_OFFICER",
    "SENSITIVITY_LEVEL tag with 4 classification levels",
    "5 tag assignments across sensitive columns",
    "MASK_FINANCIAL_DATA masking policy for text columns",
    "MASK_DOLLAR_VALUES masking policy for numeric columns",
])
