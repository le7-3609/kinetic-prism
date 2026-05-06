import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CorePowerOrb } from './core-power-orb';

describe('CorePowerOrb', () => {
  let fixture: ComponentFixture<CorePowerOrb>;
  let component: CorePowerOrb;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CorePowerOrb],
    }).compileComponents();

    fixture = TestBed.createComponent(CorePowerOrb);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have default intensity of 0', () => {
    expect(component.intensity()).toBe(0);
  });
});
