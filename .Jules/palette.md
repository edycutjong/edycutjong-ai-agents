## 2024-05-24 - Add meaningful ARIA label to hidden text area
**Learning:** In Streamlit, when hiding a label visually using `label_visibility="collapsed"`, the first argument is still used as the `aria-label`. Using generic strings like "hidden_label" causes accessibility issues for screen readers.
**Action:** Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility.
