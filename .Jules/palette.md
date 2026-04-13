## 2026-04-13 - Streamlit Collapsed Labels Accessibility
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to visually hide an input label, the first argument (the label string) is still used as the `aria-label` for screen readers. Using a generic string like `"hidden_label"` creates a poor accessibility experience.
**Action:** Always provide a descriptive, meaningful string as the label argument for Streamlit inputs, even if it is visually collapsed, to ensure proper screen reader support.
