import click
import yaml
import asyncio
from typing import Dict, Any
import sys
import os

from lib.prober import probe_endpoint
from lib.log_parser import parse_access_logs
from lib.budget import BudgetManager
from lib.alerter import send_alert
from lib.reporter import format_terminal, format_json, format_markdown

async def run_probes(endpoints, iterations: int = 1):
    latencies = {ep["name"]: [] for ep in endpoints}
    for _ in range(iterations):
        for ep in endpoints:
            success, lat = await probe_endpoint(ep)
            latencies[ep["name"]].append(lat)
    return latencies

@click.command()
@click.option("--config", default="config.yaml", help="Path to config YAML")
@click.option("--logs", default=None, help="Path to JSON access logs file")
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json", "markdown"]))
@click.option("--probes", default=10, help="Number of synthetic probes to run if logs not provided")
def main(config, logs, output_format, probes):
    """API Latency Budget Tracker"""
    if not os.path.exists(config):
        click.secho(f"Config file not found: {config}", fg="red")
        sys.exit(1)
        
    with open(config, "r") as f:
        config_data = yaml.safe_load(f)
        
    endpoints = config_data.get("endpoints", [])
    budget_cfg = config_data.get("budget", {})
    total_budget = float(budget_cfg.get("total_error_budget_percentage", 1.0))
    
    alerting_cfg = config_data.get("alerting", {})
    webhook_url = alerting_cfg.get("webhook_url", "")
    
    latencies = {ep["name"]: [] for ep in endpoints}
    
    if logs:
        if not os.path.exists(logs):
            click.secho(f"Log file not found: {logs}", fg="red")
            sys.exit(1)
        with open(logs, "r") as f:
            log_lines = f.readlines()
            
        for ep in endpoints:
            url_path = ep.get("url", "").split("://")[-1].split("/", 1)[-1] if "://" in ep.get("url", "") else ep.get("url", "")
            if not url_path:
                url_path = ep.get("url")
            latencies[ep["name"]] = parse_access_logs(log_lines, endpoint_path=url_path)
    else:
        # Run synthetic probes
        latencies = asyncio.run(run_probes(endpoints, iterations=probes))
        
    budget_mgr = BudgetManager(config_data)
    results = []
    has_exhausted = False
    
    for ep in endpoints:
        name = ep["name"]
        slo_targets = ep.get("slo", {})
        ep_latencies = latencies.get(name, [])
        
        report = budget_mgr.evaluate(ep_latencies, slo_targets, total_budget)
        report["name"] = name
        results.append(report)
        
        if report["is_exhausted"]:
            has_exhausted = True
            
    if output_format == "table":
        format_terminal(results)
    elif output_format == "json":
        click.echo(format_json(results))
    elif output_format == "markdown":
        click.echo(format_markdown(results))
        
    if has_exhausted and webhook_url:
        send_alert(webhook_url, "🚨 API Latency Budget EXHAUSTED for one or more endpoints.")

    if has_exhausted:
        sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    main()
