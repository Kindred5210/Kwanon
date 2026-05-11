---
name: kwanon
description: Use when the user wants an interactive assessment of AI replacement risk or career resilience based on their biography, projects, work history, time in society, research experience, family/resource constraints, and goals; ask staged questions, estimate month-by-month future AI replacement risk and anti-replacement resilience curves, then provide practical life and career advice.
---

# Kwanon

> This skill estimates pressure and resilience. It does not judge a person's worth or predict destiny.

## Core Idea

A useful AI replacement forecast is not a job-title lookup. It is a task-and-evidence assessment:

- What work does the person actually do?
- Which parts can AI perform, accelerate, or cheapen?
- Which parts require trust, judgment, responsibility, physical presence, or domain context?
- What evidence shows the person can adapt faster than the role changes?
- What constraints shape the safest next move?

Output a transparent scenario estimate: a month-by-month AI replacement risk probability curve, a month-by-month anti-replacement resilience index curve, uncertainty notes, and practical advice.

## Phase 0: Entry Routing

Classify the request before asking questions.

| User Input | Route | Action |
|---|---|---|
| Clear self-assessment request | Direct assessment | Start Phase 1 essential interview. |
| Vague anxiety or career confusion | Diagnosis | Ask 1-2 questions to locate role, concern, and time horizon, then assess. |
| User provides structured profile JSON | Script-first | Validate fields against `references/input-schema.md`, then run forecast. |
| User wants latest industry/job-market data | Evidence refresh | Verify current high-quality sources before scoring market assumptions. |
| User wants to evaluate another person | Consent caution | Avoid sensitive or invasive claims; use only provided professional evidence. |

If the user is visibly anxious, reduce intensity: ask fewer questions, avoid extreme labels in the first response, and focus on the next controllable step.

## Phase 1: Progressive Interview

Use `references/question-bank.md`. Start with at most 7 questions:

1. Current role or target role.
2. Country/city and industry.
3. Time since entering society or working.
4. Weekly task mix and rough percentages.
5. Strongest projects, papers, products, or proof of ability.
6. Current AI usage in real work or study.
7. Transition window and weekly learning/building time.

After the first answer, map the role to an occupation family using `references/occupation-taxonomy.md`. If the role is hybrid, ask which family consumes more weekly time.

Do not collect sensitive details unless they affect timing or recommendations. Let the user answer "skip" or "unknown".

## Phase 1.5: Profile Quality Checkpoint

Before scoring, summarize what is known and what is missing:

```text
Profile checkpoint
- Occupation family: ...
- Strongest evidence: ...
- Highest-uncertainty field: ...
- Sensitive fields skipped: ...
- Enough to score? yes/no
```

Continue only when the profile has enough evidence for a useful estimate. If not, ask 1-3 targeted follow-ups. Do not turn the interview into a long form.

## Phase 2: Synthesis And Scoring

Use two layers:

- Occupation family defaults from `references/occupation-taxonomy.md`.
- User-specific overrides from actual tasks, projects, AI skill, research depth, market pressure, and resource constraints.

Risk side:

- Occupation task exposure.
- Industry adoption speed.
- Task standardization.
- Verification ease.
- AI tool fit.
- Market pressure.
- Low human trust requirement.
- Low physical dependency.
- Low domain context.
- Low resource buffer.

Resilience side:

- AI collaboration.
- Business judgment.
- Project proof.
- Learning velocity.
- Domain knowledge.
- Communication and accountability.
- Research depth.
- Network access.
- Resource buffer.

Use `references/scoring-rubric.md` for factor definitions. Use `references/input-schema.md` when converting answers into JSON.

## Phase 2.5: Scoring Review Checkpoint

If the assessment is high-stakes, sparse, or likely to surprise the user, show a compact scoring preview before finalizing:

```text
Scoring preview
- Risk pressure drivers: ...
- Resilience drivers: ...
- Main assumption: ...
- Confidence: low/medium/high
```

If the user corrects a major assumption, update the profile before charting.

## Phase 3: Forecast And Chart

When a structured profile is available, run:

```bash
python3 scripts/career_risk_forecast.py --input profile.json --output forecast.json --svg risk_chart.svg --months 36
```

Default behavior:

- Horizon: 36 months unless the user specifies otherwise.
- Scenarios: slow, base, fast AI adoption.
- Chart: SVG with base risk probability, base resilience index, and slow/fast risk bounds.
- Scale: 0-100 on both axes.

If tools are unavailable, compute the same structure manually and provide a Markdown table with monthly or quarterly points.

## Phase 4: Quality Validation

Before answering, run a self-check:

| Check | Pass Standard | Fail Signal |
|---|---|---|
| Task-based | Risk is explained by task mix, not title alone. | "Programmer = high risk" with no task evidence. |
| Evidence-based | Projects/research/resources are tied to scores. | Scores appear out of nowhere. |
| Sensitive-safe | Family/background affect runway only. | Background treated as ability or worth. |
| Scenario-honest | Caveat and uncertainty are explicit. | Single exact probability presented as truth. |
| Actionable | Every major risk has an action. | Advice is generic encouragement. |
| Occupation-aware | Family-specific factors are considered. | Physical, regulated, or trust-heavy work scored like office work. |

Use `scripts/quality_check.py` for repository validation after editing the skill files.

## Phase 5: Final Report

Produce the final answer in this order:

1. One-sentence caveat: this is a scenario estimate, not destiny.
2. Chart or chart path, with axes clearly labeled.
3. Current assessment: occupation family, risk pressure, resilience, confidence.
4. Top risk sources.
5. Top resilience advantages.
6. Action plan:
   - Next 2 weeks.
   - Next 1-2 months.
   - Next 3-6 months.
7. Review cadence: reassess in 3-6 months, or sooner after a major role/project change.

Encouragement must be grounded in evidence. Do not use empty comfort.

## Special Cases

### Sparse Information

If the user provides little detail, output a low-confidence preliminary estimate and ask targeted follow-ups. Never fill gaps with invented biography.

### All Occupations

This skill covers broad occupation families rather than every title. For rare roles, decompose tasks by time share and score from tasks first.

### Regulated Professions

Separate documentation automation from accountable professional judgment. Medical, legal, audit, therapy, and education roles often face AI augmentation before full replacement.

### Physical Or Care Work

Do not overstate near-term replacement where work depends on site access, hands, equipment, safety, or human presence. Look for AI pressure in scheduling, diagnosis support, documentation, quoting, training, and customer communication.

### Creator Or Founder Work

AI may reduce production cost while increasing the importance of taste, distribution, brand, trust, capital, and speed of iteration.

### Evaluating Others

Do not infer private background, mental health, class, or family conditions. Use only professional evidence provided by the user, and frame the result as scenario pressure, not a judgment.

## Never Do

- Do not claim objective certainty.
- Do not output "you will be replaced" as a verdict.
- Do not use family background, age, gender, city origin, or school prestige as destiny.
- Do not recommend extreme life decisions from one assessment.
- Do not hide uncertainty to sound confident.
- Do not produce a chart without explaining the assumptions behind it.

## Validation

After editing this skill, validate:

```bash
python3 scripts/career_risk_forecast.py --self-test
python3 scripts/simulate_profiles.py --seed 20260509 --count 5
python3 scripts/quality_check.py .
python3 /Users/Kiddo/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

If `quick_validate.py` cannot run because `PyYAML` is missing, run an equivalent manual frontmatter check and record the limitation.
