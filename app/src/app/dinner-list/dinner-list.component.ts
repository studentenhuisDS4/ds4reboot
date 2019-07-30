import {Component, Input, OnInit} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {dayNames, IDinner, userEntry, weekDates} from '../models/dinner.models';
import {compareAsc, isSameDay} from 'date-fns';
import {ProfileService} from '../services/profile.service';
import {IUser} from '../models/profile.model';
import {environment} from '../../environments/environment';
import {MatSnackBar} from '@angular/material';

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
    weekDinners: IDinner[] = [];
    todayDinner: IDinner;

    showWeek = false;
    weekCollapse = 'hide';
    todayCollapse = 'show';
    dayCollapse = 'none';

    user: IUser = null;

    @Input() miniView = false;

    constructor(private dinnerListService: DinnerListService, private profileService: ProfileService, private snackBar: MatSnackBar) {
        this.loadDinnerWeek();
        this.profileService.getProfile().then(result => {
            this.user = result;
        });
    }

    ngOnInit() {
    }

    signOffDinner(dinner: IDinner) {
        this.dinnerListService.signOff(this.user.id, dinner.date).then(output => {
                this.openSnackBar(`${this.user.housemate.display_name} cancelled for dinner.`, 'Ok');
                this.todayDinner = this.updateDinner(output.result, dinner.date);
            },
            error => {
                this.openSnackBar(`Failed sign-off action for ${this.user.housemate.display_name}!`, 'Shit');
            });
    }

    signupDinner(dinner: IDinner) {
        this.dinnerListService.signUp(this.user.id, dinner.date).then(output => {
                this.openSnackBar(`Signup +1 for ${this.user.housemate.display_name} successful!`, 'Ok');
                this.todayDinner = this.updateDinner(output.result, dinner.date);
            },
            error => {
                this.openSnackBar(`Failed action for ${this.user.housemate.display_name}!`, 'Shit');
            });
    }

    cookDinner(dinner: IDinner, signOff = false) {
        this.dinnerListService.cook(this.user.id, dinner.date, signOff).then(output => {
                if (output.result && output.result.cook && output.result.cook.id == this.user.id) {
                    this.openSnackBar(`Cooking by ${this.user.housemate.display_name} set.`, 'Ok');
                } else {
                    this.openSnackBar(`Cooking free to be claimed again.`, 'Ok');
                }
                this.todayDinner = this.updateDinner(output.result, dinner.date);
            },
            error => {
                this.openSnackBar(`Failed action for ${this.user.housemate.display_name}!`, 'Shit');
            });
    }

    closeDinner(dinner: IDinner) {
        const cost = dinner.cost;
        this.dinnerListService.close(dinner).then(output => {
                const d: IDinner = output.result;    // (TODO API) Hack for now...
                if (d && !d.open) {
                    this.openSnackBar(`Dinner closed.`, 'Ok');
                } else {
                    if (cost && !d.cost) {
                        this.openSnackBar(`Dinner opened (cost refunded).`, 'Ok');
                    } else {
                        this.openSnackBar(`Dinner opened.`, 'Ok');
                    }
                }
                this.todayDinner = this.updateDinner(d, d.date);
            },
            error => {
                this.openSnackBar(`Failed action for ${this.user.housemate.display_name}!`, 'Shit');
            });
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
    openDinner(dinner: IDinner): void {
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
                    result.push(this.createEmptyDinner(day));
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

    openSnackBar(message: string, action: string) {
        this.snackBar.open(message, action, {
            duration: 2000,
            verticalPosition: 'bottom',
        });
    }

    private updateDinner(dinner: IDinner, day: Date) {
        if (dinner) {
            return dinner;
        } else {
            return this.createEmptyDinner(day);
        }
    }

    private createEmptyDinner(day: Date): IDinner {
        return {
            id: null,
            date: day,
            signup_time: null, close_time: null, eta_time: null,
            num_eating: null, open: true, cost: null, cook: null,
            userdinners: [],
        };
    }

    private getUserEntry(todayDinner: IDinner, user: IUser) {
        return userEntry(todayDinner, user);
    }
}
