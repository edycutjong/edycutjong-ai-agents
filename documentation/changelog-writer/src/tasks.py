from crewai import Task
from textwrap import dedent

class ChangelogTasks:
    def classify_commits_task(self, agent, commits_str):
        return Task(
            description=dedent(f"""
                Analyze the following git commits and classify them into categories:
                - Features (new functionality)
                - Fixes (bug fixes)
                - Chores (maintenance, dependencies)
                - Documentation (docs changes)
                - Refactor (code structure changes)
                - Other (anything else)

                Commits:
                {commits_str}

                Group them and provide a summary for each group.
            """),
            expected_output="A structured summary of commits grouped by category (Features, Fixes, etc.).",
            agent=agent
        )

    def write_changelog_task(self, agent):
        return Task(
            description=dedent(f"""
                Using the classification from the previous task, write a professional Markdown changelog.
                The changelog should include:
                - A header with the date.
                - A brief "Release Highlights" section if there are major features.
                - Sections for "New Features", "Bug Fixes", "Improvements", "Internal Changes".
                - Bullet points for each change, rewritten to be clear and concise for a general developer audience.

                Do not include raw commit hashes unless necessary for context.
                Focus on the VALUE of the change.
            """),
            expected_output="A complete, well-formatted Markdown changelog string.",
            agent=agent
        )
