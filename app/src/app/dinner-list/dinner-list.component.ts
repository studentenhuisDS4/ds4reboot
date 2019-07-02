import {Component, OnInit} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {dayNames, IDinnerDate, weekDates} from '../models/dinner.models';
import {compareAsc, isSameDay} from 'date-fns';
import {ProfileService} from '../services/profile.service';
import {IProfile} from '../models/profile.model';
import {environment} from '../../environments/environment';

@Component({
    selector: 'app-dinner-list',
    templateUrl: './dinner-list.component.html',
    styleUrls: ['./dinner-list.component.scss'],
    animations: [
        trigger('slideInOut', [
            state('show', style({
                opacity: '1.0',
            })),
            state('hide', style({
                opacity: '0',
                display: 'none',
            })),
            transition('show => hide', animate('100ms ease-in-out')),
            transition('hide => show', animate('150ms ease-in-out')),
        ]),
        trigger('slideOpen', [
            state('false', style({
                'margin-bottom': '-50px',
            })),
            state('true', style({
                'max-width': '100%',
                position: 'absolute',
                top: '200px',
                'z-index': 2,
                'margin-bottom': '10px',
            })),
            transition('* => *', animate('200ms ease-in-out')),
        ])
    ]
})
export class DinnerListComponent implements OnInit {
    weekDinners: IDinnerDate[] = [];
    todayDinner: IDinnerDate;

    showWeek = false;
    weekCollapse = 'hide';
    todayCollapse = 'show';
    dayCollapse = 'none';

    user: IProfile = null;

    constructor(private dinnerListService: DinnerListService, private profileService: ProfileService) {
        this.loadDinnerWeek();
        this.profileService.getProfile().then(result => {
            this.user = result;
        });
        // console.log(this.profileService.getUserId());
    }

    ngOnInit() {
    }

    signupDinner(dinner: IDinnerDate) {
        console.log('Test complete');
    }

    // Animation on week
    toggleWeek(): void {
        this.showWeek = !this.showWeek;
        if (!this.showWeek) {
            this.todayDinner = this.findToday();
            if (!this.todayDinner) {
                console.log('Error happened while finding today! Resorting to week overview.');
                this.showWeek = true;
            }
        }
        // Trigger animation
        this.weekCollapse = this.weekCollapse === 'show' ? 'hide' : 'show';
        this.todayCollapse = this.weekCollapse === 'hide' ? 'show' : 'hide';
    }

    // Animation on day
    openDinner(dinner: IDinnerDate): void {
        if (environment.debug) {
            console.log('Dinner day pressed.', dinner);
        }
        this.dayCollapse = this.dayCollapse === dinner.date.toString() ? 'none' : dinner.date.toString();
    }


    findToday() {
        const today = new Date();
        let foundDinner = null;
        if (this.weekDinners != null) {
            this.weekDinners.forEach(dinner => {
                if (isSameDay(dinner.date, today)) {
                    foundDinner = dinner;
                }
            });
        }
        return foundDinner;
    }

    loadDinnerWeek() {
        this.weekDinners = [];
        // Push nonexistent days on the pile as well.
        this.dinnerListService.getDinnerWeek().then(result => {
            weekDates(new Date()).forEach(day => {
                const findDay = result.find(r => isSameDay(r.date, day));
                if (!findDay) {
                    result.push({
                        id: null,
                        date: day,
                        signup_time: null, close_time: null, eta_time: null,
                        num_eating: null, open: true, cost: null, cook: null,
                    });
                    result.sort((a, b) => compareAsc(a.date, b.date));
                }
            });
            this.weekDinners = result;
            this.todayDinner = this.findToday();
        });
    }

    getWeekday(date: Date) {
        return dayNames[(new Date(date)).getDay()];
    }

}
