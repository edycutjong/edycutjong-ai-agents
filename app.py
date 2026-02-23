"""
🧠 AI Agents Hub — Browse & Run 130+ AI Automation Agents
Built by Jules AI • Powered by Streamlit
"""

import streamlit as st
import os
import importlib.util
import sys
from pathlib import Path

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
        st.markdown("## 🧠 AI Agents Hub")
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
    filtered = agents
    if selected_cat != "All":
        filtered = {k: v for k, v in filtered.items() if v["category"] == selected_cat}
    if search:
        search_lower = search.lower()
        filtered = {k: v for k, v in filtered.items()
                    if search_lower in v["name"].lower()
                    or search_lower in v["description"].lower()
                    or search_lower in k.lower()}

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
    st.markdown('<h1 class="hero-title">AI Agents Hub</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Browse & explore 130+ AI automation agents — '
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

    # Tabs: Code, README, Run
    tabs = ["📄 Code", "📖 README"]
    if agent["has_main"]:
        tabs.append("▶️ Run Agent")

    tab_objects = st.tabs(tabs)

    # Code tab
    with tab_objects[0]:
        main_py = agent_path / "main.py"
        if main_py.exists():
            st.markdown('<div class="code-header">main.py</div>', unsafe_allow_html=True)
            st.code(main_py.read_text(encoding="utf-8"), language="python", line_numbers=True)

        # Show other Python files
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

    # README tab
    with tab_objects[1]:
        agents_md = agent_path / "AGENTS.md"
        readme = agent_path / "README.md"
        if agents_md.exists():
            st.markdown(agents_md.read_text(encoding="utf-8"))
        elif readme.exists():
            st.markdown(readme.read_text(encoding="utf-8"))
        else:
            st.info("No README available for this agent.")

    # Run tab
    if agent["has_main"] and len(tab_objects) > 2:
        with tab_objects[2]:
            st.warning(
                "⚠️ **Running agents requires dependencies and API keys.**\n\n"
                "To run this agent locally:\n"
                "```bash\n"
                f"cd {agent_key}\n"
                "pip install -r requirements.txt\n"
                "streamlit run main.py\n"
                "```"
            )

            # Show requirements
            req_file = agent_path / "requirements.txt"
            if req_file.exists():
                st.markdown("**Dependencies:**")
                st.code(req_file.read_text(encoding="utf-8"), language="text")


if __name__ == "__main__":
    main()
