"""Unit tests for the CorePowerCalculator service.

Verifies deterministic output and edge-case handling without any I/O.
"""

from __future__ import annotations

from uuid import uuid4

from app.domain.models import WorkoutSession
from app.services.core_power_calculator import CorePowerCalculator


class TestCorePowerCalculator:
    """Tests for CorePowerCalculator.calculate_initial_power."""

    def setup_method(self) -> None:
        self.calculator = CorePowerCalculator()

    def test_returns_metric_for_valid_session(self) -> None:
        """A session with a valid URL should produce a non-None metric."""
        session = WorkoutSession(
            user_id=uuid4(),
            raw_data_url="https://example.com/workout.mp4",
        )
        metric = self.calculator.calculate_initial_power(session)
        assert metric is not None
        assert 0.0 <= metric.score <= 100.0
        assert 0.0 <= metric.glowing_intensity <= 1.0
        assert metric.power_level in {"Nova", "Blaze", "Flame", "Spark", "Ember"}

    def test_deterministic_output(self) -> None:
        """The same URL should always yield the same score."""
        session = WorkoutSession(
            user_id=uuid4(),
            raw_data_url="https://example.com/stable.mp4",
        )
        first = self.calculator.calculate_initial_power(session)
        second = self.calculator.calculate_initial_power(session)
        assert first is not None and second is not None
        assert first.score == second.score

    def test_different_urls_produce_different_scores(self) -> None:
        """Two distinct URLs should (almost certainly) produce different scores."""
        s1 = WorkoutSession(user_id=uuid4(), raw_data_url="https://a.com/1.mp4")
        s2 = WorkoutSession(user_id=uuid4(), raw_data_url="https://b.com/2.mp4")
        m1 = self.calculator.calculate_initial_power(s1)
        m2 = self.calculator.calculate_initial_power(s2)
        assert m1 is not None and m2 is not None
        assert m1.score != m2.score
