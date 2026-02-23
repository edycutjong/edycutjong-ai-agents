import argparse
import sys
from crewai import Crew, Process
from src.github_client import GitHubClient
from src.agents import CodeReviewerAgents
from src.tasks import CodeReviewerTasks
from src.utils import logger, print_header, print_step, print_success, print_error, console
from rich.markdown import Markdown

def main():
    print_header("Code Review Agent")

    parser = argparse.ArgumentParser(description="AI-powered Code Reviewer Agent")
    parser.add_argument("repo", help="GitHub repository name (e.g., owner/repo)")
    parser.add_argument("pr_number", type=int, help="Pull Request number")
    parser.add_argument("--post-comment", action="store_true", help="Post the review as a comment on the PR")

    args = parser.parse_args()

    try:
        # Step 1: Fetch PR Diff
        print_step(f"Fetching PR #{args.pr_number} from {args.repo}...")
        github_client = GitHubClient()
        diff = github_client.get_pr_diff(args.repo, args.pr_number)
        print_success("PR diff fetched successfully.")

        if not diff:
            print_error("The PR diff is empty or could not be retrieved.")
            sys.exit(1)

        # Step 2: Initialize Agents and Tasks
        print_step("Initializing AI Agents...")
        agents = CodeReviewerAgents()
        tasks = CodeReviewerTasks()

        reviewer_agent = agents.code_reviewer_agent()
        style_agent = agents.style_checker_agent()
        security_agent = agents.security_analyst_agent()
        report_agent = agents.report_generator_agent()

        review_task = tasks.code_review_task(reviewer_agent, diff)
        style_task = tasks.style_check_task(style_agent, diff)
        security_task = tasks.security_audit_task(security_agent, diff)

        # The final task depends on the output of the previous three
        final_report_task = tasks.generate_report_task(
            report_agent,
            context=[review_task, style_task, security_task]
        )

        # Step 3: Run Crew
        print_step("Starting Code Review Process...")
        crew = Crew(
            agents=[reviewer_agent, style_agent, security_agent, report_agent],
            tasks=[review_task, style_task, security_task, final_report_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()

        # Step 4: Display Results
        print_header("Review Results")
        # CrewAI returns 'CrewOutput' object in newer versions, check if result is string or object
        if hasattr(result, 'raw'):
             markdown_content = result.raw
        else:
             markdown_content = str(result)

        console.print(Markdown(markdown_content))

        # Step 5: Post Comment
        if args.post_comment:
            print_step("Posting review to GitHub...")
            comment_body = f"## AI Code Review Summary\n\n{markdown_content}"
            github_client.post_comment(args.repo, args.pr_number, comment_body)
            print_success("Review posted successfully.")

    except Exception as e:
        print_error(f"An error occurred: {e}")
        logger.exception("Detailed traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()
