"""
🧠 AI Agents Hub — Browse & Run 180+ AI Automation Agents
Built by Jules AI • Powered by Streamlit
"""

import streamlit as st
import os
from pathlib import Path

# Load .env file locally (on Streamlit Cloud, st.secrets handles this)
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agents Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    .stApp { font-family: 'Inter', sans-serif; }

    /* Hero */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7, #ec4899, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .hero-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* Category badges */
    .cat-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px 4px;
        background: rgba(168, 85, 247, 0.15);
        color: #a855f7;
    }

    /* Agent card */
    .agent-card {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        background: rgba(255,255,255,0.03);
        transition: all 0.2s;
    }
    .agent-card:hover {
        border-color: rgba(168,85,247,0.4);
        background: rgba(168,85,247,0.05);
    }
    .agent-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f3f4f6;
        margin-bottom: 4px;
    }
    .agent-desc {
        font-size: 0.85rem;
        color: #9ca3af;
        line-height: 1.4;
    }

    /* Stats */
    .stat-box {
        text-align: center;
        padding: 16px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.3);
    }

    /* Code viewer */
    .code-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #a855f7;
        margin-bottom: 8px;
    }

    div[data-testid="stVerticalBlock"] > div { gap: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ──────────────────────────────────────────────────
CATEGORY_META = {
    "ai-ml-ops": ("🤖", "AI & ML Ops", "Machine learning operations and AI infrastructure"),
    "api-integration": ("🔌", "API Integration", "API connectors and integration tools"),
    "business-productivity": ("💼", "Business", "Business automation and productivity"),
    "code-generation": ("⚡", "Code Generation", "Automated code generation tools"),
    "code-quality": ("✅", "Code Quality", "Code analysis, linting, and quality tools"),
    "content-writing": ("✍️", "Content", "Content creation and writing assistance"),
    "data-analytics": ("📊", "Data Analytics", "Data processing and analytics"),
    "design-frontend": ("🎨", "Design", "UI/UX design and frontend tools"),
    "devops-infra": ("🏗️", "DevOps", "Infrastructure and DevOps automation"),
    "documentation": ("📝", "Documentation", "Documentation generation and management"),
    "file-conversion": ("📁", "File Conversion", "File format conversion tools"),
    "fixers": ("🔧", "Fixers", "Code and configuration fixers"),
    "learning-education": ("📚", "Education", "Learning and educational tools"),
    "misc": ("🎯", "Miscellaneous", "Various utility agents"),
    "personal-lifestyle": ("🌟", "Lifestyle", "Personal productivity and lifestyle"),
    "security-privacy": ("🔒", "Security", "Security analysis and privacy tools"),
}

BASE_DIR = Path(__file__).parent


# ─── Discovery ──────────────────────────────────────────────────
@st.cache_data
def discover_agents():
    """Discover all agents by scanning the directory structure."""
    agents = {}
    for cat_dir in sorted(BASE_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith(('.', '_')):
            continue
        if cat_dir.name in ('__pycache__', 'node_modules', '.git'):
            continue

        cat_name = cat_dir.name

        # Handle misc subcategories
        if cat_name == "misc":
            for sub_cat in sorted(cat_dir.iterdir()):
                if not sub_cat.is_dir() or sub_cat.name.startswith('.'):
                    continue
                for agent_dir in sorted(sub_cat.iterdir()):
                    if not agent_dir.is_dir():
                        continue
                    main_py = agent_dir / "main.py"
                    agents_md = agent_dir / "AGENTS.md"
                    if main_py.exists() or agents_md.exists():
                        desc = _extract_desc(agents_md) if agents_md.exists() else ""
                        agents[f"misc/{sub_cat.name}/{agent_dir.name}"] = {
                            "name": _slug_to_name(agent_dir.name),
                            "category": f"misc/{sub_cat.name}",
                            "category_display": f"Misc — {_slug_to_name(sub_cat.name)}",
                            "path": str(agent_dir),
                            "has_main": main_py.exists(),
                            "description": desc,
                        }
            continue

        # Check if this is a category (has agent subdirectories)
        icon, display, cat_desc = CATEGORY_META.get(cat_name, ("📦", _slug_to_name(cat_name), ""))

        for agent_dir in sorted(cat_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue
            main_py = agent_dir / "main.py"
            agents_md = agent_dir / "AGENTS.md"
            if main_py.exists() or agents_md.exists():
                desc = _extract_desc(agents_md) if agents_md.exists() else ""
                agents[f"{cat_name}/{agent_dir.name}"] = {
                    "name": _slug_to_name(agent_dir.name),
                    "category": cat_name,
                    "category_display": f"{icon} {display}",
                    "path": str(agent_dir),
                    "has_main": main_py.exists(),
                    "description": desc,
                }

    return agents


def _slug_to_name(slug: str) -> str:
    acronyms = {"ai", "api", "css", "csv", "dns", "html", "http", "ip", "json",
                "jwt", "llm", "ml", "npm", "pdf", "qa", "rag", "rss", "seo",
                "sql", "ssh", "ssl", "svg", "ui", "url", "ux", "xml", "yaml",
                "sop", "cors", "cli", "crm", "readme", "ci", "cd"}
    words = slug.replace("-", " ").replace("_", " ").split()
    return " ".join(w.upper() if w.lower() in acronyms else w.capitalize() for w in words)


def _extract_desc(agents_md: Path) -> str:
    try:
        content = agents_md.read_text(encoding="utf-8")
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---") and len(line) > 20:
                clean = line.lstrip("- *>").strip()
                return clean[:200]
    except Exception:
        pass
    return ""


# ─── Main App ──────────────────────────────────────────────────
def main():
    agents = discover_agents()
    categories = sorted(set(a["category"] for a in agents.values()))

    # Sidebar
    with st.sidebar:
        if st.button("🧠 AI Agents Hub", type="tertiary"):
            st.query_params.clear()
            st.rerun()
        st.markdown(f"**{len(agents)}** agents · **{len(categories)}** categories")
        st.divider()

        # Category filter
        selected_cat = st.selectbox(
            "📂 Category",
            ["All"] + categories,
            format_func=lambda x: x if x == "All" else CATEGORY_META.get(x, ("📦", _slug_to_name(x), ""))[1] + f" ({sum(1 for a in agents.values() if a['category'] == x)})"
        )

        # Clear agent selection when category changes
        if "prev_cat" not in st.session_state:
            st.session_state.prev_cat = selected_cat
        if selected_cat != st.session_state.prev_cat:
            st.session_state.prev_cat = selected_cat
            if "agent" in st.query_params:
                del st.query_params["agent"]
                st.rerun()

        # Search
        search = st.text_input("🔍 Search agents", placeholder="e.g. hallucination, code, PDF...")

        # Clear agent selection when search changes
        if search and "agent" in st.query_params:
            del st.query_params["agent"]
            st.rerun()

        st.divider()
        st.markdown(
            "<div style='text-align:center;color:#6b7280;font-size:0.8rem'>"
            "Built with ♥ by <a href='https://edycu.dev' style='color:#a855f7'>edycu.dev</a>"
            "</div>",
            unsafe_allow_html=True
        )

    # Filter agents
    if search:
        # Search across ALL agents regardless of category
        search_lower = search.lower()
        filtered = {k: v for k, v in agents.items()
                    if search_lower in v["name"].lower()
                    or search_lower in v["description"].lower()
                    or search_lower in v["category_display"].lower()
                    or search_lower in k.lower()}
    elif selected_cat != "All":
        filtered = {k: v for k, v in agents.items() if v["category"] == selected_cat}
    else:
        filtered = agents

    # Check if an agent is selected
    query_params = st.query_params
    selected_agent = query_params.get("agent", None)

    if selected_agent and selected_agent in agents:
        _render_agent_detail(agents[selected_agent], selected_agent)
    else:
        _render_hub(filtered, agents)


def _render_hub(filtered, all_agents):
    """Render the main hub/catalog view."""
    # Hero
    total_count = len(all_agents)
    st.markdown('<h1 class="hero-title">AI Agents Hub</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="hero-subtitle">Browse & explore {total_count}+ AI automation agents — '
        'code review, data analysis, content generation, DevOps, and more</p>',
        unsafe_allow_html=True
    )

    # Stats
    total = len(all_agents)
    built = sum(1 for a in all_agents.values() if a["has_main"])
    cats = len(set(a["category"] for a in all_agents.values()))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{total}</div><div class="stat-label">Total Agents</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{built}</div><div class="stat-label">Ready to Run</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{cats}</div><div class="stat-label">Categories</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # Results count
    if len(filtered) < len(all_agents):
        st.info(f"Showing **{len(filtered)}** of {len(all_agents)} agents")

    # Agent grid
    items = list(filtered.items())
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j >= len(items):
                break
            key, agent = items[i + j]
            with col:
                icon = CATEGORY_META.get(agent["category"], ("📦",))[0]
                status = "✅" if agent["has_main"] else "📋"

                with st.container(border=True):
                    st.markdown(f"**{icon} {agent['name']}**")
                    if agent["description"]:
                        st.caption(agent["description"][:120] + ("..." if len(agent["description"]) > 120 else ""))
                    else:
                        st.caption(f"Category: {agent['category_display']}")

                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"{status} {'Built' if agent['has_main'] else 'Spec'}")
                    with c2:
                        if agent["has_main"]:
                            if st.button("View →", key=f"view_{key}", use_container_width=True):
                                st.query_params["agent"] = key
                                st.rerun()


def _get_agent_hint(agent):
    """Return (placeholder, label, example) based on agent name keywords."""
    name = agent.get("name", "").lower()
    text = name

    hints = [
        (["email", "triage", "inbox", "newsletter"],
         "Paste email text here...", "📧 Paste Email",
         "Subject: Q3 Budget Review Meeting\n\nHi Team,\n\nPlease review the attached Q3 budget proposal before Friday. We need to finalize the marketing spend and decide on the new hire allocation. The board meeting is next Tuesday.\n\nAlso, can someone follow up on the vendor contract renewal? It expires end of month.\n\nThanks,\nSarah"),
        (["sql", "database", "query", "schema", "migration"],
         "Paste SQL or describe your query...", "🗄️ SQL / Query",
         "SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as revenue\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nWHERE o.created_at > '2024-01-01'\nGROUP BY u.name\nHAVING COUNT(o.id) > 5\nORDER BY revenue DESC\nLIMIT 20;"),
        (["contract", "legal", "compliance"],
         "Paste contract or legal text...", "⚖️ Legal Text",
         "Section 5.2 - Limitation of Liability: The Provider shall not be liable for any indirect, incidental, consequential, or punitive damages arising from this Agreement, regardless of whether such damages were foreseeable. The Provider's total aggregate liability shall not exceed the fees paid by Client in the twelve (12) months preceding the claim. This limitation applies to the fullest extent permitted by applicable law."),
        (["resume", "interview", "job", "career"],
         "Paste resume or job description...", "💼 Career Content",
         "Senior Full-Stack Developer | 5 years experience\n\nSkills: React, Node.js, Python, PostgreSQL, AWS, Docker\n\nExperience:\n- Led migration from monolith to microservices (40% latency reduction)\n- Built real-time analytics dashboard serving 10K daily users\n- Mentored 3 junior developers\n\nLooking for: Technical lead role at a growth-stage startup"),
        (["security", "vulnerability", "password", "hash", "encrypt"],
         "Paste code, config, or text to audit...", "🔒 Security Input",
         'app.use(cors({ origin: "*" }));\n\nconst db = mysql.createConnection({\n  host: "prod-db.example.com",\n  user: "root",\n  password: "admin123"\n});\n\napp.get("/users", (req, res) => {\n  const query = `SELECT * FROM users WHERE id = ${req.params.id}`;\n  db.query(query, (err, results) => res.json(results));\n});'),
        (["docker", "k8s", "kubernetes", "ci-pipeline", "deploy"],
         "Paste config (Dockerfile, YAML, CI)...", "🐳 DevOps Config",
         "FROM node:18\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nEXPOSE 3000\nCMD [\"node\", \"server.js\"]"),
        (["git ", "changelog", "commit", "diff", "version bump"],
         "Paste commit messages, diff, or branch info...", "🗂️ Git Content",
         "feat: add user authentication with JWT tokens\nfix: resolve memory leak in WebSocket handler\nrefactor: extract payment logic into service layer\nfeat: add rate limiting middleware (100 req/min)\nfix: handle edge case in CSV export with unicode\nchore: upgrade dependencies (React 19, Node 22)\ndocs: update API reference for v2 endpoints"),
        (["cors", "rate-limit", "uptime", "url", "link check", "endpoint"],
         "Enter a URL or API endpoint...", "🔗 Enter URL",
         "https://api.github.com/repos/vercel/next.js"),
        (["blog", "seo", "article", "copy editor", "content writ", "post writer"],
         "Enter a topic or paste your draft...", "✍️ Topic or Draft",
         "Write a blog post about: How AI coding assistants are changing software development in 2025. Cover the productivity gains, potential risks, and best practices for developers."),
        (["csv", "json", "log analyz", "log pars", "data analys", "parse"],
         "Paste your data (CSV, JSON, logs)...", "📊 Paste Data",
         'name,age,city,score\nAlice,28,New York,92\nBob,35,London,87\nCharlie,22,Tokyo,95\nDiana,31,Paris,78\nEve,27,Berlin,91'),
        (["regex", "pattern", "match", "validator"],
         "Enter text or pattern to test...", "🔍 Text or Pattern",
         "Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$\n\nTest strings:\nuser@example.com\ninvalid-email@\nhello.world@company.co.uk\n@missing-local.com\ntest+tag@gmail.com"),
        (["markdown", "html-to", "convert", "format"],
         "Paste content to convert...", "🔄 Content to Convert",
         '<div class="container">\n  <h1>Welcome</h1>\n  <p>This is a <strong>sample</strong> HTML page with <a href="https://example.com">a link</a>.</p>\n  <ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n  </ul>\n</div>'),
        (["translate", "i18n", "localize"],
         "Paste text to translate...", "🌐 Text to Translate",
         "Welcome to our platform! Your account has been created successfully. Please verify your email address to get started. If you need help, contact our support team."),
        (["color", "css", "svg", "figma", "accessibility", "ascii art"],
         "Paste CSS, HTML, or describe design...", "🎨 Design Input",
         ".card {\n  background: #1a1a2e;\n  color: #eee;\n  border-radius: 12px;\n  padding: 24px;\n  box-shadow: 0 4px 20px rgba(0,0,0,0.3);\n}\n\n.btn-primary {\n  background: linear-gradient(135deg, #667eea, #764ba2);\n  color: white;\n  font-size: 14px;\n  padding: 8px 16px;\n}"),
        (["recipe", "meal", "food", "nutrition"],
         "Enter ingredients or dietary preferences...", "🍽️ Food / Ingredients",
         "I have: chicken breast, broccoli, garlic, soy sauce, rice, sesame oil, ginger. Looking for a healthy dinner recipe, preferably Asian-inspired, under 500 calories."),
        (["habit", "mood", "journal", "wellness"],
         "Describe your goal or current situation...", "🧘 Your Situation",
         "I want to build a morning routine. Currently I wake up at 8am, check my phone for 30 minutes, then rush to work. I'd like to wake at 6:30am, exercise, and read before starting work."),
        (["gift", "recommend"],
         "Describe the person and occasion...", "🎁 Context",
         "My friend is turning 30. She loves hiking, photography, and cooking. Budget is $50-100. She already has a good camera and hiking boots."),
        (["test gen", "unit test", "spec gen", "mock"],
         "Paste code to generate tests for...", "🧪 Code to Test",
         "def calculate_discount(price, quantity, is_member):\n    if quantity >= 10:\n        discount = 0.15\n    elif quantity >= 5:\n        discount = 0.10\n    else:\n        discount = 0\n    if is_member:\n        discount += 0.05\n    return round(price * quantity * (1 - discount), 2)"),
        (["readme", "doc writer", "documentation"],
         "Paste code or describe what to document...", "📖 Code / Description",
         "class RateLimiter:\n    def __init__(self, max_requests, window_seconds):\n        self.max_requests = max_requests\n        self.window = window_seconds\n        self.requests = {}\n\n    def is_allowed(self, client_id):\n        now = time.time()\n        self._cleanup(client_id, now)\n        if len(self.requests.get(client_id, [])) >= self.max_requests:\n            return False\n        self.requests.setdefault(client_id, []).append(now)\n        return True"),
        (["code", "review", "bug", "lint", "style", "refactor", "dead code", "complexity", "api"],
         "Paste your code here...", "📝 Paste Code",
         "def process_data(data):\n    result = []\n    for i in range(len(data)):\n        if data[i] != None:\n            temp = data[i]\n            if type(temp) == str:\n                temp = temp.strip()\n                if temp != '':\n                    result.append(temp)\n            elif type(temp) == int:\n                if temp > 0:\n                    result.append(temp)\n    return result"),
    ]

    for keywords, placeholder, label, example in hints:
        if any(kw in text for kw in keywords):
            return placeholder, label, example

    return ("Describe what you need or paste your text...", "📝 Your Input",
            "Analyze the following: Our web app has 1,200 daily active users with an average session of 4.5 minutes. Bounce rate is 45% and conversion rate is 2.3%. What improvements would you suggest?")


def _render_agent_detail(agent, agent_key):
    """Render detailed view for a single agent."""
    # Back button
    if st.button("← Back to Hub"):
        st.query_params.clear()
        st.rerun()

    icon = CATEGORY_META.get(agent["category"], ("📦",))[0]
    st.markdown(f"# {icon} {agent['name']}")

    if agent["description"]:
        st.markdown(f"> {agent['description']}")

    st.markdown(f"**Category:** {agent['category_display']}")
    st.divider()

    agent_path = Path(agent["path"])

    # Tabs: Try It (first/default), README, Code, Setup
    tabs = ["🚀 Try It", "📖 README", "📄 Code"]
    if agent["has_main"]:
        tabs.append("⚙️ Setup")

    tab_objects = st.tabs(tabs)

    # ─── Tab 0: Try It ─────────────────────────────────
    with tab_objects[0]:
        # Check if OpenAI key is available globally
        _has_openai = os.environ.get("OPENAI_API_KEY")
        if not _has_openai:
            try:
                _has_openai = st.secrets.get("OPENAI_API_KEY", None)
            except Exception:
                _has_openai = None

        if _has_openai and not _has_openai.startswith("sk-your"):
            st.caption("Test this agent directly — powered by OpenAI")

            agent_purpose = agent.get("description", agent.get("name", "AI Agent"))

            # Read argparse/click help from main.py for richer context
            _cli_help = ""
            try:
                _main_src = (Path(agent["path"]) / "main.py").read_text(encoding="utf-8")
                import re as _re
                _help_matches = _re.findall(r'help=["\']([^"\']+)["\']', _main_src)
                if _help_matches:
                    _cli_help = " CLI options: " + "; ".join(_help_matches[:5]) + "."
            except Exception:
                pass

            system_prompt = (
                f"You are an AI agent called '{agent['name']}'. "
                f"Your purpose: {agent_purpose}.{_cli_help} "
                "Respond helpfully and concisely to the user's input. "
                "Format your response with clear sections and use markdown."
            )

            placeholder, label, example = _get_agent_hint(agent)

            # Load Example button — sets the text area key directly
            ta_key = f"try_{agent_key}"
            if st.button("💡 Load Example", key=f"load_{agent_key}"):
                st.session_state[ta_key] = example
                st.rerun()

            user_input = st.text_area(
                label,
                placeholder=placeholder,
                height=150,
                key=ta_key,
            )

            if st.button("🚀 Run", key=f"run_{agent_key}", use_container_width=True):
                if not user_input:
                    st.warning("Please enter some text.")
                else:
                    with st.spinner("🔄 Running agent..."):
                        try:
                            import json as _json
                            from urllib.request import Request, urlopen

                            req_data = _json.dumps({
                                "model": "gpt-4o-mini",
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_input},
                                ],
                                "max_tokens": 1024,
                                "temperature": 0.3,
                            }).encode()

                            req = Request(
                                "https://api.openai.com/v1/chat/completions",
                                data=req_data,
                                headers={
                                    "Authorization": f"Bearer {_has_openai}",
                                    "Content-Type": "application/json",
                                },
                            )

                            with urlopen(req, timeout=30) as resp:
                                result = _json.loads(resp.read())

                            reply = result["choices"][0]["message"]["content"]
                            model = result.get("model", "gpt-4o-mini")
                            tokens = result.get("usage", {}).get("total_tokens", "?")

                            st.divider()
                            st.markdown("#### 📊 Result")
                            st.markdown(reply)
                            st.caption(f"Model: `{model}` · Tokens: `{tokens}`")

                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.warning(
                "⚠️ **OpenAI API key required**  \n"
                "Set `OPENAI_API_KEY` in Streamlit Secrets or your environment to enable live testing."
            )

    # ─── Tab 1: README ─────────────────────────────────
    with tab_objects[1]:
        agents_md = agent_path / "AGENTS.md"
        readme = agent_path / "README.md"
        if agents_md.exists():
            st.markdown(agents_md.read_text(encoding="utf-8"))
        elif readme.exists():
            st.markdown(readme.read_text(encoding="utf-8"))
        else:
            st.info("No README available for this agent.")

    # ─── Tab 2: Code ───────────────────────────────────
    with tab_objects[2]:
        main_py = agent_path / "main.py"
        if main_py.exists():
            st.markdown('<div class="code-header">main.py</div>', unsafe_allow_html=True)
            st.code(main_py.read_text(encoding="utf-8"), language="python", line_numbers=True)

        py_files = sorted(agent_path.rglob("*.py"))
        other_files = [f for f in py_files if f.name != "main.py" and "__pycache__" not in str(f)]
        if other_files:
            with st.expander(f"📂 {len(other_files)} more Python files"):
                for f in other_files:
                    rel = f.relative_to(agent_path)
                    st.markdown(f'<div class="code-header">{rel}</div>', unsafe_allow_html=True)
                    try:
                        st.code(f.read_text(encoding="utf-8"), language="python", line_numbers=True)
                    except Exception:
                        st.warning(f"Could not read {rel}")

    # ─── Tab 3: Setup ─────────────────────────────────
    if agent["has_main"] and len(tab_objects) > 3:
        with tab_objects[3]:
            # Detect if it's a Streamlit app or a plain CLI script
            main_content = ""
            try:
                main_content = (agent_path / "main.py").read_text(encoding="utf-8")
            except Exception:
                pass
            is_streamlit = "streamlit" in main_content.lower()

            # Detect required API keys from code and .env.example
            env_vars = []

            # Scan main.py source for common API key patterns
            api_key_patterns = [
                "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY",
                "GEMINI_API_KEY", "HUGGINGFACE_TOKEN", "HF_TOKEN",
                "COHERE_API_KEY", "PINECONE_API_KEY", "SERPAPI_KEY",
                "SERP_API_KEY", "TAVILY_API_KEY", "LANGCHAIN_API_KEY",
            ]
            for pat in api_key_patterns:
                if pat in main_content:
                    env_vars.append(pat)

            # Also check .env.example if it exists
            env_file = agent_path / ".env.example"
            if env_file.exists():
                try:
                    for line in env_file.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key = line.split("=", 1)[0].strip()
                            if key and key not in env_vars:
                                env_vars.append(key)
                except Exception:
                    pass

            # Also scan all Python files in the agent directory for API key patterns
            if not env_vars:
                for py_file in agent_path.rglob("*.py"):
                    if "__pycache__" in str(py_file):
                        continue
                    try:
                        py_content = py_file.read_text(encoding="utf-8")
                        for pat in api_key_patterns:
                            if pat in py_content and pat not in env_vars:
                                env_vars.append(pat)
                    except Exception:
                        continue

            # Only show warnings for missing keys — hide when all configured
            if env_vars:
                missing = []
                for v in env_vars:
                    val = os.environ.get(v)
                    if not val:
                        try:
                            val = st.secrets.get(v, None)
                        except Exception:
                            val = None
                    if not val or val.startswith("sk-your") or val.startswith("your-") or val.startswith("ghp_your"):
                        missing.append(v)

                if missing:
                    st.warning(
                        "⚠️ **Missing API keys:**  "
                        + ", ".join(f"`{v}`" for v in missing)
                        + "  \nSet these in Streamlit Secrets or environment variables."
                    )

            if is_streamlit:
                st.info(
                    "This is a **Streamlit app** — run it separately:\n"
                    "```bash\n"
                    f"cd {agent_key}\n"
                    "pip install -r requirements.txt\n"
                    "streamlit run main.py\n"
                    "```"
                )
            else:
                st.markdown("**To run this agent locally:**")
                req_file = agent_path / "requirements.txt"
                if req_file.exists():
                    st.code(
                        f"cd {agent_key}\n"
                        "pip install -r requirements.txt\n"
                        "python main.py --help",
                        language="bash",
                    )
                else:
                    st.code(
                        f"cd {agent_key}\n"
                        "python main.py --help",
                        language="bash",
                    )

            # Show requirements
            req_file = agent_path / "requirements.txt"
            if req_file.exists():
                with st.expander("📦 Dependencies"):
                    st.code(req_file.read_text(encoding="utf-8"), language="text")


if __name__ == "__main__":
    main()
