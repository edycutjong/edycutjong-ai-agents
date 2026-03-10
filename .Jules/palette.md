## 2024-05-24 - AI Agents Hub UX Audit
**Learning:** This is a Streamlit application serving as a hub for 182 AI agents. The UI is built using standard Streamlit components with some custom CSS injection.

**Observations:**
1.  **Search Input**: The search input `st_keyup` uses a custom component. The label has an emoji "🔍".
2.  **Buttons**: Standard Streamlit buttons are used. Some have emojis in labels.
3.  **Cards**: Agent cards are rendered using standard containers with custom CSS classes like `.agent-card`.
4.  **Accessibility**:
    -   Images/Icons are mostly emojis or text-based.
    -   Color contrast seems okay based on CSS variables (gray/purple theme).
    -   Keyboard navigation in Streamlit is generally handled by the framework but can be clunky.
    -   Missing explicit ARIA labels on some custom interactive elements if they were raw HTML, but here most are Streamlit widgets.

**Opportunity**:
The search input in the sidebar is a key interaction point. Currently, it just has a placeholder "Search agents...".
Streamlit's `st.text_input` (and `st_keyup`) renders a label.
A potential quick win is ensuring the search input has a clear, accessible label and perhaps adding a "Clear" button or similar if it's not present, but `st_keyup` might be limited.

Let's look at `app.py` again specifically for the search implementation.
```python
        # Search Input (real-time keyup to allow button disabled state to toggle on typing)
        search_val = st_keyup(f"🔍 {tr['search']}", placeholder=tr['search'], key="keyup_search_val", debounce=100)
```
The label is "🔍 Search agents...". This is visible.

**Better Opportunity**:
The "Surprise Me" button.
```python
        # Surprise Me button
        st.markdown(f"<small>{tr['surprise_hint']}</small>", unsafe_allow_html=True)
        if st.button(tr['surprise_btn'], key="surprise_me", use_container_width=True):
```
It's a standard button.

**Another Opportunity**:
The Agent Cards in `_render_hub`.
```python
                    with st.container(border=True):
                        # ...
                        if agent["has_main"]:
                            if st.button(tr['view'], key=f"view_{key}", use_container_width=True):
                                # ...
```
The "View ->" button is generic. For screen readers, having many "View ->" buttons is bad practice because the context is lost if they navigate by buttons. It should be "View [Agent Name]".

**Plan**:
Update the "View ->" button label or aria-label to include the agent name for better accessibility.
However, Streamlit buttons don't easily support `aria-label` directly in the python API unless we use `help` (tooltip) which renders as a title attribute, or if we change the label text itself.
Changing the visible label to "View [Agent Name]" might clutter the UI if names are long.

Streamlit's `st.button` has a `help` parameter.
`st.button(label, key=None, help=None, ...)`
Adding `help=f"View {agent_name}"` would add a tooltip, which is a small UX win and improves accessibility for mouse users, and some screen readers might read the title/tooltip.

**Alternative**:
Look at `app.py` custom CSS.
There are custom styles for buttons.
```css
    /* Button micro-animation */
    .stButton > button {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
```

**Selected Micro-UX**:
Add tooltips (`help` parameter) to the "View" buttons in the agent grid to indicate *which* agent is being viewed. This is a "Helpful Addition" and "Accessibility Check".

Also, check the "Surprise Me" button. Adding a tooltip there like "Randomly select an agent" could be nice.

Let's verify if `st.button` supports `help`. Yes it does.

Let's also look at the "Run" button in the agent detail view.
```python
            st.button(
                tr['run_btn'],
                key=f"run_{agent_key}",
                use_container_width=True,
                disabled=is_running,
                on_click=_on_run_click
            )
```
Adding a tooltip here explaining what it does (e.g., "Execute this agent with your input") would be good.

**Primary Task**:
Enhance the "View" buttons in the Hub grid with dynamic tooltips (`help` param) containing the agent's name. This improves context for users hovering and potentially for accessibility tools.

**Secondary Task**:
Add a tooltip to the "Surprise Me" button.

Let's refine the plan.
1.  Modify `_render_hub` in `app.py`.
2.  Find the loop where agent cards are rendered.
3.  Update `st.button(tr['view'], ...)` to include `help=f"{tr['view']} {agent['name']}"` or similar.
4.  Modify `main` function to add help to "Surprise Me" button.

Wait, `tr['view']` is "View ->".
The tooltip should probably say "View details for [Agent Name]".

Let's check `i18n.py` for potential string additions? Or just construct it.
I can use the existing translations.

Let's double check `app.py` content again to be sure where to edit.
