## 2025-02-25 - Search Empty State Recovery
**Learning:** Streamlit's `st_keyup` component maintains its own frontend state, making it difficult to clear the input field programmatically without forcing a component reset.
**Action:** When implementing "Clear" functionality for `st_keyup`, use a dynamic key (e.g., `key=f"search_{suffix}"`) and increment the suffix to force a fresh component instance.
