"""Application entry-point for The Kinetic Prism API.

Creates and configures the FastAPI application instance, registers
routers, and wires up middleware.  Run with:

    uvicorn app.main:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="The Kinetic Prism",
    description=(
        "SDG 3 — Fitness & Health analytics engine.  "
        "Upload workout sessions and receive AI-driven core-power metrics."
    ),
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(router, prefix="/api/v1")
