## 2026-04-24 - Adding helpful context to disabled UI elements
**Learning:** In Streamlit applications, disabled buttons (like disabled search or run buttons) don't naturally convey to users *why* they are disabled. Screen reader users and sighted users both benefit from understanding the criteria required to activate the button.
**Action:** Utilize the `help` parameter on `st.button` components to provide contextual tooltips, especially when `disabled=True`. This explains why a button is currently inactive and provides actionable guidance.
