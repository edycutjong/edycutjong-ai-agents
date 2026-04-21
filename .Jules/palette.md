## 2026-04-21 - Screen Reader ARIA Label with Collapsed Streamlit Components
**Learning:** In Streamlit applications, when using `label_visibility="collapsed"` to hide a label visually (e.g., in a text area or selectbox), the first argument is still used as the `aria-label` for screen readers. Using a generic string like 'hidden_label' makes the element inaccessible.
**Action:** Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility, even if the label is set to be visually collapsed.
