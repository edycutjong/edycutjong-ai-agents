"""
🧠 AI Agents Hub — Browse & Run 180+ AI Automation Agents
Built by Jules AI • Powered by Streamlit
"""

import streamlit as st
import os
import json
import random
from datetime import datetime
from pathlib import Path
from examples import get_agent_hint
from i18n import LOCALES, LOCALE_NAMES, get_translations
from st_keyup import st_keyup

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

    /* Agent card — with micro-animation */
    .agent-card {
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        background: var(--card-bg);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .agent-card:hover {
        border-color: var(--card-hover-border);
        background: var(--card-hover-bg);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.15);
    }

    /* Card container hover — lift + glow */
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.12);
    }

    /* Button micro-animation */
    .stButton > button {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* Fade-in animation for content */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    section.main .block-container {
        animation: fadeInUp 0.4s ease-out;
    }

    /* Stat box pulse on hover */
    .stat-box {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stat-box:hover {
        transform: scale(1.02);
        border-color: rgba(168, 85, 247, 0.4);
    }

    /* Smooth sidebar transitions */
    [data-testid="stSidebar"] * {
        transition: background-color 0.2s ease, color 0.2s ease;
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
        /* transition already defined above */
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

    /* Search input: reduce gap to button and match sidebar background */
    [data-testid="stSidebar"] iframe[title="st_keyup.st_keyup"] {
        margin-bottom: -0.75rem;
    }
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] iframe[title="st_keyup.st_keyup"] {
        background-color: var(--sidebar-bg, transparent) !important;
    }

    /* Loading Skeleton Styling */
    .stSpinner > div {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        padding: 1.5rem 2rem !important;
        margin: 1rem 0 !important;
    }
    .stSpinner > div > div {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .stSpinner > div > div > img {
        width: 22px !important;
        height: 22px !important;
    }
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

# ─── Agent Translations ────────────────────────────────────────
_agent_tr_file = BASE_DIR / "agent_translations.json"
_agent_translations = json.loads(_agent_tr_file.read_text(encoding="utf-8")) if _agent_tr_file.exists() else {}


def _tr_agent(agent_key: str, field: str, locale: str, fallback: str) -> str:
    """Get translated agent name or description, falling back to English."""
    return _agent_translations.get(agent_key, {}).get(locale, {}).get(field, fallback)


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
                    readme_md = agent_dir / "README.md"
                    if main_py.exists() or agents_md.exists():
                        desc = _extract_desc(agents_md) if agents_md.exists() else ""
                        if not desc and readme_md.exists():
                            desc = _extract_desc(readme_md)
                        if not desc and main_py.exists():
                            desc = _extract_desc_from_main(main_py)
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
            readme_md = agent_dir / "README.md"
            if main_py.exists() or agents_md.exists():
                desc = _extract_desc(agents_md) if agents_md.exists() else ""
                if not desc and readme_md.exists():
                    desc = _extract_desc(readme_md)
                if not desc and main_py.exists():
                    desc = _extract_desc_from_main(main_py)
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


def _extract_desc(md_file: Path) -> str:
    try:
        content = md_file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---") and len(line) > 20:
                clean = line.lstrip("- *>").strip()
                return clean[:200]
    except Exception:
        pass
    return ""


def _extract_desc_from_main(main_py: Path) -> str:
    """Extract description from main.py argparse or docstring."""
    try:
        content = main_py.read_text(encoding="utf-8")
        # Try argparse description
        import re
        m = re.search(r'description=["\']([^"\']+)["\']', content)
        if m:
            return m.group(1)[:200]
        # Try module docstring
        m = re.search(r'^"""\s*\n?(.+?)(?:\n|""")', content)
        if m:
            desc = m.group(1).strip().rstrip(' —-')
            if len(desc) > 10:
                return desc[:200]
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

    # Sync locale with query params on initial load or change
    if "lang" in st.query_params:
        url_lang = st.query_params["lang"]
        if url_lang in LOCALE_NAMES and st.session_state.get("locale") != url_lang:
            st.session_state["locale"] = url_lang

    agents = discover_agents()
    categories = sorted(set(a["category"] for a in agents.values()))

    # Sidebar
    with st.sidebar:
        # Language selector (horizontal: 🌐 + dropdown)
        locale_options = list(LOCALE_NAMES.keys())
        locale_labels = list(LOCALE_NAMES.values())
        current_locale = st.session_state.get("locale", "en")
        locale_idx = locale_options.index(current_locale) if current_locale in locale_options else 0
        tr = get_translations(st.session_state.get("locale", "en"))

        selected_locale = st.selectbox(
            tr.get("language", "Language"),
            locale_options,
            index=locale_idx,
            format_func=lambda x: f"{x.upper()} · {LOCALE_NAMES[x]}",
            key="lang_select",
            label_visibility="collapsed",
        )
        if selected_locale != st.session_state.get("locale"):
            st.session_state["locale"] = selected_locale
            st.query_params["lang"] = selected_locale
            st.rerun()
        # Inject dynamic CSS to localize the native Streamlit InputInstructions
        st.markdown(f"""
        <style>
        div[data-testid="InputInstructions"] > span {{
            font-size: 0 !important;
        }}
        .stTextInput div[data-testid="InputInstructions"] > span::after {{
            content: "↵ {tr.get('press_enter', 'Press Enter to apply')}";
            font-size: 0.75rem;
        }}
        .stTextArea div[data-testid="InputInstructions"] > span::after {{
            content: "⌘ ↵ {tr.get('press_enter', 'Press Enter to apply')}";
            font-size: 0.75rem;
        }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🧠 {tr['title']}")
        st.markdown(f"**{len(agents)}** {tr['sidebar_agents']} · **{len(categories)}** {tr['sidebar_categories']}")
        st.divider()

        # Category filter
        selected_cat = st.selectbox(
            f"📂 {tr['categories']}",
            ["All"] + categories,
            format_func=lambda x: tr['all_categories'] if x == "All" else (tr.get('category_names', {}).get(x, CATEGORY_META.get(x, ("📦", _slug_to_name(x), ""))[1]) + f" ({sum(1 for a in agents.values() if a['category'] == x)})")
        )

        # Clear agent selection when category changes
        if "prev_cat" not in st.session_state:
            st.session_state.prev_cat = selected_cat
        if selected_cat != st.session_state.prev_cat:
            st.session_state.prev_cat = selected_cat
            if "agent" in st.query_params:
                del st.query_params["agent"]
                st.rerun()

        # Search Input (real-time keyup to allow button disabled state to toggle on typing)
        search_val = st_keyup(f"🔍 {tr['search']}", placeholder=tr['search'], key="keyup_search_val", debounce=100)
        if search_val is None:
            search_val = ""
        
        # Track last applied search term
        if "last_search" not in st.session_state:
            st.session_state.last_search = ""
            
        # Automatically clear search filters if the user deletes all text and presses enter
        if len(search_val) == 0 and st.session_state.last_search != "":
            st.session_state.last_search = ""
            if "agent" in st.query_params:
                del st.query_params["agent"]
                
        # Only enable if >= 1 char AND it has changed from the currently applied search
        disable_btn = len(search_val) < 1 or search_val == st.session_state.last_search
        
        # Change button text exactly to something like 'Search'
        btn_label = tr.get("search_btn", "Search")
        
        if st.button(btn_label, key="search_button", use_container_width=True, disabled=disable_btn):
            st.session_state.last_search = search_val
            if search_val and "agent" in st.query_params:
                del st.query_params["agent"]
            st.rerun()

        # The actual filter variable used for agents is now the committed search
        search = st.session_state.last_search

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
                import time as _time
                for i, run in enumerate(st.session_state["run_history"]):
                    preview = run["input"][:60].replace("\n", " ") + ("…" if len(run["input"]) > 60 else "")
                    # Relative time display
                    elapsed = int(_time.time() - run.get('ts', _time.time()))
                    if elapsed < 60:
                        rel = tr.get('time_just_now', 'just now')
                    elif elapsed < 3600:
                        rel = tr.get('time_min_ago', '{n} min ago').format(n=elapsed // 60)
                    else:
                        rel = tr.get('time_hr_ago', '{n}h ago').format(n=elapsed // 3600)
                    with st.expander(f"`{rel}` **{run['agent']}**", expanded=False):
                        st.caption(f"{tr.get('input_label', 'Input')}: {preview}")
                        st.markdown(run["output"])
                        st.caption(f"{tr.get('tokens_label', 'Tokens')}: `{run['tokens']}`")

        locale = st.session_state.get("locale", "en")
        locale_prefix = f"/{locale}" if locale != "en" else ""
        footer_links = (
            f"<a href='https://apps.edycu.dev{locale_prefix}/privacy' style='color:#6b7280;text-decoration:none'>{tr.get('footer_privacy', 'Privacy Policy')}</a>"
            f" · <a href='https://apps.edycu.dev{locale_prefix}/terms' style='color:#6b7280;text-decoration:none'>{tr.get('footer_terms', 'Terms of Service')}</a>"
            f" · <a href='https://apps.edycu.dev{locale_prefix}/support' style='color:#6b7280;text-decoration:none'>{tr.get('footer_support', 'Support')}</a>"
        )
        st.markdown(
            f"<div style='text-align:center;color:#6b7280;font-size:0.8rem'>"
            f"{footer_links}<br>"
            f"{tr['footer']} <a href='https://edycu.dev' style='color:#a855f7'>edycu.dev</a>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Filter agents
    if search:
        # Search across ALL agents regardless of category (including translated names)
        search_lower = search.lower()
        locale = st.session_state.get("locale", "en")
        def _matches(k, v):
            if search_lower in v["name"].lower() or search_lower in k.lower():
                return True
            if search_lower in v["description"].lower():
                return True
            if search_lower in v["category_display"].lower():
                return True
            # Also search translated name/description
            if locale != "en":
                tr_name = _tr_agent(k, "name", locale, "").lower()
                tr_desc = _tr_agent(k, "description", locale, "").lower()
                if search_lower in tr_name or search_lower in tr_desc:
                    return True
            return False
        filtered = {k: v for k, v in agents.items() if _matches(k, v)}
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
        st.info(tr.get('showing_agents', 'Showing **{count}** of {total} agents').format(count=len(filtered), total=len(all_agents)))

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
                    locale = st.session_state.get("locale", "en")
                    a_name = _tr_agent(key, "name", locale, agent["name"]) if locale != "en" else agent["name"]
                    a_desc = _tr_agent(key, "description", locale, agent["description"]) if locale != "en" else agent["description"]
                    st.markdown(f"**{icon} {a_name}**")
                    if a_desc:
                        st.caption(a_desc[:120] + ("..." if len(a_desc) > 120 else ""))
                    else:
                        _cat_tr = tr.get('category_names', {}).get(agent['category'], agent['category_display'])
                        st.caption(f"{tr['category_label']}: {_cat_tr}")

                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"<div style='display:flex;align-items:center;min-height:38px;padding:0.25rem 0;font-size:0.85rem;opacity:0.7'>{status} {tr['built'] if agent['has_main'] else tr['spec']}</div>", unsafe_allow_html=True)
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
        # Preserve lang param when going back
        lang = st.query_params.get("lang", None)
        st.query_params.clear()
        if lang:
            st.query_params["lang"] = lang
        st.rerun()

    icon = CATEGORY_META.get(agent["category"], ("📦",))[0]
    locale = st.session_state.get("locale", "en")
    a_name = _tr_agent(agent_key, "name", locale, agent["name"]) if locale != "en" else agent["name"]
    a_desc = _tr_agent(agent_key, "description", locale, agent["description"]) if locale != "en" else agent["description"]
    st.markdown(f"# {icon} {a_name}")

    if a_desc:
        st.markdown(f"> {a_desc}")

    # Translate category display
    cat_key = agent["category"]
    cat_icon = CATEGORY_META.get(cat_key, ("📦",))[0]
    cat_display = tr.get('category_names', {}).get(cat_key, agent['category_display'])
    st.markdown(f"**{tr['category_label']}:** {cat_icon} {cat_display}")
    st.divider()

    agent_path = Path(agent["path"])

    # Tabs: Try It (first/default), README, Code, Setup
    tabs = [tr['run_tab'], tr['docs_tab'], tr['code_tab']]
    if agent["has_main"]:
        tabs.append(tr.get('setup_tab', '⚙️ Setup'))

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

            # Check current app language
            current_locale = st.session_state.get("locale", "en")
            
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

            running_key = f"running_{agent_key}"
            is_running = st.session_state.get(running_key, False)
            cache_key = f"cache_{agent_key}"

            btn_label = f"🔄 {tr['load_example']}" if st.session_state[seen_key] else f"💡 {tr['load_example']}"
            if st.button(btn_label, key=f"load_{agent_key}", disabled=is_running):
                seen = st.session_state[seen_key]
                remaining = [i for i in range(len(examples)) if i not in seen]
                if not remaining:  # all shown, reset
                    seen.clear()
                    remaining = list(range(len(examples)))
                pick = random.choice(remaining)
                seen.append(pick)
                st.session_state[ta_key] = examples[pick]
                st.rerun()

            force_translate = False
            base_label = tr.get('default_input_label', label) if label == "📝 Your Input" else label
            
            if current_locale != "en":
                col_label, col_toggle = st.columns([1, 1])
                with col_label:
                    st.markdown(f"**{base_label}**")
                
                lang_names = {
                    "id": "Indonesian", "zh": "Chinese", "hi": "Hindi", 
                    "es": "Spanish", "fr": "French", "ar": "Arabic", 
                    "bn": "Bengali", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese"
                }
                target_lang = lang_names.get(current_locale, current_locale)
                toggle_str = tr.get("translate_toggle", f"🌐 Translate response to {{lang}}").replace("{lang}", target_lang)
                
                with col_toggle:
                    force_translate = st.toggle(
                        toggle_str, 
                        value=st.session_state.get(f"translate_{agent_key}", True),
                        key=f"translate_{agent_key}",
                        disabled=is_running
                    )
                if force_translate:
                    system_prompt += f"\nIMPORTANT: You MUST write your entire response in {target_lang}."
            else:
                st.markdown(f"**{base_label}**")

            user_input = st.text_area(
                base_label,
                label_visibility="collapsed",
                placeholder=tr.get('default_input_placeholder', placeholder) if placeholder == "Describe what you need or paste your text..." else placeholder,
                height=150,
                key=ta_key,
                disabled=is_running,
            )

            def _on_run_click():
                if st.session_state[ta_key]:
                    st.session_state[running_key] = True

            st.button(
                tr['run_btn'], 
                key=f"run_{agent_key}", 
                use_container_width=True, 
                disabled=is_running,
                on_click=_on_run_click
            )

            # Warning if trying to run with empty input
            if st.session_state.get(running_key) and not user_input:
                st.session_state[running_key] = False
                st.warning(tr['enter_text'])
                
            # If running, do the API call
            if st.session_state.get(running_key) and user_input:
                cached = st.session_state.get(cache_key)
                # If exact same input is already cached, no need to run API again
                if cached and cached["input"] == user_input:
                    st.session_state[running_key] = False
                    st.rerun()
                    
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
                            "ts": __import__('time').time(),
                        })
                        st.session_state["run_history"] = st.session_state["run_history"][:10]

                    except Exception as e:
                        st.error(f"{tr['error']}: {str(e)}")
                    finally:
                        st.session_state[running_key] = False
                        
                st.rerun()

            # Render cached result (will show after run finishes and reruns)
            cached = st.session_state.get(cache_key)
            if cached and cached["input"] == user_input and not is_running:
                st.divider()
                st.markdown(f"#### {tr['result']}")
                st.markdown(cached["output"])
                st.caption(f"{tr.get('model_label', 'Model')}: `{cached['model']}` · {tr.get('tokens_label', 'Tokens')}: `{cached['tokens']}`")
                _render_copy_btn(cached["output"], f"copy_cached_{agent_key}")

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
            st.info(tr.get('no_readme', 'No README available for this agent.'))

    # ─── Tab 2: Code ───────────────────────────────────
    with tab_objects[2]:
        main_py = agent_path / "main.py"
        if main_py.exists():
            st.markdown('<div class="code-header">main.py</div>', unsafe_allow_html=True)
            st.code(main_py.read_text(encoding="utf-8"), language="python", line_numbers=True)

        py_files = sorted(agent_path.rglob("*.py"))
        other_files = [f for f in py_files if f.name != "main.py" and "__pycache__" not in str(f)]
        if other_files:
            with st.expander(f"📂 {len(other_files)} {tr.get('more_files', 'more Python files')}"):
                for f in other_files:
                    rel = f.relative_to(agent_path)
                    st.markdown(f'<div class="code-header">{rel}</div>', unsafe_allow_html=True)
                    try:
                        st.code(f.read_text(encoding="utf-8"), language="python", line_numbers=True)
                    except Exception:
                        st.warning(f"{tr.get('could_not_read', 'Could not read')} {rel}")

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
                "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY",
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
                        tr.get('missing_api_keys', '⚠️ **Missing API keys:**') + "  "
                        + ", ".join(f"`{v}`" for v in missing)
                        + "  \n" + tr.get('set_api_keys_hint', 'Set these in Streamlit Secrets or environment variables.')
                    )

            if is_streamlit:
                st.info(
                    tr.get('streamlit_app_info', 'This is a **Streamlit app** — run it separately:') + "\n"
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
                with st.expander(tr.get('dependencies', '📦 Dependencies')):
                    st.code(req_file.read_text(encoding="utf-8"), language="text")


if __name__ == "__main__":
    main()
