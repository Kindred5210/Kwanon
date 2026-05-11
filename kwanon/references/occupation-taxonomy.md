# Occupation Taxonomy

Use this taxonomy to cover most occupations without enumerating every job title. First identify the dominant task family, then adjust by the user's actual task percentages, seniority, project proof, and constraints.

## Family Selection Rules

- Prefer actual task mix over job title.
- For hybrid roles, choose the family that consumes the most time and mention the second family.
- If the role is rare, map each task to a family and average by time share.
- If the user provides explicit factor scores or detailed task percentages, those override family defaults.
- Do not treat family, class background, age, or city origin as destiny. Use them only for resources, constraints, and timing.

## Occupation Families

| Family | Typical Roles | Default Risk | Default Resilience Levers | Key Follow-Ups |
|---|---|---:|---|---|
| digital-production | Programmers, analysts, designers, writers, translators, editors, data workers | 68 | AI workflow skill, project proof, system ownership, domain context | What shipped artifact proves ability? Can you verify AI output? |
| process-service | Customer support, admin, operations, HR ops, finance ops, document review | 72 | Workflow ownership, customer context, process improvement, compliance knowledge | How much work follows templates? Can you redesign the process? |
| regulated-professional | Doctors, lawyers, auditors, accountants, teachers, therapists, licensed finance | 42 | License, accountability, trust, institution, client relationship, judgment | What decisions require legal or professional responsibility? |
| physical-skilled | Technicians, electricians, mechanics, nurses, construction, chefs, drivers, field engineers | 30 | Physical presence, equipment skill, safety, customer trust, local scarcity | Which tasks require hands, site access, equipment, or safety ownership? |
| relationship-sales | Sales, BD, account managers, recruiters, agents, brokers, consultants | 45 | Trust, negotiation, network, market insight, deal ownership | Do you own relationships and revenue, or only prepare materials? |
| management-coordination | Product managers, project managers, engineering managers, operations managers | 46 | Prioritization, conflict resolution, strategy, accountability, cross-team influence | What decisions do you own? What happens if you are absent? |
| research-frontier | Researchers, PhD students, scientists, lab engineers, R&D staff | 48 | Problem formulation, experiment design, publication, proprietary data, rigor | Does the work create new knowledge or mainly summarize known work? |
| creator-founder | Creators, artists, founders, indie hackers, personal brands | 55 | Audience, brand, distribution, taste, capital, speed, product-market learning | Is value from production volume, taste, audience trust, or business model? |
| public-institutional | Civil service, public sector, state-owned institutions, military-adjacent admin | 34 | Institutional rules, credential gates, local process knowledge, stability | Is promotion/risk driven by market productivity or institutional rules? |
| education-training | Tutors, teachers, coaches, course creators, corporate trainers | 48 | Student trust, pedagogy, credential, community, live feedback | Is work standardized content delivery or deep coaching/accountability? |
| care-social | Social work, elder care, childcare, counseling support, community service | 32 | Human presence, empathy, safety, trust, local regulation | Which parts are documentation vs direct care and responsibility? |
| entrepreneurship-operations | Small business owners, merchants, restaurant operators, local service owners | 44 | Local execution, supplier/customer network, capital, operations, speed | Which tasks are owner judgment vs routine admin/marketing? |

## Family Defaults For Scripts

Use these defaults when a script or agent has only a role/title and sparse details:

| Family | exposure | industry_adoption | standardization | verification | ai_tool_fit | market_pressure | human_trust | physical_dependency | domain_context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| digital-production | 68 | 72 | 62 | 75 | 78 | 64 | 38 | 5 | 42 |
| process-service | 72 | 66 | 78 | 70 | 74 | 70 | 36 | 8 | 38 |
| regulated-professional | 42 | 48 | 46 | 62 | 58 | 40 | 78 | 30 | 70 |
| physical-skilled | 30 | 42 | 45 | 52 | 40 | 42 | 70 | 88 | 68 |
| relationship-sales | 45 | 58 | 42 | 55 | 55 | 58 | 82 | 18 | 62 |
| management-coordination | 46 | 62 | 40 | 58 | 56 | 52 | 80 | 10 | 68 |
| research-frontier | 48 | 60 | 38 | 70 | 66 | 46 | 58 | 35 | 72 |
| creator-founder | 55 | 64 | 48 | 50 | 70 | 70 | 72 | 15 | 55 |
| public-institutional | 34 | 38 | 58 | 55 | 46 | 28 | 68 | 20 | 78 |
| education-training | 48 | 56 | 55 | 58 | 62 | 55 | 76 | 22 | 60 |
| care-social | 32 | 40 | 44 | 42 | 38 | 36 | 86 | 72 | 66 |
| entrepreneurship-operations | 44 | 55 | 52 | 58 | 58 | 62 | 76 | 40 | 70 |

## Family-Specific Interpretation

- Digital and process roles can be high risk even when the person is smart; the defense is moving from execution to ownership, evaluation, and workflow design.
- Regulated and care roles often face documentation automation before full role replacement.
- Physical roles may face AI-assisted diagnosis, scheduling, training, and robotics pressure, but near-term replacement is slower when the work is site-specific and safety-critical.
- Relationship and management roles are safer when the user owns decisions, revenue, trust, and accountability; they are exposed when they only generate documents or coordinate simple status updates.
- Creator and founder roles are highly unequal: AI lowers production cost but raises the importance of taste, distribution, audience trust, and strategy.
