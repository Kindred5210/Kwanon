# Scoring Rubric

All factors use 0-100. A higher risk factor raises replacement pressure. A higher resilience factor lowers risk and raises the anti-replacement curve. Start with occupation-family defaults from `occupation-taxonomy.md`, then override them with actual task evidence from the user.

## Risk Factors

| Factor | Weight | High Score Means |
|---|---:|---|
| occupation_task_exposure | 0.30 | Core tasks are text, code, analysis, design, data entry, support, or other AI-friendly digital work. |
| industry_adoption | 0.12 | The industry has budget, data, tools, and pressure to adopt AI quickly. |
| task_standardization | 0.12 | Work follows repeatable procedures or templates. |
| verification_ease | 0.10 | Output can be cheaply tested, reviewed, benchmarked, or accepted by metrics. |
| ai_tool_fit | 0.08 | Current AI tools already map well to the user's task shape. |
| market_pressure | 0.08 | The role faces outsourcing, price pressure, layoffs, or oversupply. |
| low_human_trust | 0.07 | Work needs little trust, negotiation, leadership, or accountability. |
| low_physical_dependency | 0.05 | Work has little on-site, equipment, or physical-world dependency. |
| low_domain_context | 0.04 | Work has little proprietary, customer, organizational, or field-specific context. |
| low_resource_buffer | 0.04 | User has little time or financial buffer to adapt. |

## Resilience Factors

| Factor | Weight | High Score Means |
|---|---:|---|
| ai_collaboration | 0.18 | User can use, test, evaluate, and integrate AI into real workflows. |
| business_judgment | 0.16 | User understands goals, constraints, tradeoffs, users, and value creation. |
| project_proof | 0.14 | User has inspectable shipped work, papers, demos, customers, or measurable results. |
| learning_velocity | 0.14 | User repeatedly learns new tools or domains and reduces repeated mistakes. |
| domain_knowledge | 0.12 | User has context AI cannot easily infer: industry, customer, lab, product, or system history. |
| communication_accountability | 0.10 | User can coordinate, explain, own outcomes, and earn trust. |
| research_depth | 0.06 | User can formulate problems, run experiments, analyze uncertainty, and write clearly. |
| network_access | 0.05 | User has mentors, peers, customers, recruiters, community, or family network. |
| resource_buffer | 0.05 | User has time, money, housing, hardware, or emotional support to adapt. |

## Scenario Parameters

Use an S curve for AI adoption:

```text
adoption(t) = L / (1 + exp(-k * (t - midpoint)))
```

Defaults:

| Scenario | k per month | midpoint | max multiplier |
|---|---:|---:|---:|
| slow | 0.035 | 54 | 1.15 |
| base | 0.060 | 36 | 1.35 |
| fast | 0.095 | 24 | 1.65 |

## Risk Bands

| Score | Label | Meaning |
|---:|---|---|
| 0-20 | Low | Short-term impact is mainly tool augmentation. |
| 21-40 | Medium-low | Some tasks may be reorganized or repriced. |
| 41-60 | Medium | Active adaptation is needed. |
| 61-80 | High | The role structure may shrink or change materially. |
| 81-100 | Extreme | Prepare a migration plan and reduce exposure quickly. |

## Interpretation

- Experience protects only when it creates judgment, context, network, or responsibility. Repeating the same simple task for years should not be overvalued.
- Family and money should affect schedule, risk tolerance, and runway. They must not be used as a proxy for intelligence, dignity, or worth.
- A high-risk score can still be acceptable if resilience rises faster than exposure.
- For all occupations, task mix outranks title. A "manager" doing only reporting may be more exposed than a "technician" solving messy site problems.
