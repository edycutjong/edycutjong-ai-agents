## 2024-03-16 - Descriptive labels for collapsed text areas
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" harms accessibility.
**Action:** Always provide a descriptive, localized label (e.g., `base_label`) rather than a dummy value like 'hidden_label' when hiding labels to ensure accessibility.
