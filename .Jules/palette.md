## 2024-05-24 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when hiding a label using `label_visibility="collapsed"`, the first argument passed to the input component (like `st.text_area`) is still used under the hood as the `aria-label`. Using placeholder text like `"hidden_label"` severely degrades the screen reader experience.
**Action:** Always provide the full, descriptive, localized string as the first argument to Streamlit input components, even when visually hiding them with `label_visibility="collapsed"`.
