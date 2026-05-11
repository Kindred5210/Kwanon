#!/usr/bin/env python3
"""Generate deterministic sample profiles and validate the forecast model."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List

from career_risk_forecast import forecast_profile, write_outputs


ARCHETYPES: List[Dict[str, Any]] = [
    {
        "name": "junior_crud_programmer",
        "profile": {
            "role": "junior CRUD programmer",
            "industry": "software outsourcing",
            "occupation_family": "digital-production",
            "months_in_workforce": 1,
            "research_months": 0,
            "tasks": ["CRUD features", "API integration", "bug fixes"],
            "project_count": 1,
            "shipped_projects": 0,
            "task_ai_share": 72,
            "task_standardization": 78,
            "verification_ease": 82,
            "ai_usage_level": 45,
            "learning_velocity": 64,
            "market_pressure": 74,
            "human_trust_requirement": 28,
            "physical_dependency": 0,
            "runway_months": 4,
        },
    },
    {
        "name": "senior_system_owner",
        "profile": {
            "role": "senior backend engineer system owner",
            "industry": "internet software",
            "occupation_family": "digital-production",
            "months_in_workforce": 108,
            "tasks": ["architecture", "incident response", "mentoring", "stakeholder alignment"],
            "project_count": 9,
            "shipped_projects": 7,
            "measurable_outcomes": 5,
            "task_ai_share": 42,
            "task_standardization": 38,
            "verification_ease": 75,
            "ai_usage_level": 82,
            "learning_velocity": 72,
            "business_judgment": 85,
            "communication_accountability": 88,
            "human_trust_requirement": 85,
            "domain_knowledge": 84,
            "runway_months": 12,
        },
    },
    {
        "name": "research_heavy_candidate",
        "profile": {
            "role": "machine learning research assistant",
            "industry": "university research",
            "occupation_family": "research-frontier",
            "months_in_workforce": 12,
            "research_months": 30,
            "papers": 2,
            "tasks": ["literature review", "experiments", "paper writing", "model evaluation"],
            "project_count": 3,
            "shipped_projects": 1,
            "task_ai_share": 58,
            "task_standardization": 48,
            "verification_ease": 68,
            "ai_usage_level": 76,
            "learning_velocity": 82,
            "business_judgment": 42,
            "communication_accountability": 56,
            "human_trust_requirement": 58,
            "runway_months": 6,
        },
    },
    {
        "name": "content_design_freelancer",
        "profile": {
            "role": "content designer and video editor freelancer",
            "industry": "media content",
            "occupation_family": "creator-founder",
            "months_in_workforce": 36,
            "tasks": ["short video editing", "copywriting", "thumbnail design", "client communication"],
            "project_count": 12,
            "shipped_projects": 10,
            "measurable_outcomes": 3,
            "task_ai_share": 78,
            "task_standardization": 64,
            "verification_ease": 58,
            "ai_usage_level": 70,
            "learning_velocity": 68,
            "business_judgment": 62,
            "communication_accountability": 74,
            "human_trust_requirement": 62,
            "market_pressure": 78,
            "runway_months": 5,
        },
    },
    {
        "name": "onsite_technician",
        "profile": {
            "role": "onsite equipment technician",
            "industry": "manufacturing maintenance",
            "occupation_family": "physical-skilled",
            "months_in_workforce": 48,
            "tasks": ["equipment diagnosis", "onsite repair", "safety inspection", "customer explanation"],
            "project_count": 4,
            "shipped_projects": 4,
            "task_ai_share": 25,
            "task_standardization": 45,
            "verification_ease": 52,
            "ai_usage_level": 38,
            "learning_velocity": 54,
            "business_judgment": 58,
            "communication_accountability": 70,
            "human_trust_requirement": 72,
            "physical_dependency": 88,
            "domain_knowledge": 70,
            "runway_months": 8,
        },
    },
    {
        "name": "regulated_lawyer",
        "profile": {
            "role": "junior lawyer",
            "industry": "legal services",
            "occupation_family": "regulated-professional",
            "months_in_workforce": 24,
            "tasks": ["legal research", "contract review", "client communication", "court preparation"],
            "project_count": 5,
            "shipped_projects": 3,
            "task_ai_share": 55,
            "task_standardization": 45,
            "verification_ease": 62,
            "ai_usage_level": 58,
            "learning_velocity": 65,
            "business_judgment": 62,
            "communication_accountability": 76,
            "human_trust_requirement": 84,
            "domain_knowledge": 66,
            "runway_months": 6,
        },
    },
    {
        "name": "relationship_sales_owner",
        "profile": {
            "role": "enterprise account manager",
            "industry": "b2b software sales",
            "occupation_family": "relationship-sales",
            "months_in_workforce": 60,
            "tasks": ["account research", "relationship maintenance", "negotiation", "proposal writing"],
            "project_count": 6,
            "shipped_projects": 6,
            "measurable_outcomes": 4,
            "task_ai_share": 52,
            "task_standardization": 40,
            "verification_ease": 58,
            "ai_usage_level": 66,
            "learning_velocity": 64,
            "business_judgment": 78,
            "communication_accountability": 84,
            "human_trust_requirement": 88,
            "domain_knowledge": 70,
            "runway_months": 7,
        },
    },
    {
        "name": "public_institutional_admin",
        "profile": {
            "role": "public sector administrative staff",
            "industry": "government public sector",
            "occupation_family": "public-institutional",
            "months_in_workforce": 72,
            "tasks": ["policy documents", "approval process", "coordination", "public service records"],
            "project_count": 3,
            "shipped_projects": 3,
            "task_ai_share": 48,
            "task_standardization": 62,
            "verification_ease": 55,
            "ai_usage_level": 42,
            "learning_velocity": 48,
            "business_judgment": 55,
            "communication_accountability": 70,
            "human_trust_requirement": 72,
            "domain_knowledge": 80,
            "runway_months": 10,
        },
    },
    {
        "name": "education_training_teacher",
        "profile": {
            "role": "high school teacher",
            "industry": "education",
            "occupation_family": "education-training",
            "months_in_workforce": 84,
            "tasks": ["lesson planning", "classroom teaching", "student feedback", "parent communication"],
            "project_count": 5,
            "shipped_projects": 5,
            "task_ai_share": 45,
            "task_standardization": 52,
            "verification_ease": 58,
            "ai_usage_level": 48,
            "learning_velocity": 56,
            "business_judgment": 58,
            "communication_accountability": 82,
            "human_trust_requirement": 84,
            "physical_dependency": 28,
            "domain_knowledge": 70,
            "runway_months": 8,
        },
    },
    {
        "name": "care_social_worker",
        "profile": {
            "role": "elder care social worker",
            "industry": "community care",
            "occupation_family": "care-social",
            "months_in_workforce": 42,
            "tasks": ["home visits", "case notes", "family communication", "resource coordination"],
            "project_count": 3,
            "shipped_projects": 3,
            "task_ai_share": 32,
            "task_standardization": 44,
            "verification_ease": 42,
            "ai_usage_level": 35,
            "learning_velocity": 52,
            "business_judgment": 55,
            "communication_accountability": 78,
            "human_trust_requirement": 90,
            "physical_dependency": 74,
            "domain_knowledge": 68,
            "runway_months": 5,
        },
    },
    {
        "name": "small_business_operator",
        "profile": {
            "role": "local restaurant owner",
            "industry": "restaurant local service",
            "occupation_family": "entrepreneurship-operations",
            "months_in_workforce": 96,
            "tasks": ["store operations", "supplier negotiation", "staff scheduling", "local marketing"],
            "project_count": 4,
            "shipped_projects": 4,
            "measurable_outcomes": 3,
            "task_ai_share": 42,
            "task_standardization": 52,
            "verification_ease": 60,
            "ai_usage_level": 40,
            "learning_velocity": 56,
            "business_judgment": 78,
            "communication_accountability": 82,
            "human_trust_requirement": 80,
            "physical_dependency": 60,
            "domain_knowledge": 78,
            "runway_months": 4,
        },
    },
]


def jitter_profile(profile: Dict[str, Any], rng: random.Random) -> Dict[str, Any]:
    cloned = json.loads(json.dumps(profile))
    for key, value in list(cloned["profile"].items()):
        if isinstance(value, (int, float)) and key not in {"months_in_workforce", "research_months", "project_count", "shipped_projects", "papers"}:
            cloned["profile"][key] = max(0, min(100, round(value + rng.uniform(-4, 4), 2)))
    return cloned


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate sample AI replacement risk profiles.")
    parser.add_argument("--seed", type=int, default=20260509)
    parser.add_argument("--count", type=int, default=len(ARCHETYPES))
    parser.add_argument("--months", type=int, default=36)
    parser.add_argument("--output-dir", type=Path, default=Path("/private/tmp/ai-replacement-risk-forecaster-sim"))
    args = parser.parse_args()

    rng = random.Random(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    for idx in range(args.count):
        archetype = ARCHETYPES[idx % len(ARCHETYPES)]
        raw = jitter_profile({"profile": archetype["profile"]}, rng)
        forecast = forecast_profile(raw, months=args.months)
        stem = f"{idx + 1:02d}-{archetype['name']}"
        json_path = args.output_dir / f"{stem}.json"
        svg_path = args.output_dir / f"{stem}.svg"
        write_outputs(forecast, json_path, svg_path, f"{archetype['name']} forecast")
        summaries.append(
            {
                "name": archetype["name"],
                "occupation_family": forecast["metadata"]["occupation_family"],
                "current_risk": forecast["scores"]["current_risk_probability"],
                "month_end_risk": forecast["scores"]["final_month_base_risk_probability"],
                "resilience": forecast["scores"]["resilience_index"],
                "risk_label": forecast["scores"]["risk_label"],
                "svg": str(svg_path),
            }
        )

    print(json.dumps({"seed": args.seed, "count": args.count, "output_dir": str(args.output_dir), "summaries": summaries}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
