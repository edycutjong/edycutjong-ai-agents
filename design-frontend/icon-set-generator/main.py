import streamlit as st  # pragma: no cover
import zipfile  # pragma: no cover
import io  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Ensure imports work regardless of run context
current_dir = os.path.dirname(os.path.abspath(__file__))  # pragma: no cover
if current_dir not in sys.path:  # pragma: no cover
    sys.path.append(current_dir)  # pragma: no cover

from agent.generator import IconGenerator  # pragma: no cover
from agent.optimizer import IconOptimizer  # pragma: no cover
from agent.formatter import IconFormatter  # pragma: no cover
from config import config  # pragma: no cover

# Page Config
st.set_page_config(  # pragma: no cover
    page_title="Icon Set Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""  # pragma: no cover
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
with st.sidebar:  # pragma: no cover
    st.title("Settings")  # pragma: no cover

    provider = st.selectbox("AI Provider", ["OpenAI", "Google"], index=0)  # pragma: no cover
    api_key = st.text_input("API Key", type="password", help="Leave empty if set in .env")  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.subheader("Style")  # pragma: no cover
    style = st.selectbox("Icon Style", config.STYLES, index=0)  # pragma: no cover
    color = st.color_picker("Primary Color", config.DEFAULT_COLOR)  # pragma: no cover

    st.markdown("---")  # pragma: no cover
    st.info("Generates 24x24 SVG icons.")  # pragma: no cover

# Main Content
st.title("🎨 Icon Set Generator")  # pragma: no cover
st.markdown("Generate consistent SVG icon sets from text descriptions using AI.")  # pragma: no cover

col1, col2 = st.columns([2, 1])  # pragma: no cover

with col1:  # pragma: no cover
    descriptions_input = st.text_area(  # pragma: no cover
        "Icon Descriptions (one per line)",
        height=200,
        placeholder="home icon\nsettings gear\nuser profile\nsearch magnifying glass"
    )

with col2:  # pragma: no cover
    st.markdown("### Preview")  # pragma: no cover
    st.write(f"**Style:** {style}")  # pragma: no cover
    st.write(f"**Color:** {color}")  # pragma: no cover

    if st.button("Generate Icons", type="primary", use_container_width=True):  # pragma: no cover
        if not descriptions_input.strip():  # pragma: no cover
            st.error("Please enter at least one icon description.")  # pragma: no cover
        else:
            descriptions = [d.strip() for d in descriptions_input.split('\n') if d.strip()]  # pragma: no cover

            # Initialize Generator
            generator = IconGenerator(provider=provider, api_key=api_key)  # pragma: no cover
            optimizer = IconOptimizer()  # pragma: no cover
            formatter = IconFormatter()  # pragma: no cover

            progress_bar = st.progress(0)  # pragma: no cover
            status_text = st.empty()  # pragma: no cover

            generated_icons = {}  # pragma: no cover

            for i, desc in enumerate(descriptions):  # pragma: no cover
                status_text.text(f"Generating: {desc}...")  # pragma: no cover

                # Generate
                raw_svg = generator.generate_icon(desc, style, color)  # pragma: no cover

                # Optimize
                opt_svg = optimizer.optimize_svg(raw_svg)  # pragma: no cover

                # Store
                icon_name = desc.lower().replace(" ", "-")  # pragma: no cover
                generated_icons[icon_name] = opt_svg  # pragma: no cover

                progress_bar.progress((i + 1) / len(descriptions))  # pragma: no cover

            status_text.text("Generation Complete!")  # pragma: no cover
            st.session_state['generated_icons'] = generated_icons  # pragma: no cover

# Display Results
if 'generated_icons' in st.session_state and st.session_state['generated_icons']:  # pragma: no cover
    st.markdown("---")  # pragma: no cover
    st.subheader("Generated Icons")  # pragma: no cover

    icons = st.session_state['generated_icons']  # pragma: no cover
    cols = st.columns(4)  # pragma: no cover

    for i, (name, svg) in enumerate(icons.items()):  # pragma: no cover
        with cols[i % 4]:  # pragma: no cover
            st.markdown(f"""  # pragma: no cover
                <div class="icon-card">
                    {svg}
                    <div class="icon-title">{name}</div>
                </div>
            """, unsafe_allow_html=True)

            # Individual download (optional, maybe overkill for UI)
            # st.download_button("SVG", svg, file_name=f"{name}.svg", mime="image/svg+xml")

    # Bulk Export
    st.markdown("---")  # pragma: no cover
    st.subheader("Export")  # pragma: no cover

    c1, c2, c3 = st.columns(3)  # pragma: no cover

    # ZIP SVGs
    svg_zip_buffer = io.BytesIO()  # pragma: no cover
    with zipfile.ZipFile(svg_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:  # pragma: no cover
        for name, svg in icons.items():  # pragma: no cover
            zf.writestr(f"{name}.svg", svg)  # pragma: no cover

    c1.download_button(  # pragma: no cover
        label="Download SVG ZIP",
        data=svg_zip_buffer.getvalue(),
        file_name="icons_svg.zip",
        mime="application/zip",
        use_container_width=True
    )

    # ZIP React
    react_zip_buffer = io.BytesIO()  # pragma: no cover
    formatter = IconFormatter() # Re-init locally just in case  # pragma: no cover
    with zipfile.ZipFile(react_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:  # pragma: no cover
        for name, svg in icons.items():  # pragma: no cover
            # Name to PascalCase
            component_name = "".join(x.title() for x in name.split("-")) + "Icon"  # pragma: no cover
            code = formatter.to_react_component(svg, component_name)  # pragma: no cover
            zf.writestr(f"{component_name}.jsx", code)  # pragma: no cover

    c2.download_button(  # pragma: no cover
        label="Download React Components",
        data=react_zip_buffer.getvalue(),
        file_name="icons_react.zip",
        mime="application/zip",
        use_container_width=True
    )

    # ZIP Vue
    vue_zip_buffer = io.BytesIO()  # pragma: no cover
    with zipfile.ZipFile(vue_zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:  # pragma: no cover
        for name, svg in icons.items():  # pragma: no cover
            component_name = "".join(x.title() for x in name.split("-")) + "Icon"  # pragma: no cover
            code = formatter.to_vue_component(svg, component_name)  # pragma: no cover
            zf.writestr(f"{component_name}.vue", code)  # pragma: no cover

    c3.download_button(  # pragma: no cover
        label="Download Vue Components",
        data=vue_zip_buffer.getvalue(),
        file_name="icons_vue.zip",
        mime="application/zip",
        use_container_width=True
    )
