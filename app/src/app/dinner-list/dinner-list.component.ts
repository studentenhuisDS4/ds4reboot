import {Component, OnInit} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {IDinnerDate} from '../models/dinner.models';

@Component({
    selector: 'app-dinner-list',
    templateUrl: './dinner-list.component.html',
    styleUrls: ['./dinner-list.component.scss'],
    animations: [
        trigger('slideInOut', [
            state('in', style({
                overflow: 'hidden',
                height: '100px',
            })),
            state('out', style({
                opacity: '0',
                height: '0px',
                overflow: 'hidden',
                'z-index': '-2',
            })),
            transition('in => out', animate('150ms ease-in-out')),
            transition('out => in', animate('200ms ease-in-out'))
        ]),
        trigger('slideOpen', [
            state('false', style({
                'margin-bottom': '-70px',
            })),
            state('true', style({
                'margin-bottom': '10px',
            })),
            transition('* => *', animate('150ms ease-in-out')),
        ])
    ]
})
export class DinnerListComponent implements OnInit {
    dinnersWeek: IDinnerDate[] = [];
    dinners: IDinnerDate[] = [];
    showWeek = true;

    weekCollapse = 'in';
    dayCollapse = 'none';

    constructor(private dinnerListService: DinnerListService) {
        this.loadDinnerWeek();
    }

    ngOnInit() {
    }

    toggleWeek(): void {
        this.weekCollapse = this.weekCollapse === 'out' ? 'in' : 'out';
        this.showWeek = !this.showWeek;
        if (!this.showWeek) {
            this.dinners = [this.dinnersWeek[0]];
        } else {
            this.dinners = this.dinnersWeek;
        }
        this.weekCollapse = this.weekCollapse === 'out' ? 'in' : 'out';
    }

    openDinner(dinner: IDinnerDate): void {
        this.dayCollapse = this.dayCollapse === dinner.id.toString() ? 'none' : dinner.id.toString();
    }

    loadDinnerWeek() {
        this.dinnerListService.getDinnerWeek().then(result => {
            this.dinnersWeek = result;
            this.dinners = this.dinnersWeek;
        });
    }

    convertDateToWeekday(date: string) {
        return this.dinnerListService.dayNames[(new Date(date)).getDay()];
    }
}
