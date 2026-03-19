import time  # pragma: no cover
import logging  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.logging import RichHandler  # pragma: no cover
from rich.table import Table  # pragma: no cover

from agent.monitor import LogMonitor  # pragma: no cover
from agent.analyzer import LogAnalyzer  # pragma: no cover
from agent.reporter import ReportGenerator  # pragma: no cover
from agent.tools import send_slack_alert, trigger_pagerduty_incident  # pragma: no cover
from config import OPENAI_API_KEY, LLM_MODEL  # pragma: no cover

# Configure Rich logging
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])  # pragma: no cover
logger = logging.getLogger("rich")  # pragma: no cover

console = Console()  # pragma: no cover

def main():  # pragma: no cover
    console.print("[bold green]Starting Incident Responder Agent...[/bold green]")  # pragma: no cover

    monitor = LogMonitor()  # pragma: no cover
    analyzer = LogAnalyzer(api_key=OPENAI_API_KEY, model_name=LLM_MODEL)  # pragma: no cover
    reporter = ReportGenerator()  # pragma: no cover

    log_buffer = []  # pragma: no cover

    try:  # pragma: no cover
        for log in monitor.stream_logs(interval=0.5):  # pragma: no cover
            log_buffer.append(log)  # pragma: no cover

            # Print log to console
            style = "red" if log['level'] == "ERROR" else "yellow" if log['level'] == "WARNING" else "white"  # pragma: no cover
            console.print(f"[{log['timestamp']}] [{style}]{log['level']}[/{style}] {log['service']}: {log['message']}")  # pragma: no cover

            # Analyze every 10 logs
            if len(log_buffer) >= 10:  # pragma: no cover
                console.print("\n[bold blue]Analyzing log batch...[/bold blue]")  # pragma: no cover
                analysis = analyzer.analyze_logs(log_buffer)  # pragma: no cover

                severity = analysis.get("severity", "UNKNOWN")  # pragma: no cover
                console.print(f"Severity: [bold]{severity}[/bold]")  # pragma: no cover

                if severity in ["HIGH", "CRITICAL"]:  # pragma: no cover
                    console.print("[bold red]CRITICAL INCIDENT DETECTED![/bold red]")  # pragma: no cover
                    console.print(f"Root Cause: {analysis.get('root_cause')}")  # pragma: no cover

                    # Alerting
                    send_slack_alert(f"CRITICAL INCIDENT: {analysis.get('summary')}")  # pragma: no cover
                    trigger_pagerduty_incident(analysis.get('summary'), severity)  # pragma: no cover

                    # Reporting
                    report_content = reporter.generate_markdown(analysis)  # pragma: no cover
                    filename = f"incident_report_{int(time.time())}.md"  # pragma: no cover
                    reporter.save_markdown(filename, report_content)  # pragma: no cover
                    console.print(f"[green]Report saved to {filename}[/green]")  # pragma: no cover

                log_buffer = [] # Clear buffer  # pragma: no cover

    except KeyboardInterrupt:  # pragma: no cover
        console.print("[bold red]Stopping agent...[/bold red]")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
