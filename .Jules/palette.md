## 2024-05-15 - Streamlit Collapsed Label Accessibility
**Learning:** When using `label_visibility='collapsed'` in Streamlit, the first argument (the label string) is still used as the `aria-label` for screen readers. Using a dummy value like "hidden_label" creates an accessibility issue.
**Action:** Always provide a descriptive, localized label as the first argument to Streamlit input components, even if it is visually hidden using `label_visibility='collapsed'`.
