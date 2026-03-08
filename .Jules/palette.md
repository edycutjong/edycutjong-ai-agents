## 2026-03-08 - Streamlit Collapsed Labels Accessibility
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" creates a poor experience for screen reader users.
**Action:** Always provide a descriptive, localized label as the first argument, even when it will be visually hidden.
