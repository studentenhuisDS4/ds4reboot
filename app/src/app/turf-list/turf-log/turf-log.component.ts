import {AfterViewInit, Component, Input, ViewChild} from '@angular/core';
import {TurfService} from '../../services/turf.service';
import {ITurfLogAggregation, ITurfLogEntry, TurfLogFilter} from '../../models/turf.model';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import {merge, of} from 'rxjs';
import {catchError, map, startWith, switchMap} from 'rxjs/operators';

@Component({
    selector: 'app-turf-log',
    templateUrl: './turf-log.component.html',
    styleUrls: ['./turf-log.component.scss']
})
export class TurfLogComponent implements AfterViewInit {
    @Input() miniView;

    displayedColumns = ['turf_by', 'turf_to', 'turf_count', 'turf_time', 'turf_type'];
    filter = new TurfLogFilter();
    aggregation: ITurfLogAggregation = {};
    dataSource: ITurfLogEntry[];
    @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
    @ViewChild(MatSort, {static: true}) sort: MatSort;
    loadingPage = false;
    logCount: number;

    constructor(
        private turfService: TurfService
    ) {
    }

    ngAfterViewInit() {
        this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);

        merge(this.sort.sortChange, this.paginator.page)
            .pipe(
                startWith({}),
                switchMap(() => {
                    this.loadingPage = true;
                    return this.turfService.getTurfLog(this.filter, this.aggregation, {
                        index: this.paginator.pageIndex,
                        size: this.paginator.pageSize
                    });
                }),
                map(data => {
                    this.loadingPage = false;
                    this.logCount = data.count;

                    return data.results;
                }),
                catchError(() => {
                    this.loadingPage = false;
                    return of([]);
                })
            ).subscribe(data => this.dataSource = data);
    }
}
