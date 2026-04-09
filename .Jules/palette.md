## 2024-05-18 - Streamlit label_visibility="collapsed" Accessibility
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to hide a label visually, the first argument is still used as the `aria-label`. Always provide a meaningful, descriptive string as the label argument to ensure screen reader accessibility.
**Action:** Replace placeholder strings like `"hidden_label"` or `"Language"` with translated, context-aware strings (e.g., `base_label` or `tr.get('language_selector_label', 'Language')`) when using `label_visibility="collapsed"`.
