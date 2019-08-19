import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'app-turf-log',
    templateUrl: './turf-log.component.html',
    styleUrls: ['./turf-log.component.scss']
})
export class TurfLogComponent implements OnInit {
    @Input() miniView;

    constructor() {
    }

    ngOnInit() {
    }

}
