"""Stub Gemini API client for future AI integration.

This module provides a placeholder interface for communicating with
Google's Gemini API.  The implementation returns mock responses so the
rest of the application can develop against a stable contract.
"""

from __future__ import annotations

from typing import Any, Optional


class GeminiClient:
    """Mock client for the Gemini generative-AI API.

    All methods return deterministic stub data.  Replace the bodies with
    real HTTP calls (via ``httpx``) when the API key is available.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._api_key: Optional[str] = api_key

    async def analyze_workout(self, data_url: str) -> Optional[dict[str, Any]]:
        """Send workout data to Gemini for analysis.

        Args:
            data_url: Public URL of the raw workout asset.

        Returns:
            A dictionary with analysis results, or ``None`` on failure.
        """
        # Stub implementation — always succeeds.
        return {
            "summary": "Workout analysis completed (stub).",
            "confidence": 0.95,
            "data_url": data_url,
        }
