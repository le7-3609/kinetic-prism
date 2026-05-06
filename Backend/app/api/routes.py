"""API routes for The Kinetic Prism.

Defines the HTTP interface consumed by the frontend.  All heavy lifting
is delegated to the service layer — routes only handle request parsing,
response formatting, and HTTP status codes.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.domain.models import AnalysisResponse, CorePowerMetric, WorkoutSession
from app.services.core_power_calculator import CorePowerCalculator

router = APIRouter()

# Instantiate the calculator once (stateless — safe to share).
_calculator = CorePowerCalculator()


@router.get(
    "/health",
    summary="Health Check",
    description="Returns service status. Use for liveness / readiness probes.",
    tags=["ops"],
)
async def health_check() -> dict[str, str]:
    """Return a simple health-check payload."""
    return {"status": "healthy", "service": "kinetic-prism"}


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyse a Workout Session",
    description="Accepts a WorkoutSession and returns the computed CorePowerMetric.",
    tags=["analysis"],
)
async def analyze_session(session: WorkoutSession) -> AnalysisResponse:
    """Run core-power analysis on the supplied workout session.

    If the calculator returns ``None`` the response will carry an error
    message instead of a metric — no exception is raised.
    """
    metric: CorePowerMetric | None = _calculator.calculate_initial_power(session)

    if metric is None:
        return AnalysisResponse(
            session_id=session.id,
            metric=None,
            error="Insufficient data to compute core-power metric.",
        )

    return AnalysisResponse(
        session_id=session.id,
        metric=metric,
    )
