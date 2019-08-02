import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageReceiptsComponent } from './manage-receipts.component';

describe('ReceiptsComponent', () => {
  let component: ManageReceiptsComponent;
  let fixture: ComponentFixture<ManageReceiptsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ManageReceiptsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageReceiptsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
