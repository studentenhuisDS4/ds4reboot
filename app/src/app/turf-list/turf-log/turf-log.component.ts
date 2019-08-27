import {Component, Input, OnInit} from '@angular/core';
import {TurfListService} from '../../services/turf-list.service';
import {ITurfLogAggregation, ITurfLogEntry, TurfLogFilter} from '../../models/turf.model';

@Component({
    selector: 'app-turf-log',
    templateUrl: './turf-log.component.html',
    styleUrls: ['./turf-log.component.scss']
})
export class TurfLogComponent implements OnInit {
    @Input() miniView;
    turfLogEntries: ITurfLogEntry[];
    filter = new TurfLogFilter();
    aggregation: ITurfLogAggregation = {};

    constructor(
        private turfService: TurfListService
    ) {
        this.turfService.getTurfLog(this.filter, this.aggregation).then(result => {
            this.turfLogEntries = result.results;
        });

        this.filter.count = 1;
    }

    ngOnInit() {
    }

}
