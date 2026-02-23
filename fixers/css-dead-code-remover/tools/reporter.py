import os
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def generate_report(
    output_path: str,
    total_rules: int,
    unused_rules: List[Any], # List of CSSRule objects
    media_stats: Dict[str, int],
    savings_kb: float = 0.0
):
    """
    Generates an HTML report.
    """
    try:
        # Calculate stats
        unused_count = len(unused_rules)
        used_count = total_rules - unused_count
        efficiency_score = int((used_count / total_rules * 100)) if total_rules > 0 else 100

        # Prepare data for template
        top_unused = []
        for rule in unused_rules[:10]: # Top 10
            top_unused.append({
                "selector": ", ".join(rule.selectors),
                "source": "main.css" # TODO: Pass source filename if available
            })

        detailed_audit = []
        # Limit detailed audit to 100 items to keep report light
        for rule in unused_rules[:100]:
            detailed_audit.append({
                "selector": ", ".join(rule.selectors),
                "status": "Unused",
                "details": "Not found in scanned files"
            })

        # Setup Jinja2
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('report.html')

        html_content = template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_rules=total_rules,
            unused_count=unused_count,
            efficiency_score=efficiency_score,
            savings_kb=round(savings_kb, 2),
            media_chart_data=media_stats,
            top_unused=top_unused,
            detailed_audit=detailed_audit
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"Report generated at {output_path}")

    except Exception as e:
        logger.error(f"Error generating report: {e}")
