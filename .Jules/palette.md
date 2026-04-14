## 2024-04-14 - Streamlit Collapsed Labels Accessibility
**Learning:** When using `label_visibility="collapsed"` in Streamlit widgets to hide labels visually, the first argument is still used as the `aria-label` by screen readers. Providing a dummy string like `"hidden_label"` creates a poor accessibility experience.
**Action:** Always provide a meaningful, descriptive string as the label argument to Streamlit widgets, even if `label_visibility="collapsed"` is used, to ensure proper screen reader accessibility.
