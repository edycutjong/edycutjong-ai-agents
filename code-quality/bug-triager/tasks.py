from crewai import Task

class BugTriagerTasks:
    def analyze_issue_task(self, agent, issue_content):
        return Task(
            description=f"""Analyze the following GitHub issue to determine its category, labels, and assignee.

            Issue Content:
            {issue_content}

            Your analysis should cover:
            1. Issue Type (Bug, Feature Request, Question, Documentation, etc.)
            2. Suggested Labels (e.g., 'bug', 'enhancement', 'question', 'documentation', 'frontend', 'backend')
            3. Suggested Assignee (infer based on content, e.g., if it's about UI, suggest a frontend maintainer).

            Return the result in a clear, structured format.""",
            agent=agent,
            expected_output="A structured summary with 'Type', 'Labels', and 'Assignee'."
        )

    def check_duplicate_task(self, agent, issue_content):
        return Task(
            description=f"""Search for potential duplicates of the following issue:

            Issue Content:
            {issue_content}

            Use the search tool to find similar issues.
            Analyze the search results to see if any are truly duplicates.""",
            agent=agent,
            expected_output="A report listing potential duplicate issues with their numbers and titles, or 'No duplicates found'."
        )

    def draft_response_task(self, agent, issue_content, context):
        return Task(
            description=f"""Draft a polite and helpful response to the issue author.

            Use the analysis and duplicate check results provided in the context.

            If a duplicate is found, kindly point it out.
            If it's a valid new issue, acknowledge it and mention the next steps (e.g., "We have labeled this as...").

            Do NOT execute the reply. Just draft the text.""",
            agent=agent,
            context=context, # Pass previous tasks here
            expected_output="A draft comment in Markdown format."
        )
