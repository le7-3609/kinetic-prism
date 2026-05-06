import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import {
  AnalysisResponse,
  HealthCheckResponse,
  WorkoutSession,
} from '../models/api.models';

/**
 * Central HTTP gateway to The Kinetic Prism backend.
 *
 * All calls target the FastAPI server running on `http://localhost:8000/api/v1`.
 * Error handling normalises HTTP failures into user-friendly messages
 * so consuming components never need to parse raw `HttpErrorResponse`.
 */
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = 'http://localhost:8000/api/v1';

  constructor(private readonly http: HttpClient) {}

  /** GET /health — lightweight liveness probe. */
  healthCheck(): Observable<HealthCheckResponse> {
    return this.http
      .get<HealthCheckResponse>(`${this.baseUrl}/health`)
      .pipe(catchError(this.handleError));
  }

  /** POST /analyze — submit a workout session for core-power analysis. */
  analyzeSession(session: WorkoutSession): Observable<AnalysisResponse> {
    return this.http
      .post<AnalysisResponse>(`${this.baseUrl}/analyze`, session)
      .pipe(catchError(this.handleError));
  }

  /**
   * Centralised error handler.
   * Extracts a human-readable message from the raw HTTP response and
   * re-throws as an `Error` so subscribers receive a clean string.
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let message: string;

    if (error.status === 0) {
      message = 'Network error — the backend is unreachable.';
    } else if (error.error && typeof error.error === 'object' && 'detail' in error.error) {
      message = `Server error (${error.status}): ${error.error['detail']}`;
    } else {
      message = `Unexpected error (${error.status}): ${error.statusText}`;
    }

    console.error('[ApiService]', message, error);
    return throwError(() => new Error(message));
  }
}
