import {Component, OnInit} from '@angular/core';
import {DinnerListService, IDinnerDate} from '../services/dinner-list.service';
import {environment} from '../../environments/environment';

@Component({
    selector: 'app-dinner-list',
    templateUrl: './dinner-list.component.html',
    styleUrls: ['./dinner-list.component.scss']
})
export class DinnerListComponent implements OnInit {
    dinners: IDinnerDate[] = [];
    displayedColumns = ['id', 'date', 'cost', 'open'];

    constructor(private dinnerListService: DinnerListService) {
        dinnerListService.getDinnerList().subscribe(result => {
            this.dinners = result;
        }, error => {
            if (environment.debug) {
                console.log('Error:', error);
            }
        });
    }

    ngOnInit() {
    }

    clickNav() {
        console.log('asd');
    }

}
