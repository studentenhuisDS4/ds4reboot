import {Component, OnInit} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {IDinnerDate} from '../services/models/dinner.models';

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
                // width: '0px'
            })),
            transition('in => out', animate('150ms ease-in-out')),
            transition('out => in', animate('200ms ease-in-out'))
        ])
    ]
})
export class DinnerListComponent implements OnInit {
    dinnersWeek: IDinnerDate[] = [];
    helpMenuOpen = 'in';

    constructor(private dinnerListService: DinnerListService) {
        this.loadDinnerWeek();
    }

    ngOnInit() {
    }

    toggleHelpMenu(): void {
        this.helpMenuOpen = this.helpMenuOpen === 'out' ? 'in' : 'out';
    }

    loadDinnerWeek() {
        this.dinnerListService.getDinnerWeek().then(result => {
            this.dinnersWeek = result;
        });
    }

    convertDateToWeekday(date: string) {
        return this.dinnerListService.dayNames[(new Date(date)).getDay()];
    }
}
