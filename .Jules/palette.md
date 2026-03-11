## 2024-05-24 - Streamlit collapsed label accessibility issue
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" causes poor accessibility.
**Action:** Always provide a descriptive, localized label rather than a dummy value like 'hidden_label' to ensure accessibility, even if the label is visually collapsed.
