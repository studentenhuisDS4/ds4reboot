import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DinnerListComponent } from './dinner-list.component';

describe('DinnerListComponent', () => {
  let component: DinnerListComponent;
  let fixture: ComponentFixture<DinnerListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DinnerListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DinnerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
