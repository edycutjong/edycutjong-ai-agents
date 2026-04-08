## 2024-03-24 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit apps, when using `label_visibility="collapsed"` to visually hide a label, the first argument is still used as the `aria-label` for screen readers. Using a generic string like "hidden_label" makes the input completely inaccessible to screen reader users.
**Action:** Always provide a meaningful, descriptive string as the label argument to `st.text_input` and `st.text_area` to ensure screen reader accessibility, even if `label_visibility="collapsed"` is used.
