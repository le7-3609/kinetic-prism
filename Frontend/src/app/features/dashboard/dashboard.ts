import { Component, signal } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common';
import { CorePowerOrb } from '../../shared/components/core-power-orb/core-power-orb';
import { ApiService } from '../../core/services/api.service';
import { AnalysisResponse, CorePowerMetric } from '../../core/models/api.models';

/**
 * Dashboard — primary feature view of The Kinetic Prism.
 *
 * Provides the "Scan Workout" trigger and renders analysis results
 * (Score, Level) alongside the CorePowerOrb visualisation.
 * All reactive state is managed via Angular Signals.
 */
@Component({
  selector: 'kp-dashboard',
  standalone: true,
  imports: [CorePowerOrb, DecimalPipe, PercentPipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard {
  /** Current glow intensity fed to the CorePowerOrb. */
  readonly glowIntensity = signal<number>(0);

  /** Computed metric from the last analysis run. */
  readonly metric = signal<CorePowerMetric | null>(null);

  /** Whether an analysis request is in-flight. */
  readonly isLoading = signal<boolean>(false);

  /** Error message from the last failed request. */
  readonly errorMessage = signal<string | null>(null);

  /** The last full analysis response. */
  readonly lastResponse = signal<AnalysisResponse | null>(null);

  constructor(private readonly api: ApiService) {}

  /** Trigger a workout analysis against the backend /analyze endpoint. */
  scanWorkout(): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    const session = {
      user_id: crypto.randomUUID(),
      raw_data_url: 'https://storage.kineticprism.io/workouts/live_scan.mp4',
    };

    this.api.analyzeSession(session).subscribe({
      next: (response) => {
        this.lastResponse.set(response);

        if (response.metric) {
          this.metric.set(response.metric);
          this.glowIntensity.set(response.metric.glowing_intensity);
        } else {
          this.errorMessage.set(response.error ?? 'Analysis returned no data.');
        }

        this.isLoading.set(false);
      },
      error: (err: Error) => {
        this.errorMessage.set(err.message);
        this.isLoading.set(false);
      },
    });
  }
}
