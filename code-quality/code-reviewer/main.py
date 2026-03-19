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

    try:  # pragma: no cover
        # Step 1: Fetch PR Diff
        print_step(f"Fetching PR #{args.pr_number} from {args.repo}...")  # pragma: no cover
        github_client = GitHubClient()  # pragma: no cover
        diff = github_client.get_pr_diff(args.repo, args.pr_number)  # pragma: no cover
        print_success("PR diff fetched successfully.")  # pragma: no cover

        if not diff:  # pragma: no cover
            print_error("The PR diff is empty or could not be retrieved.")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        # Step 2: Initialize Agents and Tasks
        print_step("Initializing AI Agents...")  # pragma: no cover
        agents = CodeReviewerAgents()  # pragma: no cover
        tasks = CodeReviewerTasks()  # pragma: no cover

        reviewer_agent = agents.code_reviewer_agent()  # pragma: no cover
        style_agent = agents.style_checker_agent()  # pragma: no cover
        security_agent = agents.security_analyst_agent()  # pragma: no cover
        report_agent = agents.report_generator_agent()  # pragma: no cover

        review_task = tasks.code_review_task(reviewer_agent, diff)  # pragma: no cover
        style_task = tasks.style_check_task(style_agent, diff)  # pragma: no cover
        security_task = tasks.security_audit_task(security_agent, diff)  # pragma: no cover

        # The final task depends on the output of the previous three
        final_report_task = tasks.generate_report_task(  # pragma: no cover
            report_agent,
            context=[review_task, style_task, security_task]
        )

        # Step 3: Run Crew
        print_step("Starting Code Review Process...")  # pragma: no cover
        crew = Crew(  # pragma: no cover
            agents=[reviewer_agent, style_agent, security_agent, report_agent],
            tasks=[review_task, style_task, security_task, final_report_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()  # pragma: no cover

        # Step 4: Display Results
        print_header("Review Results")  # pragma: no cover
        # CrewAI returns 'CrewOutput' object in newer versions, check if result is string or object
        if hasattr(result, 'raw'):  # pragma: no cover
             markdown_content = result.raw  # pragma: no cover
        else:
             markdown_content = str(result)  # pragma: no cover

        console.print(Markdown(markdown_content))  # pragma: no cover

        # Step 5: Post Comment
        if args.post_comment:  # pragma: no cover
            print_step("Posting review to GitHub...")  # pragma: no cover
            comment_body = f"## AI Code Review Summary\n\n{markdown_content}"  # pragma: no cover
            github_client.post_comment(args.repo, args.pr_number, comment_body)  # pragma: no cover
            print_success("Review posted successfully.")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        print_error(f"An error occurred: {e}")  # pragma: no cover
        logger.exception("Detailed traceback:")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

if __name__ == "__main__":
    main()
