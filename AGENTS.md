# AGENTS.md — AI Agents & Pipelines

## Overview
AI-powered agents and automation pipelines — **183 agents** across **16 categories**.

---

## 🧠 AI Agent Frameworks (`ai-frameworks/`)
| Directory | Framework | Tech |
|-----------|-----------|------|
| `autogen-agent/` | AutoGen | Python |
| `crewai-agent/` | CrewAI | Python |
| `langchain-agent/` | LangChain | Python |

---

## 🔍 Code Quality & Review (`code-quality/`)
| Directory | Description |
|-----------|-------------|
| `code-reviewer/` | AI code review agent |
| `code-review-automator/` | Automated PR review pipeline |
| `bug-triager/` | Bug classification & prioritization |
| `bug-triager-auto/` | Automated bug triage pipeline |

---

## 🧪 Testing & QA (`testing-qa/`)
| Directory | Description |
|-----------|-------------|
| `test-generator/` | Unit test writer |
| `qa-test-generator/` | Cypress/Playwright E2E test generator |

---

## 📝 Documentation (`documentation/`)
| Directory | Description |
|-----------|-------------|
| `doc-writer/` | Parse AST, generate docstrings & READMEs |
| `documentation-writer-bot/` | Scan codebases, generate/update docs |
| `changelog-writer/` | Automated changelog generation |

---

## ✉️ Communication & Email (`communication/`)
| Directory | Description |
|-----------|-------------|
| `email-drafter/` | Context-aware email response bot |
| `email-triage-assistant/` | Categorize, summarize, and draft replies |

---

## 🎙️ Meetings & Notes (`meetings/`)
| Directory | Description |
|-----------|-------------|
| `meeting-summarizer/` | Transcript processor |
| `meeting-notes-organizer/` | Extract tasks, update PM tools |

---

## 🔬 Research & Data (`research-data/`)
| Directory | Description |
|-----------|-------------|
| `research-summarizer-agent/` | Deep research agent |
| `data-analyst/` | CSV/Excel insight generator |
| `sql-query-builder-agent/` | Natural language to SQL |

---

## 📣 Content & Marketing (`content-marketing/`)
| Directory | Description |
|-----------|-------------|
| `social-media-manager-agent/` | Social content management |
| `resume-tailor-agent/` | Resume/CV tailoring |

---

## 🔧 Codebase Fixers (`fixers/`)
| Directory | Description |
|-----------|-------------|
| `api-breaking-change-detect/` | Detect breaking API changes |
| `code-style-enforcer-bot/` | Enforce code style |
| `css-dead-code-remover/` | Remove unused CSS |
| `dependency-bloat-reducer/` | Reduce dependency bloat |
| `deprecation-hunter/` | Find deprecated API usage |
| `doc-drift-fixer/` | Fix outdated documentation |
| `i18n-missing-key-finder/` | Find missing i18n keys |
| `log-noise-reducer/` | Reduce noisy logs |
| `unused-asset-cleaner/` | Clean up unused assets |
| `vuln-auto-patcher/` | Auto-patch vulnerabilities |

---

## 🏗️ DevOps & Infrastructure (`devops-infra/`) — NEW
| Directory | Description |
|-----------|-------------|
| `incident-responder/` | Log monitoring & incident reports |
| `ci-pipeline-optimizer/` | CI/CD bottleneck analysis |
| `docker-compose-generator/` | Auto-generate Docker configs |
| `infra-cost-analyzer/` | Cloud billing waste detector |
| `env-file-auditor/` | Secret & env var scanner |
| `migration-planner/` | Database migration planning |
| `uptime-monitor-agent/` | Endpoint uptime monitoring |
| `release-notes-generator/` | Git-based release notes |
| `terraform-reviewer/` | IaC security review |
| `log-analyzer/` | Log pattern analysis |

---

## 🔒 Security & Privacy (`security-privacy/`) — NEW
| Directory | Description |
|-----------|-------------|
| `secret-scanner/` | Leaked API key detector |
| `license-compliance-checker/` | Dependency license auditor |
| `phishing-email-detector/` | Phishing email analyzer |
| `privacy-policy-generator/` | GDPR/CCPA policy generator |
| `permission-auditor/` | Excessive permission detector |
| `password-strength-analyzer/` | Auth implementation reviewer |
| `cors-config-validator/` | CORS misconfiguration checker |
| `dependency-vulnerability-monitor/` | CVE monitoring & auto-fix |

---

## 📊 Data & Analytics (`data-analytics/`) — NEW
| Directory | Description |
|-----------|-------------|
| `csv-cleaner/` | Messy CSV fixer |
| `json-schema-generator/` | JSON to schema inferrer |
| `database-diagram-generator/` | ERD generator (Mermaid/PlantUML) |
| `data-faker-agent/` | Realistic seed data generator |
| `regex-builder/` | Natural language to regex |
| `api-response-mocker/` | Mock API server generator |
| `spreadsheet-formula-writer/` | English to Excel formulas |
| `data-pipeline-validator/` | ETL integrity checker |
| `chart-generator-agent/` | Data to chart code generator |
| `log-to-metrics-converter/` | Logs to Prometheus/Grafana |

---

## 🤖 AI & ML Ops (`ai-ml-ops/`) — NEW
| Directory | Description |
|-----------|-------------|
| `prompt-optimizer/` | Prompt A/B testing |
| `model-benchmark-runner/` | Multi-model benchmarking |
| `training-data-generator/` | Synthetic data generation |
| `rag-evaluator/` | RAG pipeline quality tester |
| `llm-cost-calculator/` | Token usage cost tracker |
| `embedding-explorer/` | Vector embedding visualizer |
| `fine-tune-dataset-curator/` | Fine-tuning data formatter |
| `ai-hallucination-detector/` | Fabrication fact-checker |

---

## 🌐 API & Integration (`api-integration/`) — NEW
| Directory | Description |
|-----------|-------------|
| `api-doc-generator/` | OpenAPI spec generator |
| `webhook-tester/` | Webhook endpoint logger |
| `graphql-schema-analyzer/` | GraphQL N+1 detector |
| `rest-to-graphql-converter/` | REST to GraphQL migrator |
| `api-rate-limit-tester/` | Rate limit mapper |
| `oauth-flow-debugger/` | OAuth 2.0 flow tracer |
| `api-changelog-differ/` | API version differ |
| `postman-to-code-converter/` | Collection to code |

---

## ✍️ Content & Writing (`content-writing/`) — NEW
| Directory | Description |
|-----------|-------------|
| `blog-post-writer/` | SEO blog writer |
| `readme-generator/` | Project README scaffolder |
| `technical-blog-reviewer/` | Article accuracy checker |
| `tutorial-generator/` | Library tutorial creator |
| `copy-editor-agent/` | Grammar & style checker |
| `press-release-writer/` | Press release formatter |
| `tweet-thread-writer/` | Long-form to Twitter threads |
| `newsletter-curator/` | Tech news aggregator |
| `proposal-writer/` | Project proposal generator |
| `sop-generator/` | SOP documentation writer |

---

## 💼 Business & Productivity (`business-productivity/`) — NEW
| Directory | Description |
|-----------|-------------|
| `invoice-generator-agent/` | PDF invoice creator |
| `contract-analyzer/` | Contract risk highlighter |
| `competitive-analysis-agent/` | Competitor research |
| `okr-tracker/` | OKR management & reports |
| `standup-report-generator/` | Git-based standups |
| `timesheet-analyzer/` | Time tracking insights |
| `expense-categorizer/` | Transaction categorizer |
| `meeting-scheduler-agent/` | Cross-timezone scheduler |
| `kpi-dashboard-generator/` | KPI dashboard creator |
| `sla-monitor/` | SLA compliance tracker |

---

## 🎨 Design & Frontend (`design-frontend/`) — NEW
| Directory | Description |
|-----------|-------------|
| `color-palette-generator/` | Color scheme creator |
| `responsive-design-tester/` | Multi-viewport tester |
| `accessibility-auditor/` | WCAG compliance checker |
| `design-token-extractor/` | Design to CSS variables |
| `icon-set-generator/` | AI icon set creator |
| `component-documenter/` | UI component docs |
| `image-alt-text-writer/` | Alt text generator |
| `ui-copy-reviewer/` | UI text reviewer |

---

## 🎓 Learning & Education (`learning-education/`) — NEW
| Directory | Description |
|-----------|-------------|
| `flashcard-generator/` | Anki flashcard creator |
| `code-explainer/` | Line-by-line code explainer |
| `quiz-generator/` | Quiz & assessment creator |
| `learning-path-planner/` | Skill roadmap planner |
| `paper-summarizer/` | Academic paper summarizer |
| `interview-prep-agent/` | Interview question generator |

---

## 🔄 File & Format Conversion (`file-conversion/`) — NEW
| Directory | Description |
|-----------|-------------|
| `markdown-to-pdf-agent/` | MD to styled PDF |
| `csv-to-api-agent/` | CSV to REST API server |
| `html-to-markdown-converter/` | HTML to clean Markdown |
| `yaml-json-converter/` | YAML ↔ JSON converter |
| `sql-to-nosql-migrator/` | SQL to MongoDB migrator |
| `swagger-to-typescript/` | OpenAPI to TypeScript types |
| `figma-to-css-agent/` | Figma to production CSS |
| `video-to-transcript/` | Audio/video transcriber |

---

## 🏠 Personal & Lifestyle (`personal-lifestyle/`) — NEW
| Directory | Description |
|-----------|-------------|
| `recipe-planner/` | Meal plan generator |
| `travel-itinerary-agent/` | Trip planner |
| `habit-coach/` | Habit tracker & coach |
| `journaling-prompt-agent/` | Daily journaling prompts |
| `gift-recommendation-agent/` | Gift idea suggester |
| `workout-planner/` | Fitness plan creator |

---

## 🛠️ Code Generation & Scaffolding (`code-generation/`) — NEW
| Directory | Description |
|-----------|-------------|
| `boilerplate-generator/` | Project scaffold creator |
| `crud-api-generator/` | Schema to CRUD API |
| `type-generator/` | JSON to TypeScript/Python types |
| `migration-file-writer/` | ORM migration generator |
| `config-file-generator/` | ESLint/Prettier/TSConfig |
| `monorepo-setup-agent/` | Monorepo scaffolder |
| `github-actions-writer/` | CI/CD workflow generator |
| `dockerfile-optimizer/` | Docker image optimizer |

---

## Conventions
- Use virtual environments (venv or poetry)
- Store API keys in `.env` files
- Implement logging for all agent actions
- Include retry logic for API calls

## Testing
- **Framework:** pytest
- Test agent logic, tool functions, and prompt chains
- Mock LLM API calls and external services
- Place tests in `tests/` folder
- Target ≥80% code coverage

## Boundaries
- NEVER hardcode API keys
- NEVER make destructive actions without confirmation
