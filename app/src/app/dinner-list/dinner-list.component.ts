import {Component, OnInit} from '@angular/core';
import {DinnerListService, IDinnerDate} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';

@Component({
    selector: 'app-dinner-list',
    templateUrl: './dinner-list.component.html',
    styleUrls: ['./dinner-list.component.scss'],
    animations: [
        trigger('slideInOut', [
            state('in', style({
                overflow: 'hidden',
                height: '100px',
                width: '250px',
            })),
            state('out', style({
                opacity: '0',
                height: '0px',
                overflow: 'hidden',
                width: '0px'
            })),
            transition('in => out', animate('200ms ease-in-out')),
            transition('out => in', animate('400ms ease-in-out'))
        ])
    ]
})
export class DinnerListComponent implements OnInit {
    dinners: IDinnerDate[] = [];
    displayedColumns = ['id', 'date', 'cost', 'open'];
    helpMenuOpen = 'out';
    constructor(private dinnerListService: DinnerListService) {
        // dinnerListService.getDinnerList().subscribe(result => {
        //     this.dinners = result;
        // }, error => {
        //     if (environment.debug) {
        //         console.log('Error:', error);
        //     }
        // });
    }

    ngOnInit() {
    }

    toggleHelpMenu(): void {
        this.helpMenuOpen = this.helpMenuOpen === 'out' ? 'in' : 'out';
    }
}
