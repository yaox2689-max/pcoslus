"""PCOS Runtime v0.1

FastAPI application for the Personal Cognitive Operating System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import decide
from .routers.dashboard import router as dashboard_router
from .config import get_config


app = FastAPI(
    title="PCOS Runtime",
    description="Personal Cognitive Operating System - Decision Engine",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(decide.router)
app.include_router(dashboard_router)


@app.on_event("startup")
async def startup_event():
    """Load configurations at startup."""
    config = get_config()
    import os
    provider = os.getenv("LLM_PROVIDER", "deepseek")
    print(f"PCOS Runtime v0.1 started")
    print(f"  LLM Provider: {provider}")
    print(f"  Identity values: {config.get_identity_values()}")
    print(f"  World model beliefs: {len(config.get_world_model_beliefs())}")


@app.get("/")
async def root():
    """Root endpoint - redirect to dashboard."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")


@app.get("/health")
async def health():
    """Health check endpoint."""
    config = get_config()
    return {
        "status": "healthy",
        "identity_loaded": bool(config.identity),
        "world_model_loaded": bool(config.world_model),
        "strategy_engine_loaded": bool(config.strategy_engine),
        "decision_engine_loaded": bool(config.decision_engine),
    }
