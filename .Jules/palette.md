## 2024-04-18 - Streamlit label_visibility and aria-label
**Learning:** In Streamlit apps, when using `label_visibility="collapsed"` to hide a label visually, the first argument is still used as the `aria-label` for the rendered HTML component (like an input or textarea).
**Action:** Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility, avoiding generic hidden strings like "hidden_label".
