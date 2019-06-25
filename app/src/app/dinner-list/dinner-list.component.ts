import {Component, OnInit} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {convertStringToDate, dayNames, IDinnerDate, weekDates} from '../models/dinner.models';

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
                'max-width': '100%',
                position: 'absolute',
                top: '200px',
                'z-index': 2,
                'margin-bottom': '10px',
            })),
            transition('* => *', animate('300ms ease-in-out')),
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

    // Animation on week
    toggleWeek(): void {
        this.weekCollapse = this.weekCollapse === 'out' ? 'in' : 'out';
        this.showWeek = !this.showWeek;
        if (!this.showWeek) {
            const todayDinner = this.findToday();
            if (todayDinner) {
                this.dinners = [todayDinner];
            } else {
                this.dinners = [this.dinnersWeek[0]];
            }
        } else {
            this.dinners = this.dinnersWeek;
        }
        this.weekCollapse = this.weekCollapse === 'out' ? 'in' : 'out';
    }

    // Animation on day
    openDinner(dinner: IDinnerDate): void {
        this.dayCollapse = this.dayCollapse === dinner.date.toString() ? 'none' : dinner.date.toString();
    }


    findToday() {
        const today = new Date();
        if (this.dinnersWeek != null) {
            this.dinnersWeek.forEach(dinner => {
                if (dinner.date === today.getDate().toString()) {
                    return dinner;
                }
            });
        }
        return null;
    }

    loadDinnerWeek() {
        this.dinnersWeek = [];
        this.dinnerListService.getDinnerWeek().then(result => {
            weekDates(new Date()).forEach(day => {
                const findDay = result.find(r => convertStringToDate(r.date) === day.getDay());
                if (!findDay) {
                    result.push({
                        id: null,
                        date: day,
                        signup_time: null, close_time: null, eta_time: null,
                        num_eating: null, open: true, cost: null, cook: null,
                    });
                    result.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
                }
            });
            this.dinnersWeek = result;
            this.dinners = this.dinnersWeek;
        });
    }

    convertDateToWeekday(date: string) {
        return dayNames[(new Date(date)).getDay()];
    }


}
