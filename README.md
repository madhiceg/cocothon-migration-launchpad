# CoCoDuo Migration Launchpad

**AI-Powered Migration Planning for Snowflake** — built by the CoCoDuo team for the kipi CoCothon Hackathon.

CoCoDuo Migration Launchpad turns weeks of manual migration planning into minutes. A Solutions Architect (SA) fills out a guided assessment form, and the system generates a comprehensive, branded migration plan — complete with tool recommendations, architecture patterns, timelines, risk analysis, and cost estimates — all powered by Snowflake Cortex Code (CoCo).

---

## How It Works

The solution follows a three-stage pipeline:

```
┌─────────────────┐      ┌──────────────────┐      ┌───────────────────────┐
│  Streamlit App   │ ───► │  CoCo Skill      │ ───► │  Snowflake Notebook   │
│  (Assessment     │      │  (migration-      │      │  (Migration Plan      │
│   Intake Form)   │      │   expert)         │      │   Generator)          │
└─────────────────┘      └──────────────────┘      └───────────────────────┘
```

### 1. Streamlit App (`streamlit_app.py`)
A multi-step intake form where SAs capture customer migration details:
- **Customer profile** — name, industry, company size, SA contact info
- **Source systems** — Oracle, Teradata, SQL Server, Hadoop, etc. with version, hosting, connectivity, and data volumes
- **ETL/ELT tools** — current pipeline tools, satisfaction levels, post-migration plans
- **Transformation layer** — dbt, Snowpark, stored procedures, current tooling
- **Architecture nuances** — cost priorities, technical debt, security requirements, risks, and free-text context

Submissions are stored in `MIGRATION_ASSESSMENTS.INTAKE.ASSESSMENTS` with full version history.

### 2. Cortex Code Skill (`migration-expert/`)
A custom CoCo skill that acts as a senior migration architect. When invoked, it:
- Fetches the customer's assessment data from Snowflake
- Cross-references a curated knowledge base of architecture patterns, tool profiles, industry use cases, source-system playbooks, and real customer migration stories
- Generates a structured migration plan as JSON covering:
  - Executive summary and scope
  - Architecture recommendations (medallion layers, warehouse strategy, RBAC)
  - Tool stack selection with scored comparisons across ingestion, transformation, orchestration, BI, and governance
  - Phase-by-phase timeline with milestones
  - Risk register with mitigations
  - Cost estimates and ROI projections

### 3. Snowflake Notebook (`Migration_Plan_Generator.ipynb`)
A pure renderer that takes the JSON plan output and generates a branded HTML report following kipi.ai brand guidelines — ready for customer delivery. Zero business logic; all intelligence lives in the skill.

---

## Project Structure

```
/
├── README.md                          # This file
├── streamlit_app.py                   # Assessment intake Streamlit app
├── Migration_Plan_Generator.ipynb     # Notebook — renders JSON plan to branded HTML
├── CoCoDuo_Presentation.ipynb         # Hackathon presentation deck generator
└── migration-expert/                  # CoCo custom skill
    ├── SKILL.md                       # Skill definition and instructions
    ├── scripts/
    │   └── fetch-assessment.sql       # SQL queries for assessment data retrieval
    ├── knowledge/                     # Curated knowledge base
    │   ├── architecture-patterns.md   # Medallion, Data Vault, star schema patterns
    │   ├── industry-use-cases.md      # Vertical-specific use cases and customer stories
    │   ├── migration-reference-pack.md# 12-step migration methodology
    │   ├── multi-tenancy-patterns.md  # MTT, OPT, APT patterns
    │   ├── source-system-playbooks.md # Oracle, Teradata, SQL Server, Hadoop playbooks
    │   ├── tool-profiles.md           # Detailed tool ratings and comparisons
    │   ├── tool-selection-matrix.md   # Tool selection decision matrix
    │   └── references/                # PDFs, ebooks, SVGs from Snowflake resources
    └── brand-resources/               # kipi.ai logos and brand guidelines
        ├── brand-guidelines.md        # Colors, typography, layout rules
        └── *.png                      # Logo assets
```

---

## Key Features

- **Guided Assessment Intake** — Structured Streamlit form with multi-step wizard, dynamic source system fields, progress tracking, and auto-save via version history
- **Knowledge-Grounded Plans** — The skill draws from 8+ curated knowledge documents covering 50+ tools, 10+ industries, 6+ source system playbooks, and real Snowflake customer stories
- **Tool Scoring Engine** — Rates tools across Snowflake fit, ease of use, enterprise depth, and cost — then recommends stacks tailored to the customer's source systems, budget, and team size
- **Industry-Aware Recommendations** — Maps customer industry to post-migration use cases, reference architectures, and value roadmaps
- **Branded Output** — HTML reports follow kipi.ai brand guidelines with proper colors, typography, and layout
- **Full Audit Trail** — Every assessment submission is versioned with change summaries in `ASSESSMENT_VERSION_HISTORY`

---

## Prerequisites

- Snowflake account with access to `MIGRATION_ASSESSMENTS` database
- Cortex Code (CoCo) enabled in Snowsight Workspace
- Snowflake Notebook runtime for rendering migration plans

---

## Usage

1. **Submit an assessment** — Open the Streamlit app and walk through the intake form for a customer
2. **Generate a plan** — In a CoCo chat session, invoke the migration-expert skill:
   ```
   Generate a migration plan for assessment assess-004-titanforge
   ```
   CoCo fetches the assessment, applies the knowledge base, and outputs a JSON plan file
3. **Render the report** — Open `Migration_Plan_Generator.ipynb`, set the `PLAN_JSON_FILE` variable to the generated JSON filename, and run all cells to produce the branded HTML report

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Assessment Intake | Streamlit in Snowflake |
| AI Planning Engine | Snowflake Cortex Code (CoCo) Custom Skill |
| Knowledge Base | Markdown files + curated PDFs |
| Data Storage | Snowflake tables (`MIGRATION_ASSESSMENTS.INTAKE`) |
| Report Rendering | Snowflake Notebook (Python + HTML/CSS) |
| Presentation | Snowflake Notebook (OpenXML PPTX generation) |

---

## Team

**CoCoDuo** — kipi.ai CoCothon Hackathon, March 2026
