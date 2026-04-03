## 2026-04-03 - Streamlit Collapsed Label Accessibility
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to hide a label visually, the first argument is still used as the `aria-label`. Generic strings like "hidden_label" break screen reader accessibility.
**Action:** Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility.
