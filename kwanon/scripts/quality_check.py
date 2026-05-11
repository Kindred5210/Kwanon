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
    for rel_path in REQUIRED_REFERENCES + REQUIRED_SCRIPTS:
        if not (skill_dir / rel_path).exists():
            fail(f"missing required file: {rel_path}")
    taxonomy = (skill_dir / "references/occupation-taxonomy.md").read_text(encoding="utf-8")
    if taxonomy.count("|") < 80:
        fail("occupation taxonomy looks too thin")
    print("quality_check.py passed")


if __name__ == "__main__":
    main()
