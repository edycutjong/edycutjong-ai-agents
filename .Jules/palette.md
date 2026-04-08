## 2024-03-29 - [Screen Reader Accessibility with Streamlit's Collapsed Labels]
**Learning:** In Streamlit, when `label_visibility="collapsed"` is used to visually hide an input's label, the first positional argument is still injected as the `aria-label`. Passing placeholder strings like `"hidden_label"` creates a poor screen reader experience, as users hear "hidden label" instead of the field's actual purpose.
**Action:** Always provide a descriptive, localized string as the first argument to Streamlit input components, even when `label_visibility` is set to `"collapsed"`.
