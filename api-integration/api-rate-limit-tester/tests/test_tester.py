import pytest
import pytest_asyncio
import pandas as pd
import httpx
from agent.tester import AsyncRateLimitTester, RateLimitTestConfig

@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_run_test_basic(httpx_mock):
    # Setup mock with callback to handle multiple requests
    def success_callback(request):
        return httpx.Response(
            status_code=200,
            headers={"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": "99"}
        )

    # Register enough callbacks
    for _ in range(50):
        httpx_mock.add_callback(success_callback)

    config = RateLimitTestConfig(
        url="https://api.example.com/test",
        method="GET",
        rps=10,
        duration=1,
        burst_size=1
    )

    tester = AsyncRateLimitTester()
    df = await tester.run_test(config)

    assert not df.empty
    # We might have fewer than 10 requests if timing is tight, but should be > 0
    assert len(df) >= 1
    assert "status_code" in df.columns
    # Check that we have 200s. If we ran out of mocks, we get 0.
    assert (df["status_code"] == 200).all()
    assert "headers" in df.columns

    headers = tester.detect_rate_limit_headers()
    assert "x-ratelimit-limit" in headers
    assert headers["x-ratelimit-limit"] == "100"

@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_run_test_throttling(httpx_mock):
    # Setup mock with callback to simulate throttling

    request_count = 0

    def custom_response(request):
        nonlocal request_count
        request_count += 1
        if request_count > 5:
            return httpx.Response(
                status_code=429,
                headers={"Retry-After": "10"}
            )
        return httpx.Response(
            status_code=200,
            headers={"X-RateLimit-Remaining": str(6 - request_count)}
        )

    for _ in range(50):
        httpx_mock.add_callback(custom_response)

    config = RateLimitTestConfig(
        url="https://api.example.com/throttle",
        method="GET",
        rps=20,
        duration=1,
        burst_size=1
    )

    tester = AsyncRateLimitTester()
    df = await tester.run_test(config)

    assert not df.empty
    assert (df["status_code"] == 429).any()

    headers = tester.detect_rate_limit_headers()
    assert "retry-after" in headers
    assert headers["retry-after"] == "10"

@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_burst_logic(httpx_mock):
    for _ in range(100):
        httpx_mock.add_callback(lambda req: httpx.Response(status_code=200))

    config = RateLimitTestConfig(
        url="https://api.example.com/burst",
        method="GET",
        rps=10,
        duration=1,
        burst_size=5
    )

    tester = AsyncRateLimitTester()
    df = await tester.run_test(config)

    # Check if requests were made
    assert len(df) > 0
