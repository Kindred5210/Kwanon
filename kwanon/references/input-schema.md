# Input Schema

The forecast script accepts a JSON object with either a top-level `profile` object or profile fields at the top level.

The interactive skill can also accept a resume, CV, biography, project list, or local file path. The agent should extract a structured profile before asking follow-ups. Supported human inputs include pasted text, Markdown, TXT, PDF, and DOCX paths.

## Minimal Profile

```json
{
  "profile": {
    "role": "junior backend programmer",
    "industry": "software outsourcing",
    "tasks": ["CRUD features", "API integration", "bug fixes"],
    "months_in_workforce": 1,
    "project_count": 1,
    "shipped_projects": 0,
    "learning_velocity": 64,
    "runway_months": 4
  }
}
```

## Optional Fields

Use 0-100 scores unless noted.

| Field | Meaning |
|---|---|
| occupation_family | One taxonomy family, such as `digital-production` or `physical-skilled`. |
| target_role | Role the user wants next. |
| region | Country/city or labor market. |
| status | student, job seeker, employee, freelancer, founder, researcher, etc. |
| employment_type | full-time, intern, contractor, outsourced, public-sector, etc. |
| research_months | Months spent doing meaningful research. |
| papers / patents | Count of papers or patents. |
| project_count | Inspectable project count. |
| shipped_projects | Projects used by real users, deployed, published, sold, or accepted. |
| measurable_outcomes | Projects with metrics, revenue, users, citations, benchmarks, or visible impact. |
| task_ai_share | Approximate percentage of tasks AI can already assist or perform. |
| task_standardization | How repetitive or template-driven the work is. |
| verification_ease | How easy it is to verify output quality. |
| ai_tool_fit | How closely current AI/automation tools fit the user's tasks. |
| ai_usage_level | Optional structured score for AI collaboration skill if the user already provides it. Do not ask for this as an intake usage-rate question. |
| business_judgment | Ability to connect work to users, money, risk, and tradeoffs. |
| communication_accountability | Ability to own outcomes, coordinate, explain, and earn trust. |
| human_trust_requirement | How much trust, negotiation, relationship, or accountability the work requires. |
| physical_dependency | How much the role depends on on-site work, equipment, hands, or safety. |
| domain_knowledge | Proprietary, customer, industry, organizational, or field context. |
| runway_months | Months of living-expense runway. |
| family_support | Optional 0-100 resource support score, not a worth or ability score. |

## Calibration Anchors

`months_in_workforce`, `human_trust_requirement`, `physical_dependency`, `domain_knowledge`, `task_standardization`, `verification_ease`, and `ai_tool_fit` can trigger transparent anchors:

- `senior_clinical_doctor`: 10+ years of clinical medical work with high trust, physical/site dependency, and domain context.
- `hr_admin_clerk`: standardized HR clerical/admin work with high verification and tool fit, low trust requirement, and low physical dependency.

When an anchor applies, output metadata includes `calibration_anchor`; existing risk curve keys stay unchanged.

## Overrides

Advanced users can pass explicit factors:

```json
{
  "profile": {
    "role": "field technician",
    "occupation_family": "physical-skilled"
  },
  "risk_factors": {
    "occupation_task_exposure": 22
  },
  "resilience_factors": {
    "domain_knowledge": 80
  }
}
```
