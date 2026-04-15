## 2024-05-24 - Descriptive labels for collapsed inputs in Streamlit
**Learning:** In Streamlit, when `label_visibility="collapsed"` is used to visually hide a label, the first argument to the component is still used as the `aria-label` for screen readers. Using a generic string like "hidden_label" makes the input inaccessible.
**Action:** Always provide a meaningful, translated string as the first argument to input components, even when the label is visually collapsed.
