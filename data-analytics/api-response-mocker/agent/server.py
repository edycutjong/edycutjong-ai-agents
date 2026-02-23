from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio
import random
from typing import Dict, Any, List
import time
from agent.parser import OpenAPIParser
from agent.data_generator import DataGenerator

class MockServer:
    def __init__(self, parser: OpenAPIParser, config: Dict[str, Any] = None):
        self.parser = parser
        self.app = FastAPI(title=parser.specification.get('info', {}).get('title', 'Mock API'))
        self.config = config or {}
        self.generator = DataGenerator()
        self.request_log = []

        # Configuration
        self.latency_ms = self.config.get('latency_ms', 0)
        self.error_rate = self.config.get('error_rate', 0.0) # 0.0 to 1.0

        self._register_routes()
        self._register_middleware()

    def update_config(self, config: Dict[str, Any]):
        """Update runtime configuration."""
        self.config.update(config)
        self.latency_ms = self.config.get('latency_ms', self.latency_ms)
        self.error_rate = self.config.get('error_rate', self.error_rate)

    def _register_middleware(self):
        @self.app.middleware("http")
        async def simulate_conditions(request: Request, call_next):
            # Record Request
            start_time = time.time()

            # Simulate Latency
            if self.latency_ms > 0:
                await asyncio.sleep(self.latency_ms / 1000.0)

            # Simulate Error
            if self.error_rate > 0 and random.random() < self.error_rate:
                # Log error request
                self.request_log.append({
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "duration_ms": (time.time() - start_time) * 1000,
                    "timestamp": time.time(),
                    "error": "Simulated error"
                })
                return JSONResponse(
                    status_code=random.choice([400, 401, 403, 404, 500, 503]),
                    content={"error": "Simulated error"}
                )

            response = await call_next(request)

            # Log
            duration = (time.time() - start_time) * 1000
            self.request_log.append({
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration,
                "timestamp": time.time()
            })

            return response

    def _register_routes(self):
        paths = self.parser.get_paths()
        for path in paths:
            methods = self.parser.get_methods_for_path(path)
            for method in methods:
                self._add_route(path, method)

    def _create_endpoint_handler(self, path: str, method: str):
        async def handler(request: Request):
            schema = self.parser.get_response_schema(path, method)
            if not schema:
                # If no schema, try to return generic success
                return JSONResponse(content={"message": "Success (no schema defined)"}, status_code=200)

            data = self.generator.generate_from_schema(schema)
            return JSONResponse(content=data)
        return handler

    def _add_route(self, path: str, method: str):
        handler = self._create_endpoint_handler(path, method)
        self.app.add_api_route(
            path,
            handler,
            methods=[method],
            summary=f"Mock for {method} {path}"
        )
