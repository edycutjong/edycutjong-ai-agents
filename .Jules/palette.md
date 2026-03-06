## 2025-03-06 - Streamlit Collapsed Labels Accessibility
**Learning:** When setting `label_visibility='collapsed'` in Streamlit components (like `st.text_area`), the first argument (the label string) is still used as the `aria-label` for screen readers. Using a dummy value like 'hidden_label' creates poor accessibility.
**Action:** Always provide a descriptive, localized label as the first argument to Streamlit input components, even when the visual label is collapsed.
