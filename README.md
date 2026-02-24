# 🧠 AI Agents Hub

192 AI automation agents built with Python & Streamlit.

🌐 **[Live Demo →](https://aiagents-edycu-dev.streamlit.app/)**

## API Keys Required

| Key | Agents | Get It |
|-----|--------|--------|
| ⭐ `OPENAI_API_KEY` | 79 agents | [platform.openai.com](https://platform.openai.com/api-keys) |
| `GEMINI_API_KEY` | 13 agents | [aistudio.google.com](https://aistudio.google.com/apikey) |
| `GITHUB_TOKEN` | 6 agents | [github.com/settings/tokens](https://github.com/settings/tokens) |
| `ANTHROPIC_API_KEY` | 1 agent | [console.anthropic.com](https://console.anthropic.com/) |
| `FIGMA_ACCESS_TOKEN` | 1 agent | [figma.com/developers](https://www.figma.com/developers/api#access-tokens) |
| `SERPAPI_API_KEY` | 1 agent | [serpapi.com](https://serpapi.com/manage-api-key) |
| `PAGERDUTY_API_KEY` | 1 agent | [pagerduty.com](https://support.pagerduty.com/main/docs/api-access-keys) |

> **103 agents require no API key** — they work offline with pure logic.

## Categories

| Category | Agents | Key Required |
|----------|--------|-------------|
| 🤖 AI & ML Ops | 8 | `OPENAI_API_KEY` |
| 🔌 API Integration | 8 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 💼 Business | 10 | `OPENAI_API_KEY` |
| ⚡ Code Generation | 8 | `OPENAI_API_KEY` |
| ✅ Code Quality | 5 | `OPENAI_API_KEY`, `GITHUB_TOKEN` |
| ✍️ Content Writing | 19 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 📊 Data Analytics | 26 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 🎨 Design & Frontend | 10 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 🏗️ DevOps & Infra | 21 | `OPENAI_API_KEY`, `GEMINI_API_KEY`, `PAGERDUTY_API_KEY` |
| 📝 Documentation | 5 | `OPENAI_API_KEY` |
| 📁 File Conversion | 11 | `OPENAI_API_KEY`, `GEMINI_API_KEY`, `FIGMA_ACCESS_TOKEN` |
| 🔧 Fixers | 10 | `OPENAI_API_KEY`, `GITHUB_TOKEN` |
| 📚 Education | 6 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 🌟 Lifestyle | 6 | `OPENAI_API_KEY`, `GEMINI_API_KEY`, `SERPAPI_API_KEY` |
| 🔒 Security | 15 | `OPENAI_API_KEY`, `GEMINI_API_KEY` |
| 📦 Misc | 14 | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` |

## Run the Hub

```bash
pip install streamlit
streamlit run app.py
```

## Why Streamlit?

> **Right tool for the right job.** The Agents Hub runs Python agents — Streamlit is purpose-built for that. The portfolio site needs SEO and custom design — Next.js on Vercel is purpose-built for that.

### Why Agents Hub uses Streamlit (not Vercel)

| Reason | Streamlit | Next.js on Vercel |
|--------|-----------|-------------------|
| **Python-native** | Agents are Python scripts — runs them natively | Needs separate Python backend for every agent |
| **Interactive REPL** | `st.text_area` → run Python → display result, 1 file | Custom API layer + React frontend needed |
| **Rapid prototyping** | 1 file (`app.py`) = full app with sidebar, tabs, state | Multiple files: components, API routes, state |
| **Free hosting** | Streamlit Community Cloud — free, auto-deploy | Vercel free tier limits serverless execution |
| **Data science** | Direct access to pandas, numpy, matplotlib | Requires API bridge to Python |

### Why the Portfolio Site uses Next.js (not Streamlit)

| Reason | Next.js | Streamlit |
|--------|---------|-----------|
| **SEO** | SSR, meta tags, sitemaps — Google indexes it | SPA with no SSR, invisible to search engines |
| **Custom design** | Full CSS, animations, layout control | Limited to Streamlit's widget system |
| **Performance** | Static pages load in milliseconds | WebSocket connection overhead |
| **Routing** | Clean URLs (`/en/web`, `/id/mobile`) | Only query params (`?agent=xyz`) |
| **i18n** | Proper `[locale]/` routing with middleware | Sidebar dropdown |
