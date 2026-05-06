"""In-memory mock database for development and testing.

Provides a simple dictionary-backed store so higher layers can persist
and retrieve domain entities without a real database dependency.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from app.domain.models import WorkoutSession


class MockSessionStore:
    """Thread-unsafe, in-memory store for WorkoutSession objects.

    Suitable only for local development and unit tests.
    """

    def __init__(self) -> None:
        self._sessions: dict[UUID, WorkoutSession] = {}

    def save(self, session: WorkoutSession) -> WorkoutSession:
        """Persist a session and return it."""
        self._sessions[session.id] = session
        return session

    def get(self, session_id: UUID) -> Optional[WorkoutSession]:
        """Retrieve a session by ID, or ``None`` if not found."""
        return self._sessions.get(session_id)

    def list_all(self) -> list[WorkoutSession]:
        """Return every stored session (order not guaranteed)."""
        return list(self._sessions.values())

    def delete(self, session_id: UUID) -> bool:
        """Remove a session. Returns ``True`` if it existed."""
        return self._sessions.pop(session_id, None) is not None
