## 2025-04-04 - Screen Reader Labels in Streamlit collapsed fields
**Learning:** In Streamlit, when using `label_visibility="collapsed"` to visually hide an input label, the first string argument is still used as the `aria-label`. Passing placeholders like "hidden_label" degrades accessibility for screen reader users.
**Action:** Always pass a descriptive label (e.g. `base_label`) as the first argument to `st.text_area` or other inputs, even when `label_visibility="collapsed"`.
