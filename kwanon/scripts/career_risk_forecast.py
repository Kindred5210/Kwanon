#!/usr/bin/env python3
"""Generate AI replacement risk and career resilience forecasts.

The model is intentionally transparent and heuristic. It estimates scenario
pressure from structured career factors; it does not claim to predict a
person's actual fate or employment outcome.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple


RISK_WEIGHTS = {
    "occupation_task_exposure": 0.30,
    "industry_adoption": 0.12,
    "task_standardization": 0.12,
    "verification_ease": 0.10,
    "ai_tool_fit": 0.08,
    "market_pressure": 0.08,
    "low_human_trust": 0.07,
    "low_physical_dependency": 0.05,
    "low_domain_context": 0.04,
    "low_resource_buffer": 0.04,
}

RESILIENCE_WEIGHTS = {
    "ai_collaboration": 0.18,
    "business_judgment": 0.16,
    "project_proof": 0.14,
    "learning_velocity": 0.14,
    "domain_knowledge": 0.12,
    "communication_accountability": 0.10,
    "research_depth": 0.06,
    "network_access": 0.05,
    "resource_buffer": 0.05,
}

SCENARIOS = {
    "slow": {"k": 0.035, "midpoint": 54.0, "max_multiplier": 1.15},
    "base": {"k": 0.060, "midpoint": 36.0, "max_multiplier": 1.35},
    "fast": {"k": 0.095, "midpoint": 24.0, "max_multiplier": 1.65},
}

OCCUPATION_FAMILIES: Dict[str, Dict[str, Any]] = {
    "digital-production": {
        "keywords": ("developer", "programmer", "software", "engineer", "analyst", "designer", "writer", "translator", "editor", "data", "前端", "后端", "程序员", "开发", "设计", "文案", "翻译", "分析师", "数据"),
        "defaults": {"occupation_task_exposure": 68, "industry_adoption": 72, "task_standardization": 62, "verification_ease": 75, "ai_tool_fit": 78, "market_pressure": 64, "human_trust_requirement": 38, "physical_dependency": 5, "domain_knowledge": 42},
    },
    "process-service": {
        "keywords": ("support", "customer service", "admin", "assistant", "operator", "hr ops", "finance ops", "document review", "客服", "行政", "助理", "运营", "审核", "录入", "文员", "财务专员", "人事"),
        "defaults": {"occupation_task_exposure": 72, "industry_adoption": 66, "task_standardization": 78, "verification_ease": 70, "ai_tool_fit": 74, "market_pressure": 70, "human_trust_requirement": 36, "physical_dependency": 8, "domain_knowledge": 38},
    },
    "regulated-professional": {
        "keywords": ("doctor", "lawyer", "auditor", "accountant", "therapist", "licensed", "compliance", "physician", "医生", "律师", "审计", "会计", "心理咨询", "合规", "执业"),
        "defaults": {"occupation_task_exposure": 42, "industry_adoption": 48, "task_standardization": 46, "verification_ease": 62, "ai_tool_fit": 58, "market_pressure": 40, "human_trust_requirement": 78, "physical_dependency": 30, "domain_knowledge": 70},
    },
    "physical-skilled": {
        "keywords": ("technician", "electrician", "mechanic", "construction", "field engineer", "chef", "driver", "nurse", "maintenance", "电工", "维修", "技工", "施工", "厨师", "司机", "护士", "现场", "设备"),
        "defaults": {"occupation_task_exposure": 30, "industry_adoption": 42, "task_standardization": 45, "verification_ease": 52, "ai_tool_fit": 40, "market_pressure": 42, "human_trust_requirement": 70, "physical_dependency": 88, "domain_knowledge": 68},
    },
    "relationship-sales": {
        "keywords": ("sales", "business development", "account manager", "recruiter", "broker", "agent", "consultant", "销售", "商务", "客户经理", "猎头", "经纪", "中介", "顾问"),
        "defaults": {"occupation_task_exposure": 45, "industry_adoption": 58, "task_standardization": 42, "verification_ease": 55, "ai_tool_fit": 55, "market_pressure": 58, "human_trust_requirement": 82, "physical_dependency": 18, "domain_knowledge": 62},
    },
    "management-coordination": {
        "keywords": ("product manager", "project manager", "program manager", "engineering manager", "operations manager", "manager", "产品经理", "项目经理", "主管", "经理", "负责人", "管理"),
        "defaults": {"occupation_task_exposure": 46, "industry_adoption": 62, "task_standardization": 40, "verification_ease": 58, "ai_tool_fit": 56, "market_pressure": 52, "human_trust_requirement": 80, "physical_dependency": 10, "domain_knowledge": 68},
    },
    "research-frontier": {
        "keywords": ("researcher", "scientist", "phd", "lab", "r&d", "research assistant", "scientific", "研究员", "博士", "实验室", "科研", "算法研究", "研发"),
        "defaults": {"occupation_task_exposure": 48, "industry_adoption": 60, "task_standardization": 38, "verification_ease": 70, "ai_tool_fit": 66, "market_pressure": 46, "human_trust_requirement": 58, "physical_dependency": 35, "domain_knowledge": 72},
    },
    "creator-founder": {
        "keywords": ("creator", "artist", "founder", "entrepreneur", "influencer", "indie hacker", "youtuber", "streamer", "自媒体", "创作者", "艺术家", "创业", "创始人", "主播", "博主"),
        "defaults": {"occupation_task_exposure": 55, "industry_adoption": 64, "task_standardization": 48, "verification_ease": 50, "ai_tool_fit": 70, "market_pressure": 70, "human_trust_requirement": 72, "physical_dependency": 15, "domain_knowledge": 55},
    },
    "public-institutional": {
        "keywords": ("civil servant", "government", "public sector", "state-owned", "military", "公务员", "事业单位", "政府", "国企", "央企", "军队"),
        "defaults": {"occupation_task_exposure": 34, "industry_adoption": 38, "task_standardization": 58, "verification_ease": 55, "ai_tool_fit": 46, "market_pressure": 28, "human_trust_requirement": 68, "physical_dependency": 20, "domain_knowledge": 78},
    },
    "education-training": {
        "keywords": ("teacher", "tutor", "coach", "trainer", "instructor", "professor", "教师", "老师", "家教", "教练", "培训师", "讲师"),
        "defaults": {"occupation_task_exposure": 48, "industry_adoption": 56, "task_standardization": 55, "verification_ease": 58, "ai_tool_fit": 62, "market_pressure": 55, "human_trust_requirement": 76, "physical_dependency": 22, "domain_knowledge": 60},
    },
    "care-social": {
        "keywords": ("social worker", "caregiver", "childcare", "elder care", "counselor", "community service", "社工", "护工", "养老", "育儿", "托育", "社区服务"),
        "defaults": {"occupation_task_exposure": 32, "industry_adoption": 40, "task_standardization": 44, "verification_ease": 42, "ai_tool_fit": 38, "market_pressure": 36, "human_trust_requirement": 86, "physical_dependency": 72, "domain_knowledge": 66},
    },
    "entrepreneurship-operations": {
        "keywords": ("small business", "merchant", "restaurant owner", "shop owner", "operator", "local service", "个体户", "商家", "店主", "餐饮老板", "小老板", "本地服务"),
        "defaults": {"occupation_task_exposure": 44, "industry_adoption": 55, "task_standardization": 52, "verification_ease": 58, "ai_tool_fit": 58, "market_pressure": 62, "human_trust_requirement": 76, "physical_dependency": 40, "domain_knowledge": 70},
    },
}

FAMILY_ALIASES = {
    "digital": "digital-production",
    "software": "digital-production",
    "office": "process-service",
    "admin": "process-service",
    "regulated": "regulated-professional",
    "professional": "regulated-professional",
    "physical": "physical-skilled",
    "skilled-trade": "physical-skilled",
    "sales": "relationship-sales",
    "relationship": "relationship-sales",
    "management": "management-coordination",
    "coordination": "management-coordination",
    "research": "research-frontier",
    "creator": "creator-founder",
    "founder": "creator-founder",
    "public": "public-institutional",
    "education": "education-training",
    "care": "care-social",
    "entrepreneur": "entrepreneurship-operations",
}

INDUSTRY_KEYWORDS: Tuple[Tuple[Iterable[str], int], ...] = (
    (("internet", "software", "ai", "fintech", "media", "consulting", "互联网", "软件", "金融", "媒体", "咨询"), 74),
    (("outsourcing", "bpo", "外包", "客服", "运营"), 80),
    (("education", "healthcare", "legal", "manufacturing", "教育", "医疗", "法律", "制造"), 48),
    (("public", "government", "state-owned", "公共", "政府", "国企"), 34),
    (("construction", "logistics", "restaurant", "retail", "施工", "物流", "餐饮", "零售"), 38),
)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def normalize_score(value: Any, default: float = 50.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return 100.0 if value else 0.0
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if 0.0 <= numeric <= 1.0:
        numeric *= 100.0
    elif 1.0 < numeric <= 5.0:
        numeric *= 20.0
    return clamp(numeric)


def first_score(profile: Mapping[str, Any], names: Iterable[str], default: float = 50.0) -> float:
    for name in names:
        if name in profile:
            return normalize_score(profile.get(name), default)
    return default


def text_blob(profile: Mapping[str, Any]) -> str:
    values: List[str] = []
    for key in ("role", "target_role", "industry", "region", "status", "employment_type"):
        if profile.get(key):
            values.append(str(profile[key]))
    for item in profile.get("tasks", []) or []:
        values.append(str(item))
    for item in profile.get("projects", []) or []:
        values.append(str(item))
    return " ".join(values).lower()


def keyword_score(blob: str, table: Tuple[Tuple[Iterable[str], int], ...], default: float) -> float:
    scores = [score for words, score in table if any(word.lower() in blob for word in words)]
    return float(max(scores)) if scores else default


def resolve_family_name(value: Any) -> str | None:
    if value is None:
        return None
    family = str(value).strip().lower().replace("_", "-")
    if family in OCCUPATION_FAMILIES:
        return family
    return FAMILY_ALIASES.get(family)


def classify_occupation_family(profile: Mapping[str, Any]) -> str:
    explicit = resolve_family_name(profile.get("occupation_family"))
    if explicit:
        return explicit
    blob = text_blob(profile)
    matches: List[Tuple[str, int]] = []
    for family, config in OCCUPATION_FAMILIES.items():
        score = sum(1 for word in config["keywords"] if word.lower() in blob)
        if score:
            matches.append((family, score))
    if not matches:
        digital_share = first_score(profile, ("digital_task_share", "task_ai_share"), 0.0)
        return "digital-production" if digital_share >= 65 else "process-service"
    matches.sort(key=lambda item: item[1], reverse=True)
    return matches[0][0]


def family_default(profile: Mapping[str, Any], key: str, fallback: float) -> float:
    family = classify_occupation_family(profile)
    return float(OCCUPATION_FAMILIES[family]["defaults"].get(key, fallback))


def runway_to_score(months: Any, default: float = 45.0) -> float:
    try:
        value = float(months)
    except (TypeError, ValueError):
        return default
    if value <= 0:
        return 10.0
    if value >= 18:
        return 90.0
    return clamp(10.0 + value * 4.5)


def project_proof_score(profile: Mapping[str, Any]) -> float:
    explicit = profile.get("project_proof")
    if explicit is not None:
        return normalize_score(explicit)
    count = profile.get("project_count", len(profile.get("projects", []) or []))
    shipped = profile.get("shipped_projects", 0)
    measurable = profile.get("measurable_outcomes", 0)
    try:
        count_f = float(count)
        shipped_f = float(shipped)
        measurable_f = float(measurable)
    except (TypeError, ValueError):
        return 45.0
    score = 18.0 + min(count_f, 6.0) * 7.0 + min(shipped_f, 4.0) * 9.0 + min(measurable_f, 4.0) * 7.0
    return clamp(score)


def research_score(profile: Mapping[str, Any]) -> float:
    explicit = profile.get("research_depth")
    if explicit is not None:
        return normalize_score(explicit)
    months = profile.get("research_months", 0)
    papers = profile.get("papers", 0)
    patents = profile.get("patents", 0)
    try:
        month_f = float(months)
        paper_f = float(papers)
        patent_f = float(patents)
    except (TypeError, ValueError):
        return 35.0
    return clamp(20.0 + min(month_f, 48.0) * 0.9 + min(paper_f, 5.0) * 8.0 + min(patent_f, 3.0) * 6.0)


def domain_context_score(profile: Mapping[str, Any]) -> float:
    explicit = profile.get("domain_knowledge")
    if explicit is not None:
        return normalize_score(explicit)
    months = profile.get("months_in_workforce", profile.get("work_months", 0))
    try:
        month_f = float(months)
    except (TypeError, ValueError):
        month_f = 0.0
    context = first_score(profile, ("customer_context", "organization_context", "industry_context"), family_default(profile, "domain_knowledge", 45.0))
    return clamp(25.0 + min(month_f, 96.0) * 0.35 + context * 0.35)


def score_risk_factors(raw: Mapping[str, Any]) -> Dict[str, float]:
    profile = raw.get("profile", raw)
    overrides = dict(raw.get("risk_factors", {}) or profile.get("risk_factors", {}) or {})
    blob = text_blob(profile)
    resource_buffer = runway_to_score(profile.get("runway_months"), 45.0)
    if profile.get("family_support") is not None:
        resource_buffer = clamp((resource_buffer + normalize_score(profile.get("family_support"), 50.0)) / 2.0)

    base = {
        "occupation_task_exposure": max(
            family_default(profile, "occupation_task_exposure", 52.0),
            first_score(profile, ("task_ai_share", "automatable_task_share", "digital_task_share"), family_default(profile, "occupation_task_exposure", 52.0)),
        ),
        "industry_adoption": keyword_score(blob, INDUSTRY_KEYWORDS, family_default(profile, "industry_adoption", 50.0)),
        "task_standardization": first_score(profile, ("task_standardization", "repetitive_task_share", "template_work_share"), family_default(profile, "task_standardization", 50.0)),
        "verification_ease": first_score(profile, ("verification_ease", "testability", "metric_verifiability"), family_default(profile, "verification_ease", 50.0)),
        "ai_tool_fit": first_score(profile, ("ai_tool_fit", "available_ai_tool_coverage"), family_default(profile, "ai_tool_fit", 50.0)),
        "market_pressure": first_score(profile, ("market_pressure", "outsourcing_pressure", "job_market_pressure"), family_default(profile, "market_pressure", 50.0)),
        "low_human_trust": 100.0 - first_score(profile, ("human_trust_requirement", "relationship_requirement", "leadership_requirement"), family_default(profile, "human_trust_requirement", 45.0)),
        "low_physical_dependency": 100.0 - first_score(profile, ("physical_dependency", "onsite_requirement", "equipment_dependency"), family_default(profile, "physical_dependency", 25.0)),
        "low_domain_context": 100.0 - domain_context_score(profile),
        "low_resource_buffer": 100.0 - resource_buffer,
    }
    for key, value in overrides.items():
        if key in base:
            base[key] = normalize_score(value, base[key])
    return {key: round(clamp(value), 2) for key, value in base.items()}


def score_resilience_factors(raw: Mapping[str, Any]) -> Dict[str, float]:
    profile = raw.get("profile", raw)
    overrides = dict(raw.get("resilience_factors", {}) or profile.get("resilience_factors", {}) or {})
    resource_buffer = runway_to_score(profile.get("runway_months"), 45.0)
    if profile.get("family_support") is not None:
        resource_buffer = clamp((resource_buffer + normalize_score(profile.get("family_support"), 50.0)) / 2.0)

    base = {
        "ai_collaboration": first_score(profile, ("ai_collaboration", "ai_usage_level", "ai_workflow_skill"), 45.0),
        "business_judgment": first_score(profile, ("business_judgment", "product_sense", "user_understanding"), 45.0),
        "project_proof": project_proof_score(profile),
        "learning_velocity": first_score(profile, ("learning_velocity", "learning_speed", "weekly_learning_consistency"), 50.0),
        "domain_knowledge": domain_context_score(profile),
        "communication_accountability": first_score(profile, ("communication_accountability", "ownership", "coordination"), 45.0),
        "research_depth": research_score(profile),
        "network_access": first_score(profile, ("network_access", "mentor_access", "community_access"), 40.0),
        "resource_buffer": resource_buffer,
    }
    for key, value in overrides.items():
        if key in base:
            base[key] = normalize_score(value, base[key])
    return {key: round(clamp(value), 2) for key, value in base.items()}


def weighted_score(factors: Mapping[str, float], weights: Mapping[str, float]) -> float:
    total_weight = sum(weights.values())
    return sum(factors[key] * weight for key, weight in weights.items()) / total_weight


def logistic(k: float, midpoint: float, month: int) -> float:
    return 1.0 / (1.0 + math.exp(-k * (month - midpoint)))


def risk_label(score: float) -> str:
    if score <= 20:
        return "low"
    if score <= 40:
        return "medium-low"
    if score <= 60:
        return "medium"
    if score <= 80:
        return "high"
    return "extreme"


def top_components(factors: Mapping[str, float], weights: Mapping[str, float], reverse: bool = True) -> List[Dict[str, Any]]:
    rows = []
    for key, value in factors.items():
        weight = weights.get(key, 0.0)
        rows.append({"factor": key, "score": round(value, 2), "weight": weight, "contribution": round(value * weight, 2)})
    rows.sort(key=lambda row: row["contribution"], reverse=reverse)
    return rows[:5]


def forecast_profile(raw: Mapping[str, Any], months: int = 36) -> Dict[str, Any]:
    profile = raw.get("profile", raw)
    occupation_family = classify_occupation_family(profile)
    risk_factors = score_risk_factors(raw)
    resilience_factors = score_resilience_factors(raw)
    risk_pressure = weighted_score(risk_factors, RISK_WEIGHTS)
    resilience_index = weighted_score(resilience_factors, RESILIENCE_WEIGHTS)
    learning = resilience_factors["learning_velocity"]
    ai_collab = resilience_factors["ai_collaboration"]
    proof = resilience_factors["project_proof"]
    learning_quality = ((learning + ai_collab + proof) / 3.0 - 50.0) / 50.0

    scenarios: Dict[str, List[Dict[str, float]]] = {}
    for name, params in SCENARIOS.items():
        rows: List[Dict[str, float]] = []
        for month in range(months + 1):
            adoption = logistic(params["k"], params["midpoint"], month)
            multiplier = 0.90 + adoption * (params["max_multiplier"] - 0.90)
            resilience_month = clamp(resilience_index + month * (0.10 + learning_quality * 0.45 - adoption * 0.20))
            risk_month = clamp(risk_pressure * multiplier - (resilience_month - 50.0) * 0.32)
            rows.append(
                {
                    "month": month,
                    "risk_probability": round(risk_month, 2),
                    "resilience_index": round(resilience_month, 2),
                    "adoption_intensity": round(adoption * 100.0, 2),
                }
            )
        scenarios[name] = rows

    base_start = scenarios["base"][0]["risk_probability"]
    base_end = scenarios["base"][-1]["risk_probability"]
    return {
        "metadata": {
            "horizon_months": months,
            "default_scenario": "base",
            "occupation_family": occupation_family,
            "caveat": "Scenario estimate only; not an objective fate or employment probability.",
        },
        "scores": {
            "risk_pressure": round(risk_pressure, 2),
            "resilience_index": round(resilience_index, 2),
            "current_risk_probability": base_start,
            "final_month_base_risk_probability": base_end,
            "risk_label": risk_label(base_end),
        },
        "risk_factors": risk_factors,
        "resilience_factors": resilience_factors,
        "scenarios": scenarios,
        "top_risk_sources": top_components(risk_factors, RISK_WEIGHTS),
        "top_resilience_advantages": top_components(resilience_factors, RESILIENCE_WEIGHTS),
    }


def _points(rows: List[Mapping[str, float]], key: str, width: int, height: int, left: int, top: int, months: int) -> str:
    plot_w = width - left - 60
    plot_h = height - top - 70
    coords = []
    for row in rows:
        x = left + (float(row["month"]) / months) * plot_w if months else left
        y = top + (1.0 - float(row[key]) / 100.0) * plot_h
        coords.append(f"{x:.1f},{y:.1f}")
    return " ".join(coords)


def render_svg(forecast: Mapping[str, Any], title: str = "AI replacement risk forecast") -> str:
    width, height = 960, 540
    left, top = 76, 58
    plot_w = width - left - 60
    plot_h = height - top - 70
    months = int(forecast["metadata"]["horizon_months"])
    scenarios = forecast["scenarios"]
    title_esc = html.escape(title)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#1f2937} .grid{stroke:#e5e7eb;stroke-width:1} .axis{stroke:#374151;stroke-width:1.4} .risk{fill:none;stroke:#dc2626;stroke-width:3} .res{fill:none;stroke:#2563eb;stroke-width:3} .slow,.fast{fill:none;stroke:#fca5a5;stroke-width:1.5;stroke-dasharray:5 5}",
        "</style>",
        f"<rect width='{width}' height='{height}' fill='#ffffff'/>",
        f"<text x='{left}' y='32' font-size='22' font-weight='700'>{title_esc}</text>",
        f"<text x='{left}' y='52' font-size='12'>Risk probability and anti-replacement resilience, 0-100 scale</text>",
    ]

    for value in range(0, 101, 20):
        y = top + (1 - value / 100.0) * plot_h
        parts.append(f"<line class='grid' x1='{left}' y1='{y:.1f}' x2='{left + plot_w}' y2='{y:.1f}'/>")
        parts.append(f"<text x='{left - 34}' y='{y + 4:.1f}' font-size='12' text-anchor='end'>{value}</text>")
        parts.append(f"<text x='{left + plot_w + 34}' y='{y + 4:.1f}' font-size='12'>{value}</text>")

    for month in range(0, months + 1, max(1, months // 6)):
        x = left + (month / months) * plot_w if months else left
        parts.append(f"<line class='grid' x1='{x:.1f}' y1='{top}' x2='{x:.1f}' y2='{top + plot_h}'/>")
        parts.append(f"<text x='{x:.1f}' y='{top + plot_h + 24}' font-size='12' text-anchor='middle'>{month}</text>")

    parts.extend(
        [
            f"<line class='axis' x1='{left}' y1='{top}' x2='{left}' y2='{top + plot_h}'/>",
            f"<line class='axis' x1='{left}' y1='{top + plot_h}' x2='{left + plot_w}' y2='{top + plot_h}'/>",
            f"<line class='axis' x1='{left + plot_w}' y1='{top}' x2='{left + plot_w}' y2='{top + plot_h}'/>",
            f"<text x='{left + plot_w / 2:.1f}' y='{height - 18}' font-size='13' text-anchor='middle'>Months from assessment</text>",
            f"<text x='20' y='{top + plot_h / 2:.1f}' font-size='13' transform='rotate(-90 20 {top + plot_h / 2:.1f})' text-anchor='middle'>AI replacement risk probability</text>",
            f"<text x='{width - 18}' y='{top + plot_h / 2:.1f}' font-size='13' transform='rotate(90 {width - 18} {top + plot_h / 2:.1f})' text-anchor='middle'>Anti-replacement resilience index</text>",
        ]
    )

    parts.append(f"<polyline class='slow' points='{_points(scenarios['slow'], 'risk_probability', width, height, left, top, months)}'/>")
    parts.append(f"<polyline class='fast' points='{_points(scenarios['fast'], 'risk_probability', width, height, left, top, months)}'/>")
    parts.append(f"<polyline class='risk' points='{_points(scenarios['base'], 'risk_probability', width, height, left, top, months)}'/>")
    parts.append(f"<polyline class='res' points='{_points(scenarios['base'], 'resilience_index', width, height, left, top, months)}'/>")

    legend_x = left + plot_w - 268
    parts.extend(
        [
            f"<rect x='{legend_x}' y='{top + 12}' width='250' height='74' rx='6' fill='#ffffff' stroke='#e5e7eb'/>",
            f"<line x1='{legend_x + 16}' y1='{top + 34}' x2='{legend_x + 56}' y2='{top + 34}' class='risk'/>",
            f"<text x='{legend_x + 66}' y='{top + 38}' font-size='13'>Base risk probability</text>",
            f"<line x1='{legend_x + 16}' y1='{top + 56}' x2='{legend_x + 56}' y2='{top + 56}' class='res'/>",
            f"<text x='{legend_x + 66}' y='{top + 60}' font-size='13'>Base resilience index</text>",
            f"<line x1='{legend_x + 16}' y1='{top + 76}' x2='{legend_x + 56}' y2='{top + 76}' class='slow'/>",
            f"<text x='{legend_x + 66}' y='{top + 80}' font-size='13'>Slow/fast risk bounds</text>",
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts)


def write_outputs(forecast: Mapping[str, Any], output: Path | None, svg: Path | None, title: str) -> None:
    if output:
        output.write_text(json.dumps(forecast, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if svg:
        svg.write_text(render_svg(forecast, title), encoding="utf-8")


def sample_profiles() -> Dict[str, Dict[str, Any]]:
    return {
        "junior_crud_programmer": {
            "profile": {
                "role": "junior CRUD backend programmer",
                "industry": "software outsourcing",
                "occupation_family": "digital-production",
                "months_in_workforce": 1,
                "tasks": ["CRUD features", "API wiring", "bug fixes", "documentation"],
                "project_count": 1,
                "shipped_projects": 0,
                "ai_usage_level": 45,
                "learning_velocity": 62,
                "task_ai_share": 70,
                "task_standardization": 76,
                "verification_ease": 82,
                "market_pressure": 72,
                "human_trust_requirement": 30,
                "runway_months": 4,
            }
        },
        "senior_system_owner": {
            "profile": {
                "role": "senior backend engineer and system owner",
                "industry": "internet software",
                "occupation_family": "digital-production",
                "months_in_workforce": 96,
                "tasks": ["architecture", "incident response", "mentoring", "cross-team design"],
                "project_count": 8,
                "shipped_projects": 6,
                "measurable_outcomes": 4,
                "ai_usage_level": 78,
                "learning_velocity": 70,
                "business_judgment": 82,
                "communication_accountability": 85,
                "human_trust_requirement": 80,
                "task_standardization": 42,
                "runway_months": 12,
            }
        },
        "onsite_technician": {
            "profile": {
                "role": "onsite equipment technician",
                "industry": "manufacturing maintenance",
                "occupation_family": "physical-skilled",
                "months_in_workforce": 48,
                "tasks": ["equipment diagnosis", "onsite repair", "safety inspection"],
                "project_count": 4,
                "shipped_projects": 4,
                "ai_usage_level": 38,
                "learning_velocity": 54,
                "human_trust_requirement": 72,
                "physical_dependency": 88,
                "runway_months": 8,
            }
        },
    }


def run_self_test() -> None:
    samples = sample_profiles()
    forecasts = {name: forecast_profile(profile, months=36) for name, profile in samples.items()}
    junior = forecasts["junior_crud_programmer"]["scores"]["final_month_base_risk_probability"]
    senior = forecasts["senior_system_owner"]["scores"]["final_month_base_risk_probability"]
    onsite = forecasts["onsite_technician"]["scores"]["final_month_base_risk_probability"]
    assert junior > senior, "junior CRUD sample should have higher final risk than senior owner sample"
    assert forecasts["onsite_technician"]["metadata"]["occupation_family"] == "physical-skilled"
    assert onsite < junior, "onsite technician sample should have lower final risk than junior CRUD sample"
    for forecast in forecasts.values():
        assert len(forecast["scenarios"]["base"]) == 37
        for row in forecast["scenarios"]["base"]:
            assert 0 <= row["risk_probability"] <= 100
            assert 0 <= row["resilience_index"] <= 100
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "self-test.svg"
        write_outputs(forecasts["junior_crud_programmer"], None, path, "Self-test forecast")
        assert path.exists() and "<svg" in path.read_text(encoding="utf-8")
    print("career_risk_forecast.py self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI replacement risk forecast JSON and SVG chart.")
    parser.add_argument("--input", type=Path, help="Input profile JSON.")
    parser.add_argument("--output", type=Path, help="Output forecast JSON.")
    parser.add_argument("--svg", type=Path, help="Output SVG chart.")
    parser.add_argument("--months", type=int, default=36, help="Forecast horizon in months.")
    parser.add_argument("--title", default="AI replacement risk forecast", help="SVG chart title.")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic self-test.")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return
    if not args.input:
        parser.error("--input is required unless --self-test is used")

    raw = json.loads(args.input.read_text(encoding="utf-8"))
    forecast = forecast_profile(raw, months=args.months)
    write_outputs(forecast, args.output, args.svg, args.title)
    if not args.output:
        print(json.dumps(forecast, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
