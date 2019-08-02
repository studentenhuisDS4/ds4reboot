import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ThesauComponent } from './thesau.component';

describe('ThesauComponent', () => {
  let component: ThesauComponent;
  let fixture: ComponentFixture<ThesauComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ThesauComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThesauComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
