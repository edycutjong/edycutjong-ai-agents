## 2024-05-18 - Streamlit Screen Reader Label
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using a dummy value like "hidden_label" makes the input inaccessible.
**Action:** Always provide a descriptive, localized label for Streamlit inputs even when `label_visibility` is collapsed to ensure accessibility.
