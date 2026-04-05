## 2025-02-12 - Streamlit Collapsed Label Accessibility
**Learning:** When using `label_visibility="collapsed"` in Streamlit widgets to hide labels visually, the first argument (label string) is still used as the `aria-label` for screen readers. Using a placeholder like "hidden_label" breaks accessibility.
**Action:** Always provide a meaningful, descriptive string as the label argument for Streamlit inputs, even when visually collapsing the label.
