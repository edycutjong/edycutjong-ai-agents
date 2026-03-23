## 2024-03-23 - Init

## 2024-03-23 - Accessibility of collapsed Streamlit labels
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like 'hidden_label' creates poor accessibility.
**Action:** Always provide a descriptive, localized label as the first argument for inputs, even if visually collapsed.
