import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BoeteComponent } from './boete.component';

describe('BoeteComponent', () => {
  let component: BoeteComponent;
  let fixture: ComponentFixture<BoeteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BoeteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BoeteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
