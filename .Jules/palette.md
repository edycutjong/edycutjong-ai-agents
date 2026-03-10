## 2024-05-15 - [Initial]
**Learning:** [insight]
**Action:** [application]

## 2024-06-03 - Streamlit Accessibility for Collapsed Labels
**Learning:** In Streamlit, when setting `label_visibility="collapsed"` for form inputs like `st.text_area`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like `"hidden_label"` results in a non-descriptive and inaccessible experience for users relying on screen readers.
**Action:** Always provide a descriptive, localized label as the first argument to Streamlit input components, even when the label is visually collapsed, to ensure proper accessibility (`aria-label`).
