import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {DinnerListService} from '../services/dinner-list.service';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {dayNames, IDinner, userEntry, weekDates} from '../models/dinner.models';
import {compareAsc, isSameDay} from 'date-fns';
import {UserService} from '../services/user.service';
import {IUser} from '../models/user.model';
import {environment} from '../../environments/environment';
import {MatAutocomplete, MatSnackBar} from '@angular/material';
import {EasterEggService} from '../services/easter.service';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatAutocompleteSelectedEvent} from '@angular/material/typings/esm5/autocomplete';
import {FormControl} from '@angular/forms';
import {filter, map} from 'rxjs/operators';
import {Observable} from 'rxjs';


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
                'margin-bottom': '-60px',
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
    currentDinner: IDinner;

    showWeek = false;
    weekCollapse = 'hide';
    todayCollapse = 'show';
    dayCollapse = 'none';

    user: IUser = null;
    @Input() miniView = false;

    activeUsers: IUser[] = [];
    filteredActiveUsers: Observable<IUser[]>;
    readonly separatorKeysCodes: number[] = [ENTER, COMMA];
    displayNameCtrl = new FormControl();
    @ViewChild('userDinnerInput', {static: false}) userDinnerInput: ElementRef<HTMLInputElement>;
    @ViewChild('autoComplete', {static: false}) matAutocomplete: MatAutocomplete;

    constructor(
        private dinnerListService: DinnerListService,
        private userService: UserService,
        private snackBar: MatSnackBar,
        private easterEgg: EasterEggService) {
        this.loadDinnerWeek();
        this.userService.getProfile().then(result => {
            this.user = result;
        });

        this.userService.getActiveUsers().then(result => {
            this.activeUsers = result;
            this.filteredActiveUsers = this.displayNameCtrl.valueChanges.pipe(
                filter(r => r !== ''),
                map((displayName: string | null) => displayName ? this._filter(displayName) : this.activeUsers)
            );
        });
    }

    ngOnInit() {
    }

    signOffDinner(dinner: IDinner, user = this.user) {
        this.dinnerListService.signOff(user.id, dinner.date).then(output => {
                this.openSnackBar(`${user.housemate.display_name} cancelled for dinner.`, 'Ok');
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
            },
            error => {
                this.openSnackBar(`Failed sign-off action for ${user.housemate.display_name}!`, 'Shit');
            });
    }

    signupDinner(dinner: IDinner, user = this.user) {
        return this.dinnerListService.signUp(user.id, dinner.date).then(output => {
                this.openSnackBar(`Signup +1 for ${user.housemate.display_name} successful!`, 'Ok');
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
                return output;
            },
            error => {
                this.openSnackBar(`Failed action for ${user.housemate.display_name}!`, 'Shit');
            });
    }

    cookDinner(dinner: IDinner, signOff = false, user = this.user) {
        this.dinnerListService.cook(user.id, dinner.date, signOff).then(output => {
                if (output.result && output.result.cook && output.result.cook.id === this.user.id) {
                    this.openSnackBar(`Cooking by ${this.user.housemate.display_name} set.`, 'Ok');
                } else {
                    this.openSnackBar(`Cooking free to be claimed again.`, 'Ok');
                }
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
            },
            error => {
                this.openSnackBar(`Failed action for ${user.housemate.display_name}!`, 'Shit');
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
                this.currentDinner = this.updateDinner(d, d.date);
                this.updateWeek();
            },
            error => {
                this.openSnackBar(`Failed action for ${this.user.housemate.display_name}!`, 'Shit');
            });
    }

    // Animation on week
    toggleWeek(): void {
        this.showWeek = !this.showWeek;
        if (!this.showWeek) {
            this.currentDinner = this.findToday();
            if (!this.currentDinner) {
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

    updateWeek() {
        this.weekDinners.forEach((dinner, index) => {
            if (isSameDay(dinner.date, this.currentDinner.date)) {
                this.weekDinners[index].num_eating = this.currentDinner.num_eating;
                this.weekDinners[index].cook = this.currentDinner.cook;
                this.weekDinners[index].userdinners = this.currentDinner.userdinners;
                this.weekDinners[index].open = this.currentDinner.open;
            }
        });
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
            this.currentDinner = this.findToday();
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

    onUserDinnerKey($event: KeyboardEvent) {
        // Avoid duplicate event and check if something was entered.
        if ($event.key === 'Enter' && this.userDinnerInput.nativeElement.value && !this.filteredActiveUsers[0]) {
            const user: IUser = this.matAutocomplete.options.first.value;
            this.signupDinner(this.currentDinner, user);
        }
    }

    private selectedTypeAhead(event: MatAutocompleteSelectedEvent) {
        const user: IUser = event.option.value;
        this.signupDinner(this.currentDinner, user);
        this.userDinnerInput.nativeElement.value = user.housemate.display_name;
    }

    private _filter(filterInput: string | IUser): IUser[] {
        let filterValue = '';
        if (typeof filterInput === 'string') {
            filterValue = filterInput ? filterInput.toLowerCase() : '';
        } else {
            filterValue = filterInput.housemate.display_name.toLowerCase();
        }
        if (!filterValue) {
            return this.activeUsers.slice();
        }
        return this.activeUsers.filter(user => user.housemate.display_name.toLowerCase().indexOf(filterValue) !== -1);
    }

    private filterDining() {
        return this.currentDinner.userdinners.filter(ud => {
            return !ud.is_cook;
        });
    }

    private filterCook() {
        return this.currentDinner.userdinners.filter(ud => {
            return ud.is_cook;
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
