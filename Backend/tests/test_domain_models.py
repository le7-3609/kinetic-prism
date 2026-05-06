"""Unit tests for domain models.

Validates Pydantic V2 schema behaviour: defaults, constraints, and
serialisation round-trips.
"""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from app.domain.models import AnalysisResponse, CorePowerMetric, WorkoutSession


# ── WorkoutSession ─────────────────────────────────────────────────────────


class TestWorkoutSession:
    """Tests for the WorkoutSession model."""

    def test_valid_session_with_defaults(self) -> None:
        """A session created with only required fields should auto-fill defaults."""
        user_id = uuid4()
        session = WorkoutSession(
            user_id=user_id,
            raw_data_url="https://example.com/data.mp4",
        )
        assert session.user_id == user_id
        assert isinstance(session.id, UUID)
        assert session.timestamp is not None
        assert str(session.raw_data_url) == "https://example.com/data.mp4"

    def test_explicit_id_is_preserved(self) -> None:
        """If a caller supplies an explicit ID it should be kept as-is."""
        explicit_id = uuid4()
        session = WorkoutSession(
            id=explicit_id,
            user_id=uuid4(),
            raw_data_url="https://example.com/data.mp4",
        )
        assert session.id == explicit_id

    def test_invalid_url_rejected(self) -> None:
        """A malformed URL must trigger a validation error."""
        with pytest.raises(ValidationError):
            WorkoutSession(
                user_id=uuid4(),
                raw_data_url="not-a-url",
            )

    def test_missing_user_id_rejected(self) -> None:
        """user_id is required — omitting it must raise."""
        with pytest.raises(ValidationError):
            WorkoutSession(raw_data_url="https://example.com/data.mp4")  # type: ignore[call-arg]

    def test_json_round_trip(self) -> None:
        """Serialising to JSON and back should produce an equivalent model."""
        original = WorkoutSession(
            user_id=uuid4(),
            raw_data_url="https://example.com/data.mp4",
        )
        rebuilt = WorkoutSession.model_validate_json(original.model_dump_json())
        assert rebuilt == original


# ── CorePowerMetric ────────────────────────────────────────────────────────


class TestCorePowerMetric:
    """Tests for the CorePowerMetric model."""

    def test_valid_metric(self) -> None:
        metric = CorePowerMetric(score=85.5, power_level="Blaze", glowing_intensity=0.855)
        assert metric.score == 85.5
        assert metric.power_level == "Blaze"
        assert metric.glowing_intensity == 0.855

    def test_score_lower_bound(self) -> None:
        metric = CorePowerMetric(score=0.0, power_level="Ember", glowing_intensity=0.0)
        assert metric.score == 0.0

    def test_score_upper_bound(self) -> None:
        metric = CorePowerMetric(score=100.0, power_level="Nova", glowing_intensity=1.0)
        assert metric.score == 100.0

    def test_score_below_zero_rejected(self) -> None:
        with pytest.raises(ValidationError):
            CorePowerMetric(score=-1.0, power_level="Ember", glowing_intensity=0.0)

    def test_score_above_100_rejected(self) -> None:
        with pytest.raises(ValidationError):
            CorePowerMetric(score=100.01, power_level="Nova", glowing_intensity=1.0)

    def test_glowing_intensity_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            CorePowerMetric(score=50.0, power_level="Flame", glowing_intensity=1.5)


# ── AnalysisResponse ───────────────────────────────────────────────────────


class TestAnalysisResponse:
    """Tests for the AnalysisResponse envelope."""

    def test_success_response(self) -> None:
        session_id = uuid4()
        metric = CorePowerMetric(score=72.0, power_level="Blaze", glowing_intensity=0.72)
        resp = AnalysisResponse(session_id=session_id, metric=metric)
        assert resp.metric is not None
        assert resp.error is None

    def test_error_response(self) -> None:
        session_id = uuid4()
        resp = AnalysisResponse(
            session_id=session_id,
            metric=None,
            error="Insufficient data.",
        )
        assert resp.metric is None
        assert resp.error == "Insufficient data."
