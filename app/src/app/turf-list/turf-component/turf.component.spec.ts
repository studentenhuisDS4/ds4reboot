import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TurfComponent } from './turf.component';

describe('TurfComponentComponent', () => {
  let component: TurfComponent;
  let fixture: ComponentFixture<TurfComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TurfComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TurfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
