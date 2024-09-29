from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import component, healthcheck, resize, resize_multiple, webp, webp_multiple
from app.middleware.ratelimit import RateLimitMiddleware
import os

app = FastAPI()

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add CORS middleware for localhost:5173, localhost:8000, localhost:8080, and localhost:8081
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://web-size.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


app.include_router(healthcheck.router)
app.include_router(resize.router)
app.include_router(resize_multiple.router)
app.include_router(webp.router)
app.include_router(webp_multiple.router)
app.include_router(component.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)