## 2024-05-18 - Streamlit label_visibility accessibility
**Learning:** When setting `label_visibility='collapsed'` in Streamlit, the label string is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" creates a poor experience.
**Action:** Always provide a descriptive, localized label as the first argument to input components, even when visually hidden.
