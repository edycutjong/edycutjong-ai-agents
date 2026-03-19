import click
import yaml
import sys
import os
from typing import List

from lib.git_analyzer import get_changed_files, get_author_email
from lib.scorer import calculate_total_risk
from lib.reporter import format_terminal, format_json, format_markdown

@click.command()
@click.option("--repo", default=".", help="Path to git repository")
@click.option("--sha", default="HEAD", help="Commit SHA to analyze")
@click.option("--config", default="config.yaml", help="Path to config YAML")
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json", "markdown"]))
@click.option("--threshold", default=75, type=int, help="Threshold score to fail CI")
def main(repo, sha, config, output_format, threshold):
    """Commit Risk Scorer"""
    config_data = {}
    if os.path.exists(config):
        with open(config, "r") as f:
            config_data = yaml.safe_load(f) or {}
            
    # Override threshold if passed explicitly, else use config, else default
    cfg_threshold = config_data.get("thresholds", {}).get("fail_ci_score", threshold)
    threshold = int(cfg_threshold)
            
    files = get_changed_files(repo, sha)
    author = get_author_email(repo, sha)
    
    score_data = calculate_total_risk(files, author, repo, config_data)
    
    if output_format == "table":
        format_terminal(score_data, files)
    elif output_format == "json":
        click.echo(format_json(score_data))
    elif output_format == "markdown":
        click.echo(format_markdown(score_data, files))
        
    if score_data["score"] >= threshold:
        sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    main()
