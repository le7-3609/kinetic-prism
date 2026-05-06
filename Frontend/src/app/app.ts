import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

/**
 * Root shell component — renders the active route via `<router-outlet>`.
 * All visual logic is delegated to feature components.
 */
@Component({
  selector: 'kp-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `<router-outlet />`,
  styles: [
    `
      :host {
        display: block;
        min-height: 100vh;
        background-color: #0b0f19;
      }
    `,
  ],
})
export class App {}
