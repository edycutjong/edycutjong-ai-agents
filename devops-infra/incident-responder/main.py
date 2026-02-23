import time
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from agent.monitor import LogMonitor
from agent.analyzer import LogAnalyzer
from agent.reporter import ReportGenerator
from agent.tools import send_slack_alert, trigger_pagerduty_incident
from config import OPENAI_API_KEY, LLM_MODEL

# Configure Rich logging
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("rich")

console = Console()

def main():
    console.print("[bold green]Starting Incident Responder Agent...[/bold green]")

    monitor = LogMonitor()
    analyzer = LogAnalyzer(api_key=OPENAI_API_KEY, model_name=LLM_MODEL)
    reporter = ReportGenerator()

    log_buffer = []

    try:
        for log in monitor.stream_logs(interval=0.5):
            log_buffer.append(log)

            # Print log to console
            style = "red" if log['level'] == "ERROR" else "yellow" if log['level'] == "WARNING" else "white"
            console.print(f"[{log['timestamp']}] [{style}]{log['level']}[/{style}] {log['service']}: {log['message']}")

            # Analyze every 10 logs
            if len(log_buffer) >= 10:
                console.print("\n[bold blue]Analyzing log batch...[/bold blue]")
                analysis = analyzer.analyze_logs(log_buffer)

                severity = analysis.get("severity", "UNKNOWN")
                console.print(f"Severity: [bold]{severity}[/bold]")

                if severity in ["HIGH", "CRITICAL"]:
                    console.print("[bold red]CRITICAL INCIDENT DETECTED![/bold red]")
                    console.print(f"Root Cause: {analysis.get('root_cause')}")

                    # Alerting
                    send_slack_alert(f"CRITICAL INCIDENT: {analysis.get('summary')}")
                    trigger_pagerduty_incident(analysis.get('summary'), severity)

                    # Reporting
                    report_content = reporter.generate_markdown(analysis)
                    filename = f"incident_report_{int(time.time())}.md"
                    reporter.save_markdown(filename, report_content)
                    console.print(f"[green]Report saved to {filename}[/green]")

                log_buffer = [] # Clear buffer

    except KeyboardInterrupt:
        console.print("[bold red]Stopping agent...[/bold red]")

if __name__ == "__main__":
    main()
