## 2024-05-14 - Replace dummy labels with descriptive ones when label_visibility="collapsed" is used
**Learning:** In Streamlit, when setting `label_visibility="collapsed"`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using dummy values like "hidden_label" or generic values compromises accessibility.
**Action:** Always provide a descriptive, localized label rather than a dummy value to ensure proper screen reader accessibility, even when the label is visually hidden.
