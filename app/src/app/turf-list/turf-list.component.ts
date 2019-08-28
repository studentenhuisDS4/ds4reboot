import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'app-turf-list',
    templateUrl: './turf-list.component.html',
    styleUrls: ['./turf-list.component.scss']
})
export class TurfListComponent implements OnInit {

    @Input() miniView = false;

    constructor() {

    }

    ngOnInit() {
    }

}
