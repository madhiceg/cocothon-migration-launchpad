from dataclasses import dataclass, field

DIMENSION_WEIGHTS = {
    "data_quality": 0.20,
    "data_governance": 0.15,
    "security_compliance": 0.15,
    "data_freshness": 0.10,
    "metadata_lineage": 0.10,
    "ai_consumption_readiness": 0.15,
    "infrastructure_scalability": 0.10,
    "organizational_readiness": 0.05,
}

BANDS = [
    {"min": 0, "max": 25, "label": "Foundational", "color": "red"},
    {"min": 26, "max": 50, "label": "Developing", "color": "orange"},
    {"min": 51, "max": 75, "label": "Advancing", "color": "yellow"},
    {"min": 76, "max": 90, "label": "Mature", "color": "green"},
    {"min": 91, "max": 100, "label": "AI-Native", "color": "blue"},
]

DIMENSION_RUBRICS = {
    "data_quality": {
        "name": "Data Quality",
        "criteria": [
            {"id": "completeness", "name": "Completeness", "weight": 0.25},
            {"id": "accuracy", "name": "Accuracy", "weight": 0.20},
            {"id": "consistency", "name": "Consistency", "weight": 0.20},
            {"id": "validity", "name": "Validity", "weight": 0.15},
            {"id": "timeliness_quality", "name": "Quality Monitoring Coverage", "weight": 0.20},
        ],
    },
    "data_governance": {
        "name": "Data Governance",
        "criteria": [
            {"id": "ownership", "name": "Data Ownership & Stewardship", "weight": 0.20},
            {"id": "cataloging", "name": "Data Cataloging & Discovery", "weight": 0.20},
            {"id": "policy_coverage", "name": "Policy Coverage", "weight": 0.25},
            {"id": "classification", "name": "Sensitive Data Classification", "weight": 0.20},
            {"id": "access_audit", "name": "Access Auditing & History", "weight": 0.15},
        ],
    },
    "security_compliance": {
        "name": "Security & Compliance",
        "criteria": [
            {"id": "rbac_maturity", "name": "RBAC Maturity", "weight": 0.25},
            {"id": "encryption", "name": "Encryption & Key Management", "weight": 0.15},
            {"id": "network_security", "name": "Network Security", "weight": 0.15},
            {"id": "mfa_auth", "name": "Authentication & MFA", "weight": 0.15},
            {"id": "compliance_posture", "name": "Regulatory Compliance Posture", "weight": 0.15},
            {"id": "data_masking", "name": "Dynamic Data Masking", "weight": 0.15},
        ],
    },
    "data_freshness": {
        "name": "Data Freshness",
        "criteria": [
            {"id": "pipeline_latency", "name": "Pipeline Latency", "weight": 0.30},
            {"id": "staleness_detection", "name": "Staleness Detection", "weight": 0.25},
            {"id": "refresh_strategy", "name": "Refresh Strategy", "weight": 0.25},
            {"id": "historical_availability", "name": "Historical Data Availability", "weight": 0.20},
        ],
    },
    "metadata_lineage": {
        "name": "Metadata & Lineage",
        "criteria": [
            {"id": "column_lineage", "name": "Column-Level Lineage", "weight": 0.25},
            {"id": "documentation", "name": "Object Documentation", "weight": 0.20},
            {"id": "tagging_coverage", "name": "Object Tagging Coverage", "weight": 0.20},
            {"id": "impact_analysis", "name": "Impact Analysis Capability", "weight": 0.20},
            {"id": "schema_evolution", "name": "Schema Evolution Tracking", "weight": 0.15},
        ],
    },
    "ai_consumption_readiness": {
        "name": "AI Consumption Readiness",
        "criteria": [
            {"id": "feature_engineering", "name": "Feature Engineering Readiness", "weight": 0.20},
            {"id": "vector_readiness", "name": "Vector & Embedding Readiness", "weight": 0.20},
            {"id": "cortex_integration", "name": "Cortex LLM & AI Function Readiness", "weight": 0.20},
            {"id": "ml_model_registry", "name": "ML Model Registry & Deployment", "weight": 0.20},
            {"id": "data_schema_ml_friendly", "name": "ML-Friendly Schema Design", "weight": 0.20},
        ],
    },
    "infrastructure_scalability": {
        "name": "Infrastructure & Scalability",
        "criteria": [
            {"id": "warehouse_optimization", "name": "Warehouse Optimization", "weight": 0.25},
            {"id": "cost_governance", "name": "Cost Governance", "weight": 0.25},
            {"id": "compute_pools", "name": "Compute Pool Readiness", "weight": 0.25},
            {"id": "storage_optimization", "name": "Storage Optimization", "weight": 0.25},
        ],
    },
    "organizational_readiness": {
        "name": "Organizational Readiness",
        "criteria": [
            {"id": "ai_literacy", "name": "AI Literacy & Skills", "weight": 0.25},
            {"id": "mlops_culture", "name": "MLOps & DataOps Culture", "weight": 0.25},
            {"id": "cross_functional", "name": "Cross-Functional Alignment", "weight": 0.25},
            {"id": "ai_strategy", "name": "Documented AI Strategy", "weight": 0.25},
        ],
    },
}


@dataclass
class CriterionScore:
    criterion_id: str
    criterion_name: str
    score: float
    max_score: float
    weight: float
    evidence: str = ""
    recommendation: str = ""


@dataclass
class DimensionScore:
    dimension_id: str
    dimension_name: str
    weight: float
    raw_score: float
    weighted_score: float
    criteria: list = field(default_factory=list)


@dataclass
class AIReadinessReport:
    overall_score: float
    band_label: str
    band_color: str
    dimensions: list = field(default_factory=list)
    timestamp: str = ""


def get_band(score: float) -> dict:
    for band in BANDS:
        if band["min"] <= score <= band["max"]:
            return band
    return BANDS[-1]


def score_dimension(dimension_id: str, criterion_scores: dict) -> DimensionScore:
    rubric = DIMENSION_RUBRICS[dimension_id]
    weight = DIMENSION_WEIGHTS[dimension_id]
    criteria_results = []
    total_weighted = 0.0
    total_weight = 0.0

    for criterion in rubric["criteria"]:
        cid = criterion["id"]
        cweight = criterion["weight"]
        raw = criterion_scores.get(cid, 0)
        raw = max(0, min(100, raw))

        criteria_results.append(
            CriterionScore(
                criterion_id=cid,
                criterion_name=criterion["name"],
                score=raw,
                max_score=100,
                weight=cweight,
            )
        )
        total_weighted += raw * cweight
        total_weight += cweight

    raw_score = total_weighted / total_weight if total_weight > 0 else 0
    weighted_score = raw_score * weight

    return DimensionScore(
        dimension_id=dimension_id,
        dimension_name=rubric["name"],
        weight=weight,
        raw_score=round(raw_score, 2),
        weighted_score=round(weighted_score, 2),
        criteria=criteria_results,
    )


def compute_overall_score(dimension_scores: list) -> AIReadinessReport:
    from datetime import datetime

    overall = sum(d.weighted_score for d in dimension_scores)
    overall = round(overall, 2)
    band = get_band(overall)

    return AIReadinessReport(
        overall_score=overall,
        band_label=band["label"],
        band_color=band["color"],
        dimensions=dimension_scores,
        timestamp=datetime.utcnow().isoformat(),
    )


def score_from_probe_results(probe_results: dict) -> AIReadinessReport:
    dimension_scores = []
    for dim_id in DIMENSION_WEIGHTS:
        criterion_scores = probe_results.get(dim_id, {})
        dim_score = score_dimension(dim_id, criterion_scores)
        dimension_scores.append(dim_score)

    return compute_overall_score(dimension_scores)


def format_report(report: AIReadinessReport) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("       ENTERPRISE AI READINESS SCORE")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  OVERALL SCORE:  {report.overall_score} / 100")
    lines.append(f"  MATURITY BAND:  {report.band_label.upper()} ({report.band_color})")
    lines.append(f"  ASSESSED:       {report.timestamp}")
    lines.append("")
    lines.append("-" * 70)
    lines.append(f"  {'DIMENSION':<35} {'SCORE':>8} {'WEIGHT':>8} {'WEIGHTED':>10}")
    lines.append("-" * 70)

    for dim in sorted(report.dimensions, key=lambda d: d.raw_score):
        lines.append(
            f"  {dim.dimension_name:<35} {dim.raw_score:>7.1f} {dim.weight:>7.0%} {dim.weighted_score:>9.2f}"
        )

    lines.append("-" * 70)
    lines.append("")

    for dim in sorted(report.dimensions, key=lambda d: d.raw_score):
        band = get_band(dim.raw_score)
        lines.append(f"  [{band['label'].upper()}] {dim.dimension_name} — {dim.raw_score}/100")
        for c in dim.criteria:
            bar = "█" * int(c.score / 5) + "░" * (20 - int(c.score / 5))
            lines.append(f"    {c.criterion_name:<30} {bar} {c.score:>5.1f}")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)
