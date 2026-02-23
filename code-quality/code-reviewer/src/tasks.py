from crewai import Task
from textwrap import dedent

class CodeReviewerTasks:
    def code_review_task(self, agent, diff):
        return Task(
            description=dedent(f"""\
                Review the following code diff for potential bugs, logical errors, and code quality issues.
                Focus on:
                - Logical correctness
                - Error handling
                - Performance implications
                - Maintainability
                - Best practices

                Code Diff:
                {diff}
                """),
            agent=agent,
            expected_output="A detailed list of findings with specific line references and suggestions for improvement."
        )

    def style_check_task(self, agent, diff):
        return Task(
            description=dedent(f"""\
                Review the following code diff for adherence to standard style guides and formatting rules.
                Focus on:
                - Indentation and spacing
                - Naming conventions
                - Code organization
                - Consistency with common patterns

                Code Diff:
                {diff}
                """),
            agent=agent,
            expected_output="A list of style violations and formatting suggestions."
        )

    def security_audit_task(self, agent, diff):
        return Task(
            description=dedent(f"""\
                Analyze the following code diff for potential security vulnerabilities.
                Focus on:
                - Input validation and sanitization
                - Authentication and authorization checks
                - Secrets exposure
                - Dependency vulnerabilities (if visible)
                - Common security flaws (OWASP Top 10)

                Code Diff:
                {diff}
                """),
            agent=agent,
            expected_output="A security report highlighting any potential risks or confirming no obvious vulnerabilities were found."
        )

    def generate_report_task(self, agent, context):
        return Task(
            description=dedent(f"""\
                Synthesize the findings from the Code Review, Style Check, and Security Audit tasks.
                Structure the report clearly with the following sections:
                1. Executive Summary: Brief overview of the changes.
                2. Code Quality Analysis: Key findings from the code review.
                3. Style Check: Formatting and adherence to standards.
                4. Security Audit: Potential vulnerabilities and risks.
                5. Recommendations: Consolidated list of action items.

                Ensure the report is concise, professional, and formatted in Markdown.
                """),
            agent=agent,
            context=context,
            expected_output="A comprehensive Markdown report summarizing all findings."
        )
