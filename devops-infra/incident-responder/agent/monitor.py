import time  # pragma: no cover
import random  # pragma: no cover
import datetime  # pragma: no cover
import logging  # pragma: no cover
from typing import Generator, Dict, Any  # pragma: no cover

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover

class LogMonitor:  # pragma: no cover
    def __init__(self):  # pragma: no cover
        self.services = ["auth-service", "payment-service", "order-service", "inventory-service"]  # pragma: no cover
        self.error_types = [  # pragma: no cover
            "ConnectionRefusedError: Database connection failed",
            "TimeoutError: Request to payment gateway timed out",
            "ValueError: Invalid user input",
            "OutOfMemoryError: Java heap space",
            "500 Internal Server Error"
        ]
        self.log_levels = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]  # pragma: no cover

    def generate_log_entry(self) -> Dict[str, Any]:  # pragma: no cover
        """Generates a single simulated log entry."""
        service = random.choice(self.services)  # pragma: no cover
        level = random.choice(self.log_levels)  # pragma: no cover
        timestamp = datetime.datetime.now().isoformat()  # pragma: no cover

        if level == "ERROR":  # pragma: no cover
            message = random.choice(self.error_types)  # pragma: no cover
        elif level == "WARNING":  # pragma: no cover
            message = f"High latency detected in {service}"  # pragma: no cover
        else:
            message = f"Processed request successfully in {service}"  # pragma: no cover

        return {  # pragma: no cover
            "timestamp": timestamp,
            "service": service,
            "level": level,
            "message": message
        }

    def stream_logs(self, interval: float = 1.0) -> Generator[Dict[str, Any], None, None]:  # pragma: no cover
        """Yields log entries indefinitely at a given interval."""
        while True:  # pragma: no cover
            log_entry = self.generate_log_entry()  # pragma: no cover
            # logger.info(f"[{log_entry['level']}] {log_entry['service']}: {log_entry['message']}")
            yield log_entry  # pragma: no cover
            time.sleep(interval)  # pragma: no cover

    def get_log_batch(self, count: int = 10) -> list[Dict[str, Any]]:  # pragma: no cover
        """Returns a batch of simulated logs."""
        return [self.generate_log_entry() for _ in range(count)]  # pragma: no cover
