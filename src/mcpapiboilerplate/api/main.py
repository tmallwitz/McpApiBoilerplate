from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mcpapiboilerplate.api.routes import health

app = FastAPI(title="McpApiBoilerplate", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


def run() -> None:
    uvicorn.run("mcpapiboilerplate.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
