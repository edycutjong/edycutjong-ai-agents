import asyncio
import time
import httpx
import pandas as pd
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class RequestResult(BaseModel):
    timestamp: float
    status_code: int
    latency: float
    headers: Dict[str, str]
    error: Optional[str] = None

class RateLimitTestConfig(BaseModel):
    url: str
    method: str = "GET"
    headers: Dict[str, str] = {}
    rps: int = 10
    duration: int = 10
    burst_size: int = 1

class AsyncRateLimitTester:
    def __init__(self):
        self.results: List[RequestResult] = []
        self._running = False

    async def _make_request(self, client: httpx.AsyncClient, url: str, method: str, headers: Dict[str, str]) -> RequestResult:
        start_time = time.time()
        try:
            response = await client.request(method, url, headers=headers)
            latency = time.time() - start_time
            return RequestResult(
                timestamp=start_time,
                status_code=response.status_code,
                latency=latency,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            latency = time.time() - start_time
            return RequestResult(
                timestamp=start_time,
                status_code=0,
                latency=latency,
                headers={},
                error=str(e)
            )
        except Exception as e:
            latency = time.time() - start_time
            return RequestResult(
                timestamp=start_time,
                status_code=0,
                latency=latency,
                headers={},
                error=str(e)
            )

    async def run_test(self, config: RateLimitTestConfig, progress_callback=None) -> pd.DataFrame:
        self.results = []
        self._running = True

        # Disable limits to allow high RPS testing (open loop)
        limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)

        async with httpx.AsyncClient(limits=limits, timeout=30.0) as client:
            tasks = []
            start_test_time = time.time()

            # Calculate interval between bursts
            # requests per burst = config.burst_size
            # bursts per second = config.rps / config.burst_size
            # interval = 1 / bursts per second = config.burst_size / config.rps

            if config.rps <= 0:
                interval = 0
            else:
                interval = float(config.burst_size) / float(config.rps)

            requests_made = 0
            total_requests = config.rps * config.duration

            while time.time() - start_test_time < config.duration and self._running:
                # Burst logic
                burst_start = time.time()
                current_burst_tasks = []

                for _ in range(config.burst_size):
                    if requests_made >= total_requests:
                        break

                    # Create task but don't await it yet
                    task = asyncio.create_task(
                        self._make_request(client, config.url, config.method, config.headers)
                    )
                    tasks.append(task)
                    current_burst_tasks.append(task)
                    requests_made += 1

                if progress_callback:
                    # Update progress
                    progress_callback(min(requests_made / total_requests, 1.0))

                if requests_made >= total_requests:
                    break

                # Sleep to maintain rate
                elapsed = time.time() - burst_start
                sleep_time = max(0, interval - elapsed)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            # Wait for all tasks to complete
            if tasks:
                results = await asyncio.gather(*tasks)
                self.results = list(results)
            else:
                self.results = []

        df = pd.DataFrame([r.model_dump() for r in self.results])
        # Convert timestamp to relative time
        if not df.empty:
            df['relative_time'] = df['timestamp'] - df['timestamp'].min()
        return df

    def stop(self):
        self._running = False

    def detect_rate_limit_headers(self) -> Dict[str, str]:
        """Analyzes results to find common rate limit headers."""
        if not self.results:
            return {}

        # Look at the headers of the first successful or 429 response
        sample_headers = {}
        for res in self.results:
            if res.headers:
                sample_headers = res.headers
                if res.status_code == 429:
                    break # Prioritize headers from a throttled response

        detected = {}
        # Common Rate Limit Headers
        common_keys = [
            'x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset',
            'ratelimit-limit', 'ratelimit-remaining', 'ratelimit-reset',
            'retry-after', 'x-rate-limit-limit', 'x-rate-limit-remaining', 'x-rate-limit-reset'
        ]

        for k, v in sample_headers.items():
            if k.lower() in common_keys:
                detected[k] = v

        return detected
