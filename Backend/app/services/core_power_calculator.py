"""Core Power Calculator — the analytical engine of The Kinetic Prism.

This service encapsulates the business logic that transforms a raw
WorkoutSession into a CorePowerMetric.  It is intentionally free of any
I/O or framework dependencies so it can be tested in isolation.
"""

from __future__ import annotations

import hashlib
from typing import Optional

from app.domain.models import CorePowerMetric, WorkoutSession

# ---------------------------------------------------------------------------
# Power-level thresholds (score → label mapping)
# ---------------------------------------------------------------------------
_POWER_LEVELS: list[tuple[float, str]] = [
    (90.0, "Nova"),
    (70.0, "Blaze"),
    (50.0, "Flame"),
    (30.0, "Spark"),
    (0.0, "Ember"),
]


def _derive_power_level(score: float) -> str:
    """Return the categorical power label for a given score."""
    for threshold, label in _POWER_LEVELS:
        if score >= threshold:
            return label
    return "Ember"  # Fallback — should never be reached.


class CorePowerCalculator:
    """Stateless service that computes core-power metrics.

    The calculation is currently a deterministic placeholder that hashes
    the session's raw-data URL to produce a reproducible score.  In a
    production system this would delegate to an ML model or the Gemini
    API via the infrastructure layer.
    """

    def calculate_initial_power(
        self, session: WorkoutSession
    ) -> Optional[CorePowerMetric]:
        """Analyse a workout session and return the core-power metric.

        Args:
            session: The workout session to analyse.

        Returns:
            A ``CorePowerMetric`` on success, or ``None`` if the input
            data is insufficient for analysis.
        """
        raw_url: str = str(session.raw_data_url)

        if not raw_url:
            return None

        # Deterministic score derived from the URL hash.
        digest: bytes = hashlib.sha256(raw_url.encode()).digest()
        score: float = round((int.from_bytes(digest[:4], "big") % 10001) / 100, 2)

        power_level: str = _derive_power_level(score)
        glowing_intensity: float = round(score / 100.0, 4)

        return CorePowerMetric(
            score=score,
            power_level=power_level,
            glowing_intensity=glowing_intensity,
        )
