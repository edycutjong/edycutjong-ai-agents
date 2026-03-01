## 2024-03-01 - Fix collapsed label accessibility
**Learning:** Streamlit's `label_visibility="collapsed"` hides the label visually, but screen readers still read the text string provided as the first argument. Using a placeholder like "hidden_label" causes screen readers to announce meaningless text.
**Action:** Always provide a real, descriptive (and localized if possible) string for the label, even if `label_visibility="collapsed"` is used.
