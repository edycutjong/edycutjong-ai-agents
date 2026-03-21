## 2024-05-24 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. A dummy value like 'hidden_label' makes the input inaccessible.
**Action:** Always provide a descriptive, localized label rather than a dummy value to ensure accessibility, even when the label is visually collapsed.
