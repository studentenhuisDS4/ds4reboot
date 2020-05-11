import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganisationComponent } from './organisation.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('OrganizationComponent', () => {
  let component: OrganisationComponent;
  let fixture: ComponentFixture<OrganisationComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [ OrganisationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganisationComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.get(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
