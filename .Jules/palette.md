## 2026-03-18 - Fix accessibility on hidden labels
**Learning:** In Streamlit, when setting `label_visibility='collapsed'`, the first argument (the label string) is still used as the `aria-label` for screen readers. Using a dummy value like 'hidden_label' harms accessibility because screen readers will announce it as 'hidden_label'.
**Action:** Always provide a descriptive, localized label as the first argument to Streamlit input components (like `st.text_area`), even if the visual label is collapsed.
