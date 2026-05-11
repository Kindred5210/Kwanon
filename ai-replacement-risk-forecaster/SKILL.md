---
name: ai-replacement-risk-forecaster
description: Use when the user wants an interactive assessment of AI replacement risk or career resilience based on their biography, projects, work history, time in society, research experience, family/resource constraints, and goals; ask staged questions, estimate month-by-month future AI replacement risk and anti-replacement resilience curves, then provide practical life and career advice.
---

# AI Replacement Risk Forecaster

## Purpose

Estimate a user's AI replacement risk as a transparent scenario forecast, not as fate, personality diagnosis, or social ranking. Use the user's actual projects, work and social timeline, research experience, task structure, AI usage, family/resource constraints, and goals to produce:

- A month-by-month AI replacement risk probability curve.
- A month-by-month anti-replacement resilience index curve.
- A concise explanation, uncertainty notes, and actionable advice.

## Operating Rules

- Ask progressively. Start with no more than 7 questions, then follow up only when the answer materially changes the forecast.
- Let users skip sensitive questions. Treat family background and finances only as resource and timing constraints; never use them to judge personal worth.
- Prefer ranges and scenarios over false precision. If information is sparse, say so and widen uncertainty.
- Do not present the result as an objective employment probability. Say it is a structured estimate based on current information and assumptions.
- Pair every risk conclusion with an action the user can take.
- If the user asks for latest market or industry data, verify current official or high-quality sources before relying on dated assumptions.

## Workflow

1. Clarify forecast horizon, defaulting to 36 months when unspecified.
2. Interview the user in stages using `references/question-bank.md`.
3. Map the role to an occupation family using `references/occupation-taxonomy.md`; if the role is hybrid, score the dominant task family and mention the secondary family.
4. Convert answers into factor scores using `references/scoring-rubric.md`.
5. Use three reasoning roles:
   - Main agent: manage the conversation, decide what is missing, and produce the final report.
   - Data/model agent: assess AI development speed, occupation exposure, industry adoption, and uncertainty.
   - Report agent: turn scores, chart, and evidence into a clear final answer.
6. If real subagents are available and the user explicitly requested multi-agent work, delegate those roles. Otherwise perform the roles sequentially.
7. When enough structured data exists, run `scripts/career_risk_forecast.py` to generate forecast JSON and an SVG chart.
8. Provide advice using `references/recommendation-patterns.md`.

## Interview Stages

Collect enough information to score the model. Do not ask all stages at once.

- Baseline: role, target role, industry, city/country, current status, years/months since entering society.
- Work content: weekly task mix, repetitive work, creative/judgment work, communication, responsibility, physical or licensed work.
- Projects: shipped projects, personal role, users/customers, measurable outcomes, code/reports/papers/portfolio links if available.
- Research: months spent in research, topic, papers, patents, experiments, grants, lab or advisor context.
- AI usage: tools used, workflows automated, ability to verify AI output, prompt/tool-building ability.
- Learning and transfer: recent learning evidence, English/document reading, programming/data/product/business breadth.
- Resources: time available each week, living-expense buffer, family support or constraints, mentors/network, acceptable transition timeline.
- Goals: defend current path, pivot to safer adjacent roles, or pursue high-growth/high-risk roles.

## Occupation Coverage

This skill is intended to work across broad occupation families, not by memorizing every job title. Use `references/occupation-taxonomy.md` when the role is outside common software, content, research, or office-work examples. The taxonomy covers:

- Digital production and software work.
- Process service and administrative work.
- Professional regulated work.
- Physical, on-site, and skilled trades.
- Relationship, sales, and brokerage work.
- Management, product, and coordination work.
- Research, science, and creative frontier work.
- Personal brand, creator, and founder work.

If the user has a rare role, decompose it into task percentages and score from tasks first.

## Scoring And Forecast

Use `references/scoring-rubric.md` for factor definitions and `references/occupation-taxonomy.md` for family defaults. The main split is:

- Risk side: occupation task exposure, industry adoption speed, task standardization, verification ease, AI tool fit, market pressure.
- Resilience side: AI collaboration ability, business judgment, project proof, learning velocity, domain knowledge, communication/accountability, research depth, network and resource buffer.

Default output:

- Horizon: 36 months.
- Scenarios: slow, base, fast AI adoption; base is the default line for the SVG.
- Y axis: 0-100 for both risk probability and resilience index.
- X axis: month number from 0 to horizon.

Run the script when a structured profile is available:

```bash
python3 scripts/career_risk_forecast.py --input profile.json --output forecast.json --svg risk_chart.svg --months 36
```

If tool execution is unavailable, compute the same fields manually and render a Markdown table or Mermaid-style line data.

The script accepts either explicit factor scores or a compact profile. A compact profile can include `role`, `industry`, `tasks`, `months_in_workforce`, `research_months`, `project_count`, `shipped_projects`, `ai_usage_level`, `learning_velocity`, `runway_months`, and optional `occupation_family`.

## Final Report Format

Produce the final answer in this order:

1. One-sentence caveat: this is a scenario estimate, not destiny.
2. The chart or chart file path, with axes clearly labeled.
3. Current assessment: task exposure, resilience, main assumptions.
4. Top risk sources.
5. Top resilience advantages.
6. Action plan:
   - Next 2 weeks.
   - Next 1-2 months.
   - Next 3-6 months.
7. Encouraging but concrete closing: emphasize controllable actions and next review date.

Avoid empty comfort. Encouragement should be tied to evidence, such as existing project proof, learning speed, or a concrete improvement path.

## Validation

Validate the skill after edits:

```bash
python3 scripts/career_risk_forecast.py --self-test
python3 scripts/simulate_profiles.py --seed 20260509 --count 5
python3 /Users/Kiddo/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

If `quick_validate.py` cannot run because `PyYAML` is missing, run an equivalent manual frontmatter check and record the limitation.
