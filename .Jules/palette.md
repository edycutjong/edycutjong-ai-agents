## 2024-05-14 - Improve Streamlit input accessibility
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using a generic dummy value like "hidden_label" makes the component inaccessible.
**Action:** Always provide a descriptive, localized label as the first argument to Streamlit input components, even when `label_visibility="collapsed"` is used to visually hide the label.
