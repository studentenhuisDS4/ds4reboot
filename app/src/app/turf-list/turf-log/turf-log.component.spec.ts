import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TurfLogComponent } from './turf-log.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('TurfLogComponent', () => {
    let component: TurfLogComponent;
    let fixture: ComponentFixture<TurfLogComponent>;
    let httpMock: HttpTestingController;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientTestingModule,
                MatPaginatorModule,
                BrowserAnimationsModule,
                MatSortModule],
            declarations: [TurfLogComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TurfLogComponent);
        component = fixture.componentInstance;
        httpMock = TestBed.get(HttpTestingController);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
