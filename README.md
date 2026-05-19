# Kwanon
此之skill可预测汝之ai更替之率 ，投简历即可

**观音 Kwanon** is a Codex skill for structured, interview-style career risk assessment in the AI era. It speaks in a readable wenyan/semi-classical 观音-style Chinese voice and estimates two month-by-month curves:

- AI replacement risk probability.
- Anti-replacement resilience index.

The forecast is a transparent scenario estimate, not a claim about destiny, personal worth, or an objective employment probability.

## What It Does

- Interviews the user progressively instead of asking for a long form all at once.
- Starts every skill response with `阿弥陀佛，善哉善哉！`.
- Uses a resume-first intake path when the user provides a CV, biography, or project list.
- If no resume is provided, starts with only three essential questions.
- Maps the user's role into broad occupation families, then adjusts by actual task mix and biography.
- Considers projects, shipped work, research time, work history, inferred tool/workflow evidence, family/resource constraints, and goals.
- Spreads risk curves so low, middle, and high cases are visually distinct, with transparent anchors for senior clinical doctors and HR admin clerks.
- Generates JSON forecast data and an anonymous Chinese SVG dual-axis line chart using only Python standard library.
- Gives concrete career advice for the next 2 weeks, 1-2 months, and 3-6 months.

## Repository Layout

```text
.
├── kwanon/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── examples/profiles/
├── .github/workflows/test.yml
├── LICENSE
└── README.md
```

## Install

Copy the skill folder into your Codex skills directory:

```bash
cp -R kwanon ~/.codex/skills/
```

Restart Codex, then invoke:

```text
$kwanon
```

`$kwanon` is the official Codex skill call because skill machine names must use lowercase English letters, digits, and hyphens. The user-facing name is **观音 Kwanon**, so natural-language requests such as "用观音评估我" are also covered by the skill description.

Example prompts:

```text
$kwanon 这是我的简历，请据此评估我未来 36 个月的 AI 取代风险与抗替代力。
```

```text
$kwanon 我没有简历，请只问我三问，然后给出中文图表和行动建议。
```

```text
$kwanon 请用观音的半文言口吻评估我的职业风险，不要问我 AI 使用率。
```

Kwanon should keep non-proper user-facing words in readable wenyan or semi-classical Chinese. Technical names such as `AI`, `Codex`, `Python`, `JSON`, `SVG`, file paths, commands, numbers, and role names may remain unchanged for clarity.

## Run The Forecast Script

```bash
python3 kwanon/scripts/career_risk_forecast.py \
  --input examples/profiles/junior-crud-programmer.json \
  --output /tmp/forecast.json \
  --svg /tmp/forecast.svg \
  --months 36
```

The SVG chart uses the fixed anonymous title `汝之率为ai更替`; do not put a person's name, resume name, sample name, or occupation title in the visible chart title. Visible labels include `距今月数`, `为AI更替之率`, and `抗替之力`.

Run built-in validation:

```bash
python3 kwanon/scripts/career_risk_forecast.py --self-test
python3 kwanon/scripts/simulate_profiles.py --seed 20260509 --count 5
python3 kwanon/scripts/quality_check.py kwanon
```

## Occupation Coverage

The skill covers broad occupation families rather than trying to enumerate every job title:

- Digital production and software work.
- Process service and administrative work.
- Regulated professional work.
- Physical, on-site, and skilled trades.
- Relationship, sales, and brokerage work.
- Management, product, and coordination work.
- Research and frontier knowledge work.
- Personal brand, creator, and founder work.
- Public or institutional roles.
- Education, training, care, and local operations.

For rare roles, the skill decomposes the user's weekly tasks and scores from the task mix.

## Skill Structure

The skill uses a phase-based workflow:

1. Entry routing.
2. Progressive interview.
3. Profile quality checkpoint.
4. Synthesis and scoring.
5. Scoring review checkpoint.
6. Forecast and chart generation.
7. Quality validation.
8. Final report.

This keeps the assessment explainable and prevents the model from jumping straight to a pseudo-precise score.

## Safety Notes

- The model is heuristic and transparent by design.
- Family background and financial buffer are used only to tailor transition timing and support recommendations.
- The output should not be used for hiring, firing, lending, insurance, admission, or other consequential decisions about another person.
- Users should reassess every 3-6 months because AI capability, market adoption, and personal skill growth can change quickly.

## License

MIT
