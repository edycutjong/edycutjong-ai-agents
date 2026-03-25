## 2025-03-05 - Streamlit Input Accessibility
**Learning:** When using `label_visibility="collapsed"` in Streamlit inputs to hide the label visually, the first argument (label) is still used as the `aria-label`. Using a dummy string like `"hidden_label"` breaks screen reader accessibility for that input.
**Action:** Always provide a meaningful, descriptive string as the label argument to Streamlit input components (like `st.text_area`, `st.text_input`), even if it is visually hidden using `label_visibility="collapsed"`.
