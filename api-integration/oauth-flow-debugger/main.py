import streamlit as st
import os
import sys
import json
from datetime import datetime

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agent import oauth_tools
from agent.debugger_agent import DebuggerAgent

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* Global Styles */
        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #f8fafc;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
            border-right: 1px solid #334155;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #94a3b8;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background-color: #3b82f6;
            color: white;
        }

        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5), 0 4px 6px -2px rgba(59, 130, 246, 0.3);
            border-color: transparent;
            color: white;
        }

        /* Inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: #334155;
            color: white;
            border: 1px solid #475569;
            border-radius: 6px;
        }

        /* JSON Display */
        .stJson {
            background-color: #0f172a;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="OAuth Flow Debugger",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_custom_css()

    # Initialize Session State
    if "auth_url" not in st.session_state:
        st.session_state.auth_url = "https://example.com/oauth/authorize"
    if "token_url" not in st.session_state:
        st.session_state.token_url = "https://example.com/oauth/token"
    if "scopes" not in st.session_state:
        st.session_state.scopes = "openid profile email"
    if "last_provider" not in st.session_state:
        st.session_state.last_provider = "Custom"

    # Sidebar Configuration
    with st.sidebar:
        st.title("🔐 OAuth Config")

        provider_data = {
            "Custom": {},
            "Google": {
                "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "scopes": "openid profile email"
            },
            "GitHub": {
                "auth_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "scopes": "read:user user:email"
            },
            "Auth0": {
                "auth_url": "https://{YOUR_DOMAIN}/authorize",
                "token_url": "https://{YOUR_DOMAIN}/oauth/token",
                "scopes": "openid profile email"
            },
             "Microsoft": {
                "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                "scopes": "User.Read"
            }
        }

        provider = st.selectbox("Provider Preset", list(provider_data.keys()))

        # Update session state if provider changes
        if st.session_state.last_provider != provider:
            preset = provider_data[provider]  # pragma: no cover
            if preset:  # pragma: no cover
                st.session_state.auth_url = preset.get("auth_url", st.session_state.auth_url)  # pragma: no cover
                st.session_state.token_url = preset.get("token_url", st.session_state.token_url)  # pragma: no cover
                st.session_state.scopes = preset.get("scopes", st.session_state.scopes)  # pragma: no cover
            st.session_state.last_provider = provider  # pragma: no cover

        client_id = st.text_input("Client ID", value="")
        client_secret = st.text_input("Client Secret", type="password", value="")
        auth_url = st.text_input("Authorization URL", key="auth_url")
        token_url = st.text_input("Token URL", key="token_url")
        redirect_uri = st.text_input("Redirect URI", value="http://localhost:8501/callback")
        scopes = st.text_input("Scopes (space separated)", key="scopes")

        st.divider()
        st.markdown("### AI Agent Settings")
        api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")

    # Initialize Agent
    debugger_agent = DebuggerAgent(api_key=api_key)

    # Main Area
    st.title("OAuth Flow Debugger")
    st.markdown("Trace, inspect, and debug OAuth 2.0 flows with AI assistance.")

    # Tabs
    tab_trace, tab_inspect, tab_ai, tab_config = st.tabs(["🚀 Trace Flow", "🔍 Token Inspector", "🤖 AI Analysis", "✅ Config Validator"])

    # Tab 1: Trace Flow
    with tab_trace:
        flow_type = st.radio("Select Flow", ["Authorization Code", "Client Credentials"], horizontal=True)

        if flow_type == "Authorization Code":
            st.subheader("Authorization Code Flow")

            # Step 1: Authorization Request
            st.markdown("#### 1. Authorization Request")
            state = st.text_input("State (Optional)", value="xyz123")

            if st.button("Generate Auth URL"):
                generated_url = oauth_tools.generate_auth_url(client_id, auth_url, redirect_uri, scopes, state)  # pragma: no cover
                st.code(generated_url, language="text")  # pragma: no cover
                st.markdown(f"[Click to Authorize]({generated_url})")  # pragma: no cover
                st.info("Click the link above to authorize. After redirection, copy the 'code' parameter from the URL and paste it below.")  # pragma: no cover

            # Step 2: Token Exchange
            st.markdown("#### 2. Exchange Code for Token")
            auth_code = st.text_input("Authorization Code", placeholder="Paste code here...")

            if st.button("Exchange Code"):
                if not auth_code:  # pragma: no cover
                    st.warning("Please enter an authorization code.")  # pragma: no cover
                else:
                    with st.spinner("Exchanging code..."):  # pragma: no cover
                        result = oauth_tools.exchange_code_for_token(client_id, client_secret, token_url, auth_code, redirect_uri)  # pragma: no cover
                        st.json(result)  # pragma: no cover

                        if "access_token" in result:  # pragma: no cover
                            st.session_state.last_token = result["access_token"]  # pragma: no cover
                            st.success("Token received!")  # pragma: no cover
                        elif "error" in result:  # pragma: no cover
                            st.error(f"Error: {result.get('error')}")  # pragma: no cover
                            st.session_state.last_error = json.dumps(result, indent=2)  # pragma: no cover

        elif flow_type == "Client Credentials":  # pragma: no cover
            st.subheader("Client Credentials Flow")  # pragma: no cover

            if st.button("Get Token"):  # pragma: no cover
                with st.spinner("Requesting token..."):  # pragma: no cover
                    result = oauth_tools.get_client_credentials_token(client_id, client_secret, token_url, scopes)  # pragma: no cover
                    st.json(result)  # pragma: no cover

                    if "access_token" in result:  # pragma: no cover
                        st.session_state.last_token = result["access_token"]  # pragma: no cover
                        st.success("Token received!")  # pragma: no cover
                    elif "error" in result:  # pragma: no cover
                        st.error(f"Error: {result.get('error')}")  # pragma: no cover
                        st.session_state.last_error = json.dumps(result, indent=2)  # pragma: no cover

    # Tab 2: Token Inspector
    with tab_inspect:
        st.subheader("JWT Inspector")
        token_input = st.text_area("Paste JWT Token", value=st.session_state.get("last_token", ""), height=150)

        if st.button("Decode Token"):
            if not token_input:  # pragma: no cover
                st.warning("Please paste a token.")  # pragma: no cover
            else:
                decoded = oauth_tools.decode_jwt(token_input)  # pragma: no cover
                if decoded.get("valid_structure"):  # pragma: no cover
                    col1, col2 = st.columns(2)  # pragma: no cover
                    with col1:  # pragma: no cover
                        st.markdown("**Header**")  # pragma: no cover
                        st.json(decoded["header"])  # pragma: no cover
                    with col2:  # pragma: no cover
                        st.markdown("**Payload**")  # pragma: no cover
                        st.json(decoded["payload"])  # pragma: no cover
                else:
                    st.error(f"Invalid JWT: {decoded.get('error')}")  # pragma: no cover

    # Tab 3: AI Analysis
    with tab_ai:
        st.subheader("AI Error Analysis")
        error_input = st.text_area("Paste Error Log / JSON", value=st.session_state.get("last_error", ""), height=150)
        context_input = st.text_input("Additional Context (e.g. provider name, steps taken)", value=f"Provider: {provider}")

        if st.button("Analyze Error"):
            if not api_key:  # pragma: no cover
                st.error("OpenAI API Key is required for this feature.")  # pragma: no cover
            elif not error_input:  # pragma: no cover
                st.warning("Please provide an error message.")  # pragma: no cover
            else:
                with st.spinner("Analyzing with AI..."):  # pragma: no cover
                    analysis = debugger_agent.analyze_error(error_input, context_input)  # pragma: no cover
                    st.markdown(analysis)  # pragma: no cover

    # Tab 4: Config Validator
    with tab_config:
        st.subheader("Configuration Validator")

        # Local Checks
        st.markdown("#### Redirect URI Check")
        issues = oauth_tools.validate_redirect_uri(redirect_uri)
        if issues:
            for issue in issues:  # pragma: no cover
                st.error(f"❌ {issue}")  # pragma: no cover
        else:
            st.success("✅ Redirect URI format looks good.")

        # AI Check
        st.markdown("#### AI Security Audit")
        if st.button("Audit Configuration"):
            if not api_key:  # pragma: no cover
                st.error("OpenAI API Key is required for this feature.")  # pragma: no cover
            else:
                config_summary = {  # pragma: no cover
                    "client_id": client_id,
                    "auth_url": auth_url,
                    "token_url": token_url,
                    "redirect_uri": redirect_uri,
                    "scopes": scopes,
                    "provider_preset": provider
                }
                with st.spinner("Auditing configuration..."):  # pragma: no cover
                    audit_result = debugger_agent.analyze_configuration(json.dumps(config_summary))  # pragma: no cover
                    st.markdown(audit_result)  # pragma: no cover

if __name__ == "__main__":
    main()
