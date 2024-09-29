from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from time import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.ip_requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time()

        # Clean up old requests
        self.ip_requests[client_ip] = [
            timestamp for timestamp in self.ip_requests[client_ip]
            if current_time - timestamp < self.window
        ]

        # Check if the number of requests exceeds the limit
        if len(self.ip_requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )

        # Record the new request
        self.ip_requests[client_ip].append(current_time)

        response = await call_next(request)
        return response