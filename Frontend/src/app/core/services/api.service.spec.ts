import { TestBed } from '@angular/core/testing';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

import { ApiService } from './api.service';
import {
  AnalysisResponse,
  HealthCheckResponse,
  WorkoutSession,
} from '../models/api.models';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  const API_BASE = 'http://localhost:8000/api/v1';

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        ApiService,
      ],
    });

    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  // ── healthCheck ──────────────────────────────────────────────────────────

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should GET /health and return HealthCheckResponse', () => {
    const mockResponse: HealthCheckResponse = {
      status: 'healthy',
      service: 'kinetic-prism',
    };

    service.healthCheck().subscribe((response) => {
      expect(response).toEqual(mockResponse);
      expect(response.status).toBe('healthy');
    });

    const req = httpMock.expectOne(`${API_BASE}/health`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should handle network errors on healthCheck', () => {
    service.healthCheck().subscribe({
      next: () => fail('Expected an error'),
      error: (err: Error) => {
        expect(err.message).toContain('Network error');
      },
    });

    const req = httpMock.expectOne(`${API_BASE}/health`);
    req.error(new ProgressEvent('error'), { status: 0, statusText: 'Unknown' });
  });

  // ── analyzeSession ──────────────────────────────────────────────────────

  it('should POST /analyze with a WorkoutSession and return AnalysisResponse', () => {
    const session: WorkoutSession = {
      user_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
      raw_data_url: 'https://storage.example.com/workouts/session_001.mp4',
    };

    const mockResponse: AnalysisResponse = {
      session_id: 'generated-uuid',
      metric: {
        score: 85.5,
        power_level: 'Nova',
        glowing_intensity: 0.85,
      },
      error: null,
    };

    service.analyzeSession(session).subscribe((response) => {
      expect(response.metric).toBeTruthy();
      expect(response.metric!.score).toBe(85.5);
      expect(response.metric!.power_level).toBe('Nova');
      expect(response.error).toBeNull();
    });

    const req = httpMock.expectOne(`${API_BASE}/analyze`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(session);
    req.flush(mockResponse);
  });

  it('should handle server error with detail message on analyzeSession', () => {
    const session: WorkoutSession = {
      user_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
      raw_data_url: 'https://storage.example.com/workouts/bad_session.mp4',
    };

    service.analyzeSession(session).subscribe({
      next: () => fail('Expected an error'),
      error: (err: Error) => {
        expect(err.message).toContain('Server error');
        expect(err.message).toContain('Validation failed');
      },
    });

    const req = httpMock.expectOne(`${API_BASE}/analyze`);
    req.flush(
      { detail: 'Validation failed' },
      { status: 422, statusText: 'Unprocessable Entity' },
    );
  });

  it('should return AnalysisResponse with null metric and error string', () => {
    const session: WorkoutSession = {
      user_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
      raw_data_url: 'https://storage.example.com/workouts/empty.mp4',
    };

    const mockResponse: AnalysisResponse = {
      session_id: 'some-uuid',
      metric: null,
      error: 'Insufficient data to compute core-power metric.',
    };

    service.analyzeSession(session).subscribe((response) => {
      expect(response.metric).toBeNull();
      expect(response.error).toBe('Insufficient data to compute core-power metric.');
    });

    const req = httpMock.expectOne(`${API_BASE}/analyze`);
    req.flush(mockResponse);
  });
});
