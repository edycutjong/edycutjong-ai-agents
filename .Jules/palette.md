## 2024-03-24 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Providing a dummy value like 'hidden_label' degrades accessibility.
**Action:** Always provide a descriptive, localized label rather than a dummy value to ensure proper screen reader accessibility.
