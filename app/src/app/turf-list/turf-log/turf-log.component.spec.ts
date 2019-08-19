import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TurfLogComponent } from './turf-log.component';

describe('TurfLogComponent', () => {
  let component: TurfLogComponent;
  let fixture: ComponentFixture<TurfLogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TurfLogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TurfLogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
