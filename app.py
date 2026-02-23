"""
🧠 AI Agents Hub — Browse & Run 180+ AI Automation Agents
Built by Jules AI • Powered by Streamlit
"""

import streamlit as st
import os
import random
from datetime import datetime
from pathlib import Path
from examples import get_agent_hint
from i18n import LOCALES, LOCALE_NAMES, get_translations

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

    /* Theme-agnostic variables — visible on both light and dark */
    :root {
        --card-border: rgba(128,128,128,0.25);
        --card-bg: rgba(128,128,128,0.04);
        --card-hover-border: rgba(168,85,247,0.5);
        --card-hover-bg: rgba(168,85,247,0.08);
        --badge-bg: rgba(168,85,247,0.12);
        --sidebar-bg: rgba(128,128,128,0.06);
        --stat-border: rgba(128,128,128,0.2);
        --stat-bg: rgba(128,128,128,0.04);
    }

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
        color: inherit; opacity: 0.6;
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
        background: var(--badge-bg);
        color: #a855f7;
    }

    /* Agent card */
    .agent-card {
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        background: var(--card-bg);
        transition: all 0.2s;
    }
    .agent-card:hover {
        border-color: var(--card-hover-border);
        background: var(--card-hover-bg);
    }
    .agent-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: inherit;
        margin-bottom: 4px;
    }
    .agent-desc {
        font-size: 0.85rem;
        color: inherit; opacity: 0.6;
        line-height: 1.4;
    }

    /* Stats */
    .stat-box {
        text-align: center;
        padding: 16px;
        border-radius: 12px;
        background: var(--stat-bg);
        border: 1px solid var(--stat-border);
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
        color: inherit; opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
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


def _render_copy_btn(text: str, key: str):
    """Render the result in a copyable code block using Streamlit's built-in copy."""
    with st.expander("📋 Copy result", expanded=False):
        st.code(text, language=None)


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
    # Fix browser back/forward: force reload when URL changes via popstate
    st.components.v1.html("""
    <script>
    if (!window._popstateListenerAdded) {
        window._popstateListenerAdded = true;
        window.addEventListener('popstate', function() {
            window.parent.location.reload();
        });
    }
    </script>
    """, height=0)

    agents = discover_agents()
    categories = sorted(set(a["category"] for a in agents.values()))

    # Sidebar
    with st.sidebar:
        # Language selector
        locale_options = list(LOCALE_NAMES.keys())
        locale_labels = list(LOCALE_NAMES.values())
        current_locale = st.session_state.get("locale", "en")
        locale_idx = locale_options.index(current_locale) if current_locale in locale_options else 0
        selected_locale = st.selectbox(
            "🌐",
            locale_options,
            index=locale_idx,
            format_func=lambda x: LOCALE_NAMES[x],
            key="lang_select",
        )
        if selected_locale != st.session_state.get("locale"):
            st.session_state["locale"] = selected_locale
            st.rerun()
        tr = get_translations(st.session_state.get("locale", "en"))

        st.markdown(f"### 🧠 {tr['title']}")
        st.markdown(f"**{len(agents)}** {tr['sidebar_agents']} · **{len(categories)}** {tr['sidebar_categories']}")
        st.divider()

        # Category filter
        selected_cat = st.selectbox(
            f"📂 {tr['categories']}",
            ["All"] + categories,
            format_func=lambda x: tr['all_categories'] if x == "All" else CATEGORY_META.get(x, ("📦", _slug_to_name(x), ""))[1] + f" ({sum(1 for a in agents.values() if a['category'] == x)})"
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
        search = st.text_input(f"🔍 {tr['search']}", placeholder=tr['search'])

        # Clear agent selection when search changes
        if search and "agent" in st.query_params:
            del st.query_params["agent"]
            st.rerun()

        # Surprise Me button
        st.markdown(f"<small>{tr['surprise_hint']}</small>", unsafe_allow_html=True)
        if st.button(tr['surprise_btn'], key="surprise_me", use_container_width=True):
            pick = random.choice(list(agents.keys()))
            st.query_params["agent"] = pick
            st.rerun()

        # ─── Run History ────────────────────────────
        if st.session_state.get("run_history"):
            st.divider()
            with st.expander(f"📜 {tr['recent_runs']} ({len(st.session_state['run_history'])})", expanded=False):
                for i, run in enumerate(st.session_state["run_history"]):
                    preview = run["input"][:60].replace("\n", " ") + ("…" if len(run["input"]) > 60 else "")
                    with st.expander(f"`{run['time']}` **{run['agent']}**", expanded=False):
                        st.caption(f"Input: {preview}")
                        st.markdown(run["output"])
                        st.caption(f"Tokens: `{run['tokens']}`")

        st.divider()
        st.markdown(
            f"<div style='text-align:center;color:#6b7280;font-size:0.8rem'>"
            f"{tr['footer']} <a href='https://edycu.dev' style='color:#a855f7'>edycu.dev</a>"
            f"</div>",
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
    tr = get_translations(st.session_state.get("locale", "en"))
    # Hero
    total_count = len(all_agents)
    st.markdown(f'<h1 class="hero-title">{tr["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="hero-subtitle">{tr["subtitle"].format(count=total_count)}</p>',
        unsafe_allow_html=True
    )

    # Stats
    total = len(all_agents)
    built = sum(1 for a in all_agents.values() if a["has_main"])
    cats = len(set(a["category"] for a in all_agents.values()))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{total}</div><div class="stat-label">{tr["total_agents"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{built}</div><div class="stat-label">{tr["ready_to_run"]}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{cats}</div><div class="stat-label">{tr["categories"]}</div></div>', unsafe_allow_html=True)

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
                        st.caption(f"{tr['category_label']}: {agent['category_display']}")

                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"<div style='display:flex;align-items:center;height:100%;min-height:38px'>{status} {tr['built'] if agent['has_main'] else tr['spec']}</div>", unsafe_allow_html=True)
                    with c2:
                        if agent["has_main"]:
                            if st.button(tr['view'], key=f"view_{key}", use_container_width=True):
                                st.query_params["agent"] = key
                                st.rerun()


# _get_agent_hint is now imported from examples.py as get_agent_hint


def _render_agent_detail(agent, agent_key):
    """Render detailed view for a single agent."""
    tr = get_translations(st.session_state.get("locale", "en"))
    # Back button
    if st.button(tr['back']):
        st.query_params.clear()
        st.rerun()

    icon = CATEGORY_META.get(agent["category"], ("📦",))[0]
    st.markdown(f"# {icon} {agent['name']}")

    if agent["description"]:
        st.markdown(f"> {agent['description']}")

    st.markdown(f"**{tr['category_label']}:** {agent['category_display']}")
    st.divider()

    agent_path = Path(agent["path"])

    # Tabs: Try It (first/default), README, Code, Setup
    tabs = [tr['run_tab'], tr['docs_tab'], tr['code_tab']]
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
            st.caption(tr['test_caption'])

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

            placeholder, label, examples = get_agent_hint(agent)

            # Random no-repeat example cycling
            ta_key = f"try_{agent_key}"
            seen_key = f"seen_{agent_key}"
            if seen_key not in st.session_state:
                st.session_state[seen_key] = []

            btn_label = f"🔄 {tr['load_example']}" if st.session_state[seen_key] else f"💡 {tr['load_example']}"
            if st.button(btn_label, key=f"load_{agent_key}"):
                seen = st.session_state[seen_key]
                remaining = [i for i in range(len(examples)) if i not in seen]
                if not remaining:  # all shown, reset
                    seen.clear()
                    remaining = list(range(len(examples)))
                pick = random.choice(remaining)
                seen.append(pick)
                st.session_state[ta_key] = examples[pick]
                st.rerun()

            user_input = st.text_area(
                label,
                placeholder=placeholder,
                height=150,
                key=ta_key,
            )

            if st.button(tr['run_btn'], key=f"run_{agent_key}", use_container_width=True):
                if not user_input:
                    st.warning(tr['enter_text'])
                else:
                    # Check cache — skip API call if same input
                    cache_key = f"cache_{agent_key}"
                    cached = st.session_state.get(cache_key)
                    if cached and cached["input"] == user_input:
                        st.divider()
                        st.markdown(f"#### {tr['result']}")
                        st.markdown(cached["output"])
                        st.caption(f"Model: `{cached['model']}` · Tokens: `{cached['tokens']}` · ⚡ {tr['cached']}")
                        _render_copy_btn(cached["output"], f"copy_cached_{agent_key}")
                    else:
                        with st.spinner(tr['running']):
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

                                # Cache result for this agent
                                st.session_state[cache_key] = {
                                    "input": user_input,
                                    "output": reply,
                                    "model": model,
                                    "tokens": tokens,
                                }

                                # Save to run history
                                if "run_history" not in st.session_state:
                                    st.session_state["run_history"] = []
                                st.session_state["run_history"].insert(0, {
                                    "agent": agent.get("name", "Unknown"),
                                    "input": user_input,
                                    "output": reply,
                                    "tokens": tokens,
                                    "time": datetime.now().strftime("%H:%M"),
                                })
                                st.session_state["run_history"] = st.session_state["run_history"][:10]

                                st.divider()
                                st.markdown(f"#### {tr['result']}")
                                st.markdown(reply)
                                st.caption(f"Model: `{model}` · Tokens: `{tokens}`")
                                _render_copy_btn(reply, f"copy_fresh_{agent_key}")

                            except Exception as e:
                                st.error(f"{tr['error']}: {str(e)}")

                    # Auto-scroll so "Result" heading is at top of viewport
                    st.components.v1.html("""
                    <script>
                    const headers = window.parent.document.querySelectorAll('section.main h4');
                    for (const h of headers) {
                        if (h.textContent.includes('Result')) {
                            h.scrollIntoView({behavior: 'smooth', block: 'start'});
                            break;
                        }
                    }
                    </script>
                    """, height=0)
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
                            # Only include actual API keys/tokens, skip config vars
                            is_api_key = any(s in key for s in ("KEY", "TOKEN", "SECRET", "API"))
                            if key and is_api_key and key not in env_vars:
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
                st.markdown(f"**{tr['run_locally']}**")
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
