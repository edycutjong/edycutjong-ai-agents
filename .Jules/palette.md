## 2024-03-13 - Initial Palette learning
**Learning:** Understanding the base UI of the AI Agent Hub. The hub is a Streamlit app.
**Action:** Always consider Streamlit limitations when adding UX enhancements.
## 2024-03-13 - Streamlit Accessibility Labels
**Learning:** In Streamlit, when setting `label_visibility="collapsed"`, the first argument (the label string) is still used as the `aria-label` for screen readers. Always provide a descriptive, localized label rather than a dummy value like "hidden_label" to ensure accessibility.
**Action:** Replace dummy labels in `st.text_area` and similar widgets with localized strings.
