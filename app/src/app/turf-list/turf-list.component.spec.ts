import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { TurfListComponent } from './turf-list.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('TurfListComponent', () => {
    let component: TurfListComponent;
    let fixture: ComponentFixture<TurfListComponent>;
    let httpMock: HttpTestingController;

    beforeEach(async(() => {
        TestBed
            .configureTestingModule({
                imports: [HttpClientTestingModule],
                declarations: [TurfListComponent]
            })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TurfListComponent);
        component = fixture.componentInstance;
        httpMock = TestBed.get(HttpTestingController);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
