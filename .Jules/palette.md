## 2024-05-13 - [Streamlit Hidden Labels]
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to hide a label visually, the first argument is still used as the `aria-label`. Using "hidden_label" or a generic name creates a poor screen reader experience.
**Action:** Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility, even when `label_visibility="collapsed"`.
