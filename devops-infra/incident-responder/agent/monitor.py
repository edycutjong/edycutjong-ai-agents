import time
import random
import datetime
import logging
from typing import Generator, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LogMonitor:
    def __init__(self):
        self.services = ["auth-service", "payment-service", "order-service", "inventory-service"]
        self.error_types = [
            "ConnectionRefusedError: Database connection failed",
            "TimeoutError: Request to payment gateway timed out",
            "ValueError: Invalid user input",
            "OutOfMemoryError: Java heap space",
            "500 Internal Server Error"
        ]
        self.log_levels = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]

    def generate_log_entry(self) -> Dict[str, Any]:
        """Generates a single simulated log entry."""
        service = random.choice(self.services)
        level = random.choice(self.log_levels)
        timestamp = datetime.datetime.now().isoformat()

        if level == "ERROR":
            message = random.choice(self.error_types)
        elif level == "WARNING":
            message = f"High latency detected in {service}"
        else:
            message = f"Processed request successfully in {service}"

        return {
            "timestamp": timestamp,
            "service": service,
            "level": level,
            "message": message
        }

    def stream_logs(self, interval: float = 1.0) -> Generator[Dict[str, Any], None, None]:
        """Yields log entries indefinitely at a given interval."""
        while True:
            log_entry = self.generate_log_entry()
            # logger.info(f"[{log_entry['level']}] {log_entry['service']}: {log_entry['message']}")
            yield log_entry
            time.sleep(interval)

    def get_log_batch(self, count: int = 10) -> list[Dict[str, Any]]:
        """Returns a batch of simulated logs."""
        return [self.generate_log_entry() for _ in range(count)]
