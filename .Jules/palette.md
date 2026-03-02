## 2026-03-02 - Streamlit hidden_label accessibility
**Learning:** In Streamlit, when setting label_visibility='collapsed', the first argument (the label string) is still used as the aria-label for screen readers. A dummy value like 'hidden_label' reduces accessibility.
**Action:** Always provide a descriptive, localized label rather than a dummy value like 'hidden_label' to ensure accessibility.
