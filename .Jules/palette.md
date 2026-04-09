## 2025-02-12 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when a widget uses `label_visibility="collapsed"` to visually hide its label, the first string argument is still used as its `aria-label` attribute. Passing a dummy string like "hidden_label" causes screen readers to read "hidden_label" to users, confusing them.
**Action:** Always pass a descriptive, localized label as the first argument to Streamlit input widgets, even if `label_visibility="collapsed"` is used.
