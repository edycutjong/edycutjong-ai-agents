## 2024-05-18 - Screen Reader Accessibility in Streamlit Input Elements
**Learning:** Even when `label_visibility='collapsed'` is set on Streamlit input elements (like `st.text_area`), Streamlit still exposes the label parameter string to screen readers.
**Action:** Always provide a descriptive base label string instead of a generic one (like "hidden_label") when hiding labels visually, ensuring screen reader users still hear the correct context.
