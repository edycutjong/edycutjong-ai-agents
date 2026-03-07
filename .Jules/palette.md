## 2025-03-07 - Streamlit collapsed labels still expose aria-label
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" degrades accessibility.
**Action:** Always provide a descriptive, localized label rather than a dummy value like 'hidden_label' to ensure accessibility, even when the label is visually collapsed.
