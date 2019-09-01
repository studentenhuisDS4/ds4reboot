import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'app-spinner',
    templateUrl: './spinner.component.html',
    styleUrls: ['./spinner.component.scss']
})
export class SpinnerComponent implements OnInit {

    @Input() color = 'primary';
    @Input() inCard = false;
    @Input() backdrop = true;
    @Input() overlay = true;

    constructor() {
    }

    ngOnInit() {
    }

}
