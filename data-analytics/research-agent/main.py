"""
Research Agent — searches and synthesizes information on a given topic.
Usage: python main.py "topic or question"
"""
import argparse, sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Research Agent] Enter a topic, question, or research brief to get a structured summary with key findings, sources, and recommendations."


def main():
    parser = argparse.ArgumentParser(description="Research a topic and synthesize findings")
    parser.add_argument("topic", nargs="?", help="Topic or research question")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard",
                        help="Research depth (default: standard)")
    args = parser.parse_args()

    if not args.topic:
        print("Research Agent")
        print('Usage: python main.py "benefits of microservices architecture" [--depth deep]')
        sys.exit(0)

    template = f"""# Research Brief: {args.topic}
Depth: {args.depth}

## Key Questions to Answer
1. What is {args.topic}?
2. Why does it matter?
3. What are the main approaches/variants?
4. What are the tradeoffs?
5. What do experts recommend?

## Suggested Sources
- Google Scholar / arXiv (academic papers)
- Official documentation / RFC
- Industry blogs (Martin Fowler, AWS, Netflix tech blog)
- Recent GitHub discussions and issues

## Output Format
Use this structure for your research notes:
- Executive Summary (2-3 sentences)
- Key Findings (5 bullets)
- Comparison Table (if applicable)
- Recommendations
- Further Reading

Run with your preferred AI tool to get the actual research content.
"""
    print(template)

if __name__ == "__main__":
    main()
