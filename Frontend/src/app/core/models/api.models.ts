/**
 * Domain models mirroring the Python backend Pydantic schemas.
 *
 * Every interface here is a 1-to-1 TypeScript representation of the
 * corresponding `app.domain.models` class on the FastAPI server.
 */

/** Payload sent to POST /api/v1/analyze */
export interface WorkoutSession {
  readonly user_id: string;
  readonly raw_data_url: string;
  readonly id?: string;
  readonly timestamp?: string;
}

/** Core Power metric returned by the analysis engine. */
export interface CorePowerMetric {
  readonly score: number;
  readonly power_level: string;
  readonly glowing_intensity: number;
}

/** Envelope returned by the /analyze endpoint. */
export interface AnalysisResponse {
  readonly session_id: string;
  readonly metric: CorePowerMetric | null;
  readonly error: string | null;
}

/** Health-check response from GET /api/v1/health */
export interface HealthCheckResponse {
  readonly status: string;
  readonly service: string;
}
