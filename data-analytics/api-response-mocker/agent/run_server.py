import uvicorn
import sys
import json
import os
import asyncio
from agent.server import MockServer
from agent.parser import OpenAPIParser

def run(spec_path, port, latency, error_rate, log_file):
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    parser = OpenAPIParser(spec_content)
    config = {
        'latency_ms': latency,
        'error_rate': error_rate
    }

    server = MockServer(parser, config)

    # Background task to write logs
    @server.app.on_event("startup")
    async def startup_event():
        asyncio.create_task(dump_logs(server, log_file))

    async def dump_logs(server, log_path):
        while True:
            await asyncio.sleep(1)
            # Write logs to file safely
            try:
                # Use a temp file and rename to avoid partial writes?
                # For simplicity, just write. JSON dump is atomic enough for small files usually.
                with open(log_path, 'w') as f:
                    json.dump(server.request_log, f)
            except Exception as e:
                print(f"Error writing logs: {e}")

    uvicorn.run(server.app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Args: spec_path, port, latency, error_rate, log_file
    if len(sys.argv) < 6:
        print("Usage: python run_server.py <spec_path> <port> <latency> <error_rate> <log_file>")
        sys.exit(1)

    spec_path = sys.argv[1]
    port = int(sys.argv[2])
    latency = int(sys.argv[3])
    error_rate = float(sys.argv[4])
    log_file = sys.argv[5]

    run(spec_path, port, latency, error_rate, log_file)
