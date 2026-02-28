import streamlit as st
import zipfile
import io
import html
import os
import sys

# Ensure imports work regardless of run context
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.generator import IconGenerator
from agent.optimizer import IconOptimizer
from agent.formatter import IconFormatter
from config import config

# Page Config
st.set_page_config(
    page_title="Icon Set Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .icon-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #41424b;
    }
    .icon-card svg {
        max-width: 100%;
        height: auto;
    }
    .icon-title {
        margin-top: 10px;
        font-size: 0.9em;
        color: #b0b0b0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Settings")

    provider = st.selectbox("AI Provider", ["OpenAI", "Google"], index=0)
    api_key = st.text_input("API Key", type="password", help="Leave empty if set in .env")

    st.markdown("---")
    st.subheader("Style")
    style = st.selectbox("Icon Style", config.STYLES, index=0)
    color = st.color_picker("Primary Color", config.DEFAULT_COLOR)

    st.markdown("---")
    st.info("Generates 24x24 SVG icons.")

# Main Content
st.title("🎨 Icon Set Generator")
st.markdown("Generate consistent SVG icon sets from text descriptions using AI.")

col1, col2 = st.columns([2, 1])

with col1:
    descriptions_input = st.text_area(
        "Icon Descriptions (one per line)",
        height=200,
        placeholder="home icon\nsettings gear\nuser profile\nsearch magnifying glass"
    )

with col2:
    st.markdown("### Preview")
    st.write(f"**Style:** {style}")
    st.write(f"**Color:** {color}")

    if st.button("Generate Icons", type="primary", use_container_width=True):
        if not descriptions_input.strip():
            st.error("Please enter at least one icon description.")
        else:
            descriptions = [d.strip() for d in descriptions_input.split('\n') if d.strip()]

            # Initialize Generator
            generator = IconGenerator(provider=provider, api_key=api_key)
            optimizer = IconOptimizer()
            formatter = IconFormatter()

            progress_bar = st.progress(0)
            status_text = st.empty()

            generated_icons = {}

            for i, desc in enumerate(descriptions):
                status_text.text(f"Generating: {desc}...")

                # Generate
                raw_svg = generator.generate_icon(desc, style, color)

                # Optimize
                opt_svg = optimizer.optimize_svg(raw_svg)

                # Store
                icon_name = desc.lower().replace(" ", "-")
                generated_icons[icon_name] = opt_svg

                progress_bar.progress((i + 1) / len(descriptions))

            status_text.text("Generation Complete!")
            st.session_state['generated_icons'] = generated_icons

# Display Results
if 'generated_icons' in st.session_state and st.session_state['generated_icons']:
    st.markdown("---")
    st.subheader("Generated Icons")

    icons = st.session_state['generated_icons']
    cols = st.columns(4)

    for i, (name, svg) in enumerate(icons.items()):
        with cols[i % 4]:
            safe_name = html.escape(name)
            st.markdown(f"""
                <div class="icon-card">
                    {svg}
                    <div class="icon-title">{safe_name}</div>
                </div>
            """, unsafe_allow_html=True)

            # Individual download (optional, maybe overkill for UI)
            # st.download_button("SVG", svg, file_name=f"{name}.svg", mime="image/svg+xml")

    # Bulk Export
    st.markdown("---")
    st.subheader("Export")

    c1, c2, c3 = st.columns(3)

    # ZIP SVGs
    svg_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(svg_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, svg in icons.items():
            zf.writestr(f"{name}.svg", svg)

    c1.download_button(
        label="Download SVG ZIP",
        data=svg_zip_buffer.getvalue(),
        file_name="icons_svg.zip",
        mime="application/zip",
        use_container_width=True
    )

    # ZIP React
    react_zip_buffer = io.BytesIO()
    formatter = IconFormatter() # Re-init locally just in case
    with zipfile.ZipFile(react_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, svg in icons.items():
            # Name to PascalCase
            component_name = "".join(x.title() for x in name.split("-")) + "Icon"
            code = formatter.to_react_component(svg, component_name)
            zf.writestr(f"{component_name}.jsx", code)

    c2.download_button(
        label="Download React Components",
        data=react_zip_buffer.getvalue(),
        file_name="icons_react.zip",
        mime="application/zip",
        use_container_width=True
    )

    # ZIP Vue
    vue_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(vue_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, svg in icons.items():
            component_name = "".join(x.title() for x in name.split("-")) + "Icon"
            code = formatter.to_vue_component(svg, component_name)
            zf.writestr(f"{component_name}.vue", code)

    c3.download_button(
        label="Download Vue Components",
        data=vue_zip_buffer.getvalue(),
        file_name="icons_vue.zip",
        mime="application/zip",
        use_container_width=True
    )
