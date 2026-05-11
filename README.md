# AI Replacement Risk Forecaster

`ai-replacement-risk-forecaster` is a Codex skill for structured, interview-style career risk assessment in the AI era. It estimates two month-by-month curves:

- AI replacement risk probability.
- Anti-replacement resilience index.

The forecast is a transparent scenario estimate, not a claim about destiny, personal worth, or an objective employment probability.

## What It Does

- Interviews the user progressively instead of asking for a long form all at once.
- Maps the user's role into broad occupation families, then adjusts by actual task mix and biography.
- Considers projects, shipped work, research time, work history, AI usage, family/resource constraints, and goals.
- Generates JSON forecast data and an SVG dual-axis line chart using only Python standard library.
- Gives concrete career advice for the next 2 weeks, 1-2 months, and 3-6 months.

## Repository Layout

```text
.
├── ai-replacement-risk-forecaster/
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
cp -R ai-replacement-risk-forecaster ~/.codex/skills/
```

Restart Codex, then invoke:

```text
$ai-replacement-risk-forecaster
```

## Run The Forecast Script

```bash
python3 ai-replacement-risk-forecaster/scripts/career_risk_forecast.py \
  --input examples/profiles/junior-crud-programmer.json \
  --output /tmp/forecast.json \
  --svg /tmp/forecast.svg \
  --months 36
```

Run built-in validation:

```bash
python3 ai-replacement-risk-forecaster/scripts/career_risk_forecast.py --self-test
python3 ai-replacement-risk-forecaster/scripts/simulate_profiles.py --seed 20260509 --count 5
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

## Safety Notes

- The model is heuristic and transparent by design.
- Family background and financial buffer are used only to tailor transition timing and support recommendations.
- The output should not be used for hiring, firing, lending, insurance, admission, or other consequential decisions about another person.
- Users should reassess every 3-6 months because AI capability, market adoption, and personal skill growth can change quickly.

## License

MIT
