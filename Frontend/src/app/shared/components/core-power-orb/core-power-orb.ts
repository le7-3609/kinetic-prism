import { Component, computed, input } from '@angular/core';

/**
 * CorePowerOrb — The signature visual of The Kinetic Prism.
 *
 * Renders a square container (sharp edges enforced globally) with a
 * glowing purple sphere whose intensity is driven by a reactive
 * `intensity` input signal (0.0 – 1.0).
 *
 * Usage:
 *   <kp-core-power-orb [intensity]="glowSignal()" />
 */
@Component({
  selector: 'kp-core-power-orb',
  standalone: true,
  template: `
    <div class="orb-container">
      <div class="orb-track">
        <!-- Ambient pulse ring -->
        <div class="orb-pulse" [style]="pulseStyle()"></div>
        <!-- Main sphere -->
        <div class="orb-sphere" [style]="sphereStyle()">
          <div class="orb-core"></div>
        </div>
      </div>
      <span class="orb-label font-mono text-xs tracking-widest text-kp-text-muted uppercase mt-4">
        Core Power
      </span>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }

    .orb-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 280px;
      height: 280px;
      background: linear-gradient(135deg, #111827 0%, #0b0f19 100%);
      border: 1px solid rgba(129, 57, 235, 0.15);
      position: relative;
      overflow: hidden;
    }

    .orb-track {
      position: relative;
      width: 160px;
      height: 160px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .orb-pulse {
      position: absolute;
      inset: -20px;
      border-radius: 50% !important;
      animation: pulse-glow 3s ease-in-out infinite;
      pointer-events: none;
    }

    .orb-sphere {
      width: 120px;
      height: 120px;
      border-radius: 50% !important;
      background: radial-gradient(
        circle at 35% 35%,
        #a855f7 0%,
        #8139eb 40%,
        #5b21b6 80%,
        #3b0d7e 100%
      );
      position: relative;
      z-index: 1;
      transition: box-shadow 0.6s ease, transform 0.6s ease;
    }

    .orb-core {
      position: absolute;
      top: 18%;
      left: 22%;
      width: 32%;
      height: 32%;
      border-radius: 50% !important;
      background: radial-gradient(
        circle,
        rgba(255, 255, 255, 0.45) 0%,
        rgba(168, 85, 247, 0.2) 60%,
        transparent 100%
      );
      filter: blur(4px);
    }

    .orb-label {
      z-index: 1;
    }

    @keyframes pulse-glow {
      0%, 100% {
        box-shadow:
          0 0 12px rgba(129, 57, 235, 0.3),
          0 0 36px rgba(129, 57, 235, 0.15);
      }
      50% {
        box-shadow:
          0 0 24px rgba(129, 57, 235, 0.6),
          0 0 60px rgba(129, 57, 235, 0.35),
          0 0 100px rgba(129, 57, 235, 0.15);
      }
    }
  `],
})
export class CorePowerOrb {
  /** Glow intensity (0.0 – 1.0). Drives sphere shadow and scale. */
  readonly intensity = input<number>(0);

  /** Computed inline style for the sphere — maps intensity to visual weight. */
  protected readonly sphereStyle = computed(() => {
    const i = Math.max(0, Math.min(1, this.intensity()));
    const blur1 = 12 + i * 30;
    const blur2 = 24 + i * 60;
    const blur3 = 48 + i * 100;
    const alpha1 = 0.3 + i * 0.5;
    const alpha2 = 0.15 + i * 0.35;
    const alpha3 = 0.05 + i * 0.2;
    const scale = 1 + i * 0.12;

    return {
      'box-shadow': `
        0 0 ${blur1}px rgba(129, 57, 235, ${alpha1}),
        0 0 ${blur2}px rgba(129, 57, 235, ${alpha2}),
        0 0 ${blur3}px rgba(129, 57, 235, ${alpha3})
      `,
      transform: `scale(${scale})`,
    };
  });

  /** Computed inline style for the ambient pulse ring. */
  protected readonly pulseStyle = computed(() => {
    const i = Math.max(0, Math.min(1, this.intensity()));
    const opacity = 0.3 + i * 0.7;
    return { opacity: `${opacity}` };
  });
}
