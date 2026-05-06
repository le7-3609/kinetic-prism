"""Core domain models for The Kinetic Prism.

All models are pure Pydantic V2 schemas with no side-effects.
They represent the fundamental data structures that flow through every
layer of the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class WorkoutSession(BaseModel):
    """A single workout recording submitted by the user for analysis.

    Attributes:
        id: Unique identifier for the session (auto-generated if omitted).
        user_id: Identifier of the user who owns this session.
        timestamp: UTC moment the workout was recorded.
        raw_data_url: URL pointing to the raw sensor / video data.
    """

    id: UUID = Field(default_factory=uuid4, description="Unique session identifier.")
    user_id: UUID = Field(..., description="Owner of this workout session.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of the workout recording.",
    )
    raw_data_url: HttpUrl = Field(
        ..., description="URL pointing to the raw workout data asset."
    )

    model_config = {"json_schema_extra": {
        "examples": [
            {
                "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "raw_data_url": "https://storage.example.com/workouts/session_001.mp4",
            }
        ]
    }}


class CorePowerMetric(BaseModel):
    """Result of the AI-driven core-power analysis.

    Produced by the CorePowerCalculator service after processing a
    WorkoutSession.  Every field is deterministic for a given input so
    that results are reproducible across runs.

    Attributes:
        score: Numerical fitness score in the range [0.0, 100.0].
        power_level: Categorical label derived from the score.
        glowing_intensity: Visual intensity value (0.0–1.0) that drives
            the frontend "prism glow" animation.
    """

    score: float = Field(
        ..., ge=0.0, le=100.0, description="Fitness score (0–100)."
    )
    power_level: str = Field(
        ..., description="Categorical power label, e.g. 'Nova', 'Blaze', 'Spark'."
    )
    glowing_intensity: float = Field(
        ..., ge=0.0, le=1.0, description="Prism glow intensity (0.0–1.0)."
    )


class AnalysisResponse(BaseModel):
    """Envelope returned by the /analyze endpoint.

    Wraps the computed metric together with the originating session id
    so the client can correlate results.
    """

    session_id: UUID = Field(..., description="ID of the analysed workout session.")
    metric: Optional[CorePowerMetric] = Field(
        None, description="Computed metric, or None if analysis could not complete."
    )
    error: Optional[str] = Field(
        None, description="Human-readable error message when metric is None."
    )
