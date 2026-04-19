## 2024-05-18 - Screen Reader Accessibility in Streamlit Collapsed Labels
**Learning:** When using `label_visibility="collapsed"` in Streamlit to visually hide a label, the first argument provided to the component is still used as the `aria-label`. Passing a placeholder like "hidden_label" causes screen readers to announce an unhelpful or confusing label.
**Action:** Always provide a meaningful, descriptive string as the label argument for Streamlit input components (like `st.text_area` or `st.selectbox`), even when `label_visibility="collapsed"` is used.
