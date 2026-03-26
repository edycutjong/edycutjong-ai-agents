## 2024-03-12 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when `label_visibility='collapsed'` is used, the first argument (label string) is still exposed as the `aria-label` for screen readers. Dummy values like 'hidden_label' make the field inaccessible.
**Action:** Always provide a descriptive, localized label as the first argument to input fields, even when visually hiding it with `label_visibility='collapsed'`.
