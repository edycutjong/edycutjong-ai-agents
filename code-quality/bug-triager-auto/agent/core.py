import json
import difflib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
try:
    from config import Config
    from prompts.system_prompts import (
        SEVERITY_PROMPT,
        ROUTING_PROMPT,
        SENTIMENT_PROMPT,
        FIX_SUGGESTION_PROMPT
    )
except ImportError:
    # Fallback for relative imports if run as a package
    from ..config import Config
    from ..prompts.system_prompts import (
        SEVERITY_PROMPT,
        ROUTING_PROMPT,
        SENTIMENT_PROMPT,
        FIX_SUGGESTION_PROMPT
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BugTriagerAgent:
    def __init__(self, issue_tracker):
        self.issue_tracker = issue_tracker
        self.llm = None
        if not Config.DEMO_MODE and Config.OPENAI_API_KEY:
            self.llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", api_key=Config.OPENAI_API_KEY)
        else:
            logger.info("Running in DEMO MODE (Mock LLM)")

    def _call_llm(self, prompt_template: PromptTemplate, **kwargs) -> str:
        """
        Calls the LLM with the formatted prompt. Returns a mock response in demo mode.
        """
        prompt = prompt_template.format(**kwargs)

        if Config.DEMO_MODE or not self.llm:
            # Return mock JSON based on the prompt type
            if "severity" in prompt.lower():
                return json.dumps({
                    "severity": "medium",
                    "labels": ["bug", "needs-triage"],
                    "reasoning": "Standard bug report requiring investigation."
                })
            elif "route" in prompt.lower():
                return json.dumps({
                    "team": "Backend",
                    "reasoning": "Keyword analysis suggests backend issue."
                })
            elif "sentiment" in prompt.lower():
                return json.dumps({
                    "sentiment": "negative",
                    "score": 0.3,
                    "summary": "User seems frustrated with the crash."
                })
            elif "suggest" in prompt.lower():
                return json.dumps({
                    "suggested_files": ["src/auth/login.py", "src/api/routes.py"],
                    "potential_cause": "Null pointer exception in login handler.",
                    "fix_strategy": "Add null check for user credentials."
                })
            return "{}"

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "{}"

    def analyze_issue(self, issue: Dict):
        """
        Performs full analysis on an issue: severity, routing, sentiment, duplicates.
        """
        logger.info(f"Analyzing issue {issue['id']}")

        # 1. Detect Duplicates
        duplicates = self.detect_duplicates(issue)

        # 2. Assign Severity & Labels
        severity_resp = self._call_llm(SEVERITY_PROMPT, title=issue['title'], description=issue['description'])
        try:
            severity_data = json.loads(severity_resp)
        except json.JSONDecodeError:
            severity_data = {"severity": "medium", "labels": [], "reasoning": "Failed to parse AI response"}

        # 3. Route to Team
        routing_resp = self._call_llm(ROUTING_PROMPT, title=issue['title'], description=issue['description'], teams=", ".join(Config.TEAMS))
        try:
            routing_data = json.loads(routing_resp)
        except json.JSONDecodeError:
            routing_data = {"team": "Unassigned", "reasoning": "Failed to parse AI response"}

        # 4. Sentiment Analysis
        sentiment_resp = self._call_llm(SENTIMENT_PROMPT, title=issue['title'], description=issue['description'])
        try:
            sentiment_data = json.loads(sentiment_resp)
        except json.JSONDecodeError:
            sentiment_data = {"sentiment": "neutral", "score": 0.5, "summary": "Failed to parse AI response"}

        # Update the issue
        updates = {
            "severity": severity_data.get("severity", "medium"),
            "labels": severity_data.get("labels", []),
            "team": routing_data.get("team", "Unassigned"),
            "sentiment": sentiment_data.get("sentiment", "neutral"),
            "analysis": f"AI Analysis:\nSeverity: {severity_data.get('reasoning')}\nRouting: {routing_data.get('reasoning')}\nSentiment: {sentiment_data.get('summary')}\nDuplicates Found: {len(duplicates)}"
        }

        self.issue_tracker.update_issue(issue['id'], updates)
        return updates

    def detect_duplicates(self, new_issue: Dict, threshold=0.6) -> List[Dict]:
        """
        Simple text similarity detection for duplicates.
        """
        duplicates = []
        all_issues = self.issue_tracker.get_all_issues()

        for issue in all_issues:
            if issue['id'] == new_issue['id']:
                continue

            # Combine title and description for comparison
            text1 = f"{new_issue['title']} {new_issue['description']}"
            text2 = f"{issue['title']} {issue['description']}"

            # Simple similarity ratio
            similarity = difflib.SequenceMatcher(None, text1, text2).ratio()

            if similarity >= threshold:
                duplicates.append({
                    "id": issue['id'],
                    "title": issue['title'],
                    "similarity": round(similarity, 2)
                })

        return duplicates

    def check_stale_issues(self, days_threshold=30):
        """
        Identifies and updates stale issues.
        """
        logger.info("Checking for stale issues...")
        stale_date = datetime.now() - timedelta(days=days_threshold)
        count = 0

        for issue in self.issue_tracker.get_all_issues():
            if issue['status'] == Config.STATUS_OPEN:
                created_at = datetime.fromisoformat(issue['created_at'])
                if created_at < stale_date:
                    self.issue_tracker.update_issue(issue['id'], {"labels": issue.get('labels', []) + ["stale"]})
                    count += 1

        return count

    def suggest_fix(self, issue_id: str) -> Dict:
        """
        Generates a fix suggestion for a specific issue.
        """
        issue = self.issue_tracker.get_issue(issue_id)
        if not issue:
            return {"error": "Issue not found"}

        resp = self._call_llm(FIX_SUGGESTION_PROMPT, title=issue['title'], description=issue['description'])
        try:
            return json.loads(resp)
        except json.JSONDecodeError:
            return {
                "suggested_files": [],
                "potential_cause": "AI failed to generate suggestion.",
                "fix_strategy": "Manual investigation required."
            }
