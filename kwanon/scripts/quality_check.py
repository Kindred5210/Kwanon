#!/usr/bin/env python3
"""Repository-level quality checks for Kwanon."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILL_SECTIONS = [
    "## Core Idea",
    "## Phase 0: Entry Routing",
    "## Phase 1: Progressive Interview",
    "## Phase 1.5: Profile Quality Checkpoint",
    "## Phase 2: Synthesis And Scoring",
    "## Phase 2.5: Scoring Review Checkpoint",
    "## Phase 3: Forecast And Chart",
    "## Phase 4: Quality Validation",
    "## Phase 5: Final Report",
    "## Special Cases",
    "## Never Do",
    "## Validation",
]

REQUIRED_REFERENCES = [
    "references/question-bank.md",
    "references/scoring-rubric.md",
    "references/recommendation-patterns.md",
    "references/source-notes.md",
    "references/occupation-taxonomy.md",
    "references/input-schema.md",
]

REQUIRED_SCRIPTS = [
    "scripts/career_risk_forecast.py",
    "scripts/simulate_profiles.py",
    "scripts/quality_check.py",
]

REQUIRED_CHINESE_CHART_LABELS = [
    "汝之率为ai更替",
    "距今月数",
    "为AI更替之率",
    "抗替之力",
    "本策更替率",
    "本策抗替力",
    "缓急二势边界",
]

FORBIDDEN_INTAKE_PHRASES = [
    "Current AI usage in real work or study",
    "How do you currently use AI tools in real work or study",
    "Ask at most 7 questions",
]

FORBIDDEN_CHART_PHRASES = [
    "观音·AI替代风险推演",
    "自测推演",
    "CHINESE_TITLES",
    "风险推演",
]

REQUIRED_CALIBRATION_TERMS = [
    "spread_risk_probability",
    "apply_anchor_calibration",
    "detect_calibration_anchor",
    "senior_clinical_doctor",
    "hr_admin_clerk",
    "calibration_anchor",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def check_frontmatter(skill_md: Path) -> None:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        fail("SKILL.md missing YAML frontmatter")
    lines = [line for line in match.group(1).splitlines() if line.strip()]
    keys = [line.split(":", 1)[0] for line in lines]
    if keys != ["name", "description"]:
        fail(f"SKILL.md frontmatter keys must be name, description; got {keys}")
    name = lines[0].split(":", 1)[1].strip()
    desc = lines[1].split(":", 1)[1].strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        fail(f"invalid skill name: {name}")
    if len(name) > 64:
        fail("skill name too long")
    if not desc or len(desc) > 1024 or "<" in desc or ">" in desc:
        fail("description is empty, too long, or contains angle brackets")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Kwanon skill structure.")
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory.")
    args = parser.parse_args()

    skill_dir = args.skill_dir
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        fail("SKILL.md not found")
    check_frontmatter(skill_md)
    text = skill_md.read_text(encoding="utf-8")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            fail(f"missing section: {section}")
    if "## Voice Protocol" not in text:
        fail("missing Voice Protocol section")
    if "exactly 3 questions" not in text or "简历" not in text:
        fail("skill must document resume-first and three-question intake")
    if "阿弥陀佛，善哉善哉！" not in text:
        fail("skill must enforce the fixed first sentence")
    if "汝之率为ai更替" not in text:
        fail("skill must document the fixed anonymous SVG title")
    for phrase in FORBIDDEN_INTAKE_PHRASES:
        if phrase in text:
            fail(f"forbidden old intake phrase remains in SKILL.md: {phrase}")
    for rel_path in REQUIRED_REFERENCES + REQUIRED_SCRIPTS:
        if not (skill_dir / rel_path).exists():
            fail(f"missing required file: {rel_path}")
    chart_script = (skill_dir / "scripts/career_risk_forecast.py").read_text(encoding="utf-8")
    for label in REQUIRED_CHINESE_CHART_LABELS:
        if label not in chart_script:
            fail(f"missing Chinese chart label: {label}")
    for term in REQUIRED_CALIBRATION_TERMS:
        if term not in chart_script:
            fail(f"missing calibration term in forecast script: {term}")
    simulate_script = (skill_dir / "scripts/simulate_profiles.py").read_text(encoding="utf-8")
    for term in ("senior_clinical_doctor", "hr_admin_clerk"):
        if term not in simulate_script:
            fail(f"missing calibration sample in simulation script: {term}")
    for phrase in FORBIDDEN_CHART_PHRASES:
        if phrase in chart_script or phrase in simulate_script:
            fail(f"forbidden chart title phrase remains: {phrase}")
    if "DEFAULT_CHART_TITLE" not in simulate_script:
        fail("simulation script must use the shared anonymous chart title")
    question_bank = (skill_dir / "references/question-bank.md").read_text(encoding="utf-8")
    if "ask exactly these 3 questions" not in question_bank or "Do not ask for a usage rate" not in question_bank:
        fail("question bank must enforce three-question intake without AI usage-rate questioning")
    rubric = (skill_dir / "references/scoring-rubric.md").read_text(encoding="utf-8")
    for term in ("Probability Spread And Anchors", "senior_clinical_doctor", "hr_admin_clerk"):
        if term not in rubric:
            fail(f"missing calibration rubric term: {term}")
    taxonomy = (skill_dir / "references/occupation-taxonomy.md").read_text(encoding="utf-8")
    if taxonomy.count("|") < 80:
        fail("occupation taxonomy looks too thin")
    print("quality_check.py passed")


if __name__ == "__main__":
    main()
