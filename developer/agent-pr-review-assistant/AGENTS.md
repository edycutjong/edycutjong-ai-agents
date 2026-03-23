# PR Review Assistant Agent

## Overview
Python Streamlit agent that reviews a GitHub PR URL, runs checks, and outputs a structured code review.

## Tech Stack
- **Language:** Python 3.11+
- **UI:** Streamlit
- **Testing:** pytest
- **Deps:** requirements.txt

## Features
- Streamlit web UI with PR URL input
- Fetch PR diff via GitHub API
- Analyze changed files for common issues
- Check for: missing tests, TODO comments, large functions, hardcoded values
- Security pattern scanning
- Structured review output with sections
- Severity badges (critical/warning/info)
- Copy review as Markdown comment

## Design
Streamlit clean white theme, review card display

## Commands
- **Dev:** `streamlit run app.py`
- **Test:** `pytest`
- **Deps:** `pip install -r requirements.txt`
