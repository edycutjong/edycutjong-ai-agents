## 2025-02-27 - [Streamlit Text Area Accessibility]
**Learning:** When using `label_visibility="collapsed"` in Streamlit to hide a label visually, the first argument is still used as the `aria-label`. Generic placeholder strings like `"hidden_label"` cause screen readers to announce unhelpful text.
**Action:** Always provide a meaningful, descriptive string as the label argument for Streamlit inputs, even when visually collapsing them, to ensure proper screen reader accessibility.
