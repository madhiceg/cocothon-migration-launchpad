# AI Readiness Advisor Skill

**"There is no AI strategy without a Data Strategy."**

Enterprise-grade AI Readiness Assessment for Snowflake. Scores your data estate across 8 critical dimensions (0-100) and generates a detailed, actionable remediation plan.

## Dimensions & Weights

| Dimension | Weight | What it measures |
|---|---|---|
| Data Quality | 20% | Completeness, accuracy, consistency, DMF coverage |
| Data Governance | 15% | Ownership, cataloging, classification, policy coverage |
| Security & Compliance | 15% | RBAC, MFA, masking, encryption, network policies |
| AI Consumption Readiness | 15% | Cortex, vectors, model registry, feature engineering |
| Data Freshness | 10% | Pipeline latency, staleness detection, Dynamic Tables |
| Metadata & Lineage | 10% | Documentation, tagging, lineage, impact analysis |
| Infrastructure & Scalability | 10% | Warehouse optimization, cost governance, compute pools |
| Organizational Readiness | 5% | AI literacy, MLOps culture, strategy alignment |

## Maturity Bands

| Score | Band | Meaning |
|---|---|---|
| 0-25 | **Foundational** | Significant gaps — not ready for AI |
| 26-50 | **Developing** | Basic foundations, major remediation needed |
| 51-75 | **Advancing** | Solid practices, targeted improvements for production AI |
| 76-90 | **Mature** | Well-governed, ready for most AI use cases |
| 91-100 | **AI-Native** | Best-in-class, fully aligned for enterprise AI |

## Project Structure

```
ai_readiness_skill/
├── SKILL.md                                # Skill definition — persona, instructions, capabilities
├── skill.yaml                              # Minimal config — resource manifest
├── README.md
│
├── resources/
│   ├── scoring/                            # Dimension rubrics (scoring criteria & Snowflake signals)
│   │   ├── data_quality.md
│   │   ├── data_governance.md
│   │   ├── security_compliance.md
│   │   ├── ai_consumption_readiness.md
│   │   ├── data_freshness.md
│   │   ├── metadata_lineage.md
│   │   ├── infrastructure_scalability.md
│   │   └── organizational_readiness.md
│   ├── action_plans/                       # Remediation playbooks per dimension
│   │   ├── data_quality.md
│   │   ├── data_governance.md
│   │   ├── security_compliance.md
│   │   ├── ai_consumption_readiness.md
│   │   ├── data_freshness.md
│   │   ├── metadata_lineage.md
│   │   ├── infrastructure_scalability.md
│   │   └── organizational_readiness.md
│   └── templates/                          # Reusable governance & security templates
│       ├── rbac_hierarchy.md
│       ├── governance_tags.md
│       ├── masking_policies.md
│       ├── security_policies.md
│       └── constraints.md
│
└── tools/
    ├── orchestrator.py                     # Main entry point
    ├── assessment/
    │   ├── scoring_engine.py               # Score computation engine
    │   ├── probe_interpreters.py           # Translate SQL results to scores
    │   └── sql/                            # SQL probes per dimension (7 files)
    └── action_plan/
        ├── plan_generator.py               # Action plan & executive summary generator
        └── sql/                            # Remediation SQL templates (8 files)
```

## Usage

From a Snowflake Notebook:

```python
from tools.orchestrator import run_assessment
results = run_assessment(session)
```

The orchestrator will:
1. Run SQL probes against `ACCOUNT_USAGE` and `INFORMATION_SCHEMA`
2. Interpret results through scoring rubrics
3. Compute a weighted AI Readiness Score (0-100)
4. Generate a prioritized action plan with SQL templates
5. Produce an executive summary
