import json
from typing import List, Dict, Any

def parse_access_logs(log_lines: List[str], endpoint_path: str = None) -> List[float]:
    """
    Parses JSON access logs and extracts latencies for a specific endpoint path.
    Expected JSON format: {"path": "/v1/users/profile", "latency_ms": 120.5, "status": 200}
    """
    latencies = []
    for line in log_lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            if endpoint_path:
                if endpoint_path not in data.get("path", "") and data.get("path", "") not in endpoint_path:
                    continue
                    
            if "latency_ms" in data:
                latency = float(data["latency_ms"])
                status = int(data.get("status", 200))
                if status >= 500:
                    latencies.append(float('inf'))
                else:
                    latencies.append(latency)
        except (json.JSONDecodeError, ValueError):
            pass
            
    return latencies
