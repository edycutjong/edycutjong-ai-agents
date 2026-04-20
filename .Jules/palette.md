## 2025-02-18 - Accessible Hidden Labels in Streamlit
**Learning:** In Streamlit components like `st.text_area` or `st.text_input`, setting `label_visibility="collapsed"` hides the label visually, but the first argument (the label string) is still rendered as the `aria-label` for screen readers. Using placeholder strings like "hidden_label" creates a poor, unhelpful accessibility experience.
**Action:** Always provide a meaningful, descriptive string as the first argument to Streamlit input components, even when visually collapsing the label.
