
## 2024-04-27 - Streamlit Disabled States & Screen Reader Labels
**Learning:** In Streamlit applications, adding a `help` attribute to disabled buttons provides necessary context for users on why an action is unavailable. Additionally, when using `label_visibility="collapsed"` on inputs like `st.text_area`, Streamlit still exposes the label parameter to screen readers. Therefore, using a generic label like `"hidden_label"` creates a poor accessibility experience.
**Action:** Always provide descriptive base labels for Streamlit inputs even when hidden visually, and always provide contextual tooltips (`help`) for disabled interactive elements.
