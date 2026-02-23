import time
import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from colorama import init, Fore, Style

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import MONITOR_ENDPOINTS, MONITOR_INTERVAL
from agent.monitor import check_endpoint, check_ssl_expiry
from agent.storage import add_result
from agent.analysis import analyze_failure
from agent.alert import send_alert

# Initialize colorama
init()

def monitor_job():
    print(f"\n{Fore.CYAN}--- Starting Monitoring Cycle ---{Style.RESET_ALL}")

    endpoints = [e.strip() for e in MONITOR_ENDPOINTS if e.strip()]
    if not endpoints:
        print(f"{Fore.YELLOW}No endpoints configured to monitor.{Style.RESET_ALL}")
        return

    for url in endpoints:
        print(f"Checking {url}...", end=" ", flush=True)

        # Check HTTP
        status_code, response_time, error = check_endpoint(url)

        # Check SSL
        ssl_days, ssl_error = check_ssl_expiry(url)

        # Log to DB
        # We need to decide what to store as error_message.
        # If HTTP fails, use that error. If SSL fails, append?

        final_error = error
        if ssl_error:
            if final_error:
                final_error += f" | SSL Error: {ssl_error}"
            else:
                final_error = f"SSL Error: {ssl_error}"

        # Determine status
        is_down = status_code == 0 or (status_code >= 400)
        is_ssl_warning = ssl_days is not None and ssl_days < 30

        ai_diagnosis = None

        if is_down:
            print(f"{Fore.RED}DOWN{Style.RESET_ALL} ({status_code}) - {response_time:.2f}s")
            # Analyze failure
            print(f"  {Fore.YELLOW}Analyzing failure...{Style.RESET_ALL}")
            ai_diagnosis = analyze_failure(url, status_code, response_time, final_error)
            print(f"  Diagnosis: {ai_diagnosis[:100]}...")

            # Send Alert
            print(f"  {Fore.MAGENTA}Sending alert...{Style.RESET_ALL}")
            send_alert(url, final_error, ai_diagnosis)

        elif is_ssl_warning:
             print(f"{Fore.YELLOW}SSL WARNING{Style.RESET_ALL} (Expires in {ssl_days} days)")
             # Maybe alert on SSL warning too?
             # For now, let's just log it. The instructions say "Detect SSL certificate expiry".
             # Alerting on SSL expiry is good practice.
             ssl_msg = f"SSL Certificate expires in {ssl_days} days."
             send_alert(url, ssl_msg, "Renew certificate.")
        else:
            print(f"{Fore.GREEN}UP{Style.RESET_ALL} ({status_code}) - {response_time:.2f}s")

        # Save to DB
        add_result(
            endpoint=url,
            status_code=status_code,
            response_time=response_time,
            error_message=final_error,
            ssl_expiry_days=ssl_days,
            ai_diagnosis=ai_diagnosis
        )

def main():
    print(f"{Fore.GREEN}Uptime Monitor Agent Started{Style.RESET_ALL}")
    print(f"Monitoring {len(MONITOR_ENDPOINTS)} endpoints every {MONITOR_INTERVAL} seconds.")

    scheduler = BlockingScheduler()
    scheduler.add_job(monitor_job, 'interval', seconds=MONITOR_INTERVAL)

    try:
        # Run once immediately
        monitor_job()
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print(f"\n{Fore.RED}Stopping monitor...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
