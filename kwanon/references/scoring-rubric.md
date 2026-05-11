# Scoring Rubric

All factors use 0-100. A higher risk factor raises replacement pressure. A higher resilience factor lowers risk and raises the anti-replacement curve. Start with occupation-family defaults from `occupation-taxonomy.md`, then override them with actual task evidence from the user.

Do not ask for AI usage rate or AI usage percentage during the intake interview. Score AI collaboration from resume evidence, project artifacts, workflow ownership, review/test habits, automation, or voluntary statements. If evidence is missing, keep the script's conservative default instead of inventing a score.

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
| ai_collaboration | 0.18 | User can use, test, evaluate, and integrate AI or automation into real workflows; infer from evidence, not from a forced usage-rate question. |
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

## Probability Spread And Anchors

The script first computes raw monthly risk, then spreads the probability away from the middle so low, medium, and high cases are easier to distinguish. It preserves the same 0-100 output fields.

Transparent anchors override the spread only when evidence is strong:

| Anchor | Trigger | Intended Range |
|---|---|---:|
| senior_clinical_doctor | Clinical doctor/physician, >=120 months in workforce, high trust, high physical/site dependency, high domain context. | 0-10 |
| hr_admin_clerk | HR/human resources clerical/admin assistant work, high standardization, high verification ease, high AI tool fit, low trust, low physical dependency. | 90-100 |

If an anchor applies, the forecast includes `metadata.calibration_anchor`. Explain the anchor as direct replacement pressure, not judgment of the person.

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
- A resume can justify many scores without follow-up questions. Ask only for the missing fields that materially change the curve or advice.
