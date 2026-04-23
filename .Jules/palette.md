## 2024-05-24 - Streamlit Collapsed Label Screen Reader Behavior
**Learning:** Even when `label_visibility="collapsed"` is set on `st.text_area` (and likely other inputs), Streamlit still exposes the first string argument (the label) to screen readers. Using a generic string like `"hidden_label"` creates a poor accessibility experience.
**Action:** Always provide a descriptive label string (like `base_label`) to Streamlit inputs, even if the visual label is collapsed or hidden.
