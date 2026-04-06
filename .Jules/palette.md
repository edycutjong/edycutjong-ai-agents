## 2024-04-06 - Streamlit Collapsed Labels Accessibility
**Learning:** In Streamlit apps, when using `label_visibility="collapsed"` to visually hide an input label, the first argument to the component (the label text) is still mapped to the `aria-label`. Using generic names like "hidden_label" causes poor screen reader experiences.
**Action:** Always provide a meaningful, descriptive string as the first argument to Streamlit input components, even if `label_visibility="collapsed"` is set, to ensure screen reader accessibility.
