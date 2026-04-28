## 2026-04-28 - Screen reader accessibility for collapsed labels
**Learning:** Even when `label_visibility='collapsed'` is set on Streamlit input elements (like `st.text_area`), Streamlit still exposes the label parameter string to screen readers.
**Action:** Always provide a descriptive base label string instead of a generic one (like 'hidden_label') for better accessibility.
