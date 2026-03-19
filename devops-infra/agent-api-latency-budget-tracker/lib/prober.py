import httpx
import time
from typing import Dict, Any, Tuple

async def probe_endpoint(endpoint: Dict[str, Any]) -> Tuple[bool, float]:
    """
    Probes an endpoint and returns (success_boolean, latency_ms)
    """
    url = endpoint.get("url")
    method = endpoint.get("method", "GET")
    
    start_time = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.request(method, url)
            response.raise_for_status()
            success = True
    except Exception:
        success = False
        
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000.0
    
    if not success:
        latency_ms = float('inf')
        
    return success, latency_ms
