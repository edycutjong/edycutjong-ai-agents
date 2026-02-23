## 2026-02-23 - Accessibility of Hidden Labels
**Learning:** Streamlit's `label_visibility='collapsed'` still exposes the label to screen readers. Using "hidden_label" as the label creates a poor screen reader experience. Always use a descriptive label even if it's visually hidden.
**Action:** When hiding labels in Streamlit, ensure the programmatic label is descriptive and matches any custom visual label provided.
