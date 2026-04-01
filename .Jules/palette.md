## 2024-04-01 - Streamlit collapsed label accessibility
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to visually hide a label, the first argument is still used as the `aria-label`. Passing "hidden_label" causes screen readers to announce "hidden_label" instead of what the input is for.
**Action:** Always provide a meaningful, descriptive string as the first argument to `st.text_area` and `st.text_input` even when the label is visually collapsed to ensure screen reader accessibility.
