## 2026-04-26 - Add tooltips explaining why buttons are disabled
**Learning:** In interactive Streamlit applications, users can get confused when action buttons (like start/stop server) are disabled without explanation. Adding dynamic `help` tooltips based on the button state improves accessibility and user understanding by providing clear reasons for the disabled state (e.g., "Server is not running").
**Action:** Always provide contextual `help` text for `st.button` components, particularly when they can be dynamically disabled, to explicitly communicate state to users and screen readers.
