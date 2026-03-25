import os
import argparse
from dotenv import load_dotenv
from agent.core import A11yFixer
from agent.utils import generate_audit_report

def main():
    parser = argparse.ArgumentParser(description="A11y Fixer Agent")
    parser.add_argument("file", help="Path to the HTML file to scan.")
    parser.add_argument("--out", default="a11y_report.html", help="Output report filename.")
    parser.add_argument("--fix", action="store_true", help="Apply fixes directly to a new HTML file.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment. LLM fix generation may fail.")

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        return

    with open(args.file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"Scanning {args.file} for accessibility issues...")
    fixer = A11yFixer(api_key=api_key) if api_key else A11yFixer(api_key="DUMMY")
    
    # In a fully LLM-integrated run, we'd use fixer.analyze_element for complex fixes,
    # but here we use the basic static analyzer to generate the report.
    result = fixer.scan_html(html_content)
    issues = result["issues"]

    report_path = generate_audit_report(issues, args.out)
    print(f"Audit complete: found {len(issues)} issues.")
    print(f"Report saved to {report_path}")

    if args.fix:
        patched_file = args.file.replace('.html', '_fixed.html')
        with open(patched_file, 'w', encoding='utf-8') as f:
            f.write(result.get("fixed_document", html_content))
        print(f"Patched HTML saved to {patched_file}")

if __name__ == "__main__":  # pragma: no cover
    main()
