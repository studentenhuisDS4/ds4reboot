import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {DinnerService} from '../services/dinner.service';
import {dayNames, IDinner, userEntry, weekDates} from '../models/dinner.models';
import {compareAsc, isSameDay} from 'date-fns';
import {UserService} from '../services/user.service';
import {IUser} from '../models/user.model';
import {MatAutocomplete} from '@angular/material';
import {EasterEggService} from '../services/easter.service';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatAutocompleteSelectedEvent} from '@angular/material/typings/esm5/autocomplete';
import {FormControl, Validators} from '@angular/forms';
import {filter, map} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {SnackBarService} from '../services/snackBar.service';


@Component({
    selector: 'app-dinner-list',
    templateUrl: './dinner-list.component.html',
    styleUrls: ['./dinner-list.component.scss'],
})
export class DinnerListComponent implements OnInit {
    weekDinners: IDinner[] = [];
    currentDinner: IDinner;
    user: IUser = null;
    @Input() miniView = false;

    activeUsers: IUser[] = [];
    filteredActiveUsers: Observable<IUser[]>;
    readonly separatorKeysCodes: number[] = [ENTER, COMMA];
    displayNameCtrl = new FormControl();
    @ViewChild('userDinnerInput') userDinnerInput: ElementRef<HTMLInputElement>;
    @ViewChild('autoComplete') matAutocomplete: MatAutocomplete;
    preConfirm = false;

    dinnerCostCtrl = new FormControl();

    constructor(
        private dinnerListService: DinnerService,
        private userService: UserService,
        private snackBar: SnackBarService,
        private easterEgg: EasterEggService
    ) {
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

        this.dinnerCostCtrl = new FormControl(0, {
            validators: [Validators.required, Validators.min(0.01), Validators.max(100)]
        });
    }

    ngOnInit() {
    }

    loadDinnerWeek(date = new Date()) {
        this.weekDinners = [];
        // Push nonexistent days on the pile as well.
        this.dinnerListService.getDinnerWeek().then(result => {
            weekDates(new Date()).forEach(wdate => {
                const findDay = result.find(r => isSameDay(r.date, wdate));
                if (!findDay) {
                    result.push(this.createEmptyDinner(wdate));
                    result.sort((a, b) => compareAsc(a.date, b.date));
                }
            });
            this.weekDinners = result;
            this.currentDinner = this.findToday(date);
        });
    }

    setCurrentDay(day = new Date()) {
        this.currentDinner = this.findToday(day);
    }

    signOffDinner(dinner: IDinner, user = this.user) {
        this.dinnerListService.signOff(user.id, dinner.date).then(output => {
                this.snackBar.openSnackBar(`${user.housemate.display_name} cancelled for dinner.`, 'Ok');
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
            },
            error => {
                this.snackBar.openSnackBar(`Failed sign-off action for ${user.housemate.display_name}!`, 'Shit');
            });
    }

    signupDinner(dinner: IDinner, user = this.user) {
        if (this.user && user.id !== this.user.id) {
            if (this.preConfirm) {
                this.preConfirm = false;
                return;
            }
            if (!confirm('This is not you, are you sure?')) {
                this.preConfirm = false;
                return;
            }
            this.preConfirm = false;
        }
        return this.dinnerListService.signUp(user.id, dinner.date).then(output => {
                this.snackBar.openSnackBar(`Signup +1 for ${user.housemate.display_name} successful!`, 'Ok');
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
                return output;
            },
            error => {
                this.snackBar.openSnackBar(`Failed action for ${user.housemate.display_name}!`, 'Shit');
            });
    }

    cookDinner(dinner: IDinner, signOff = false, user = this.user) {
        this.dinnerListService.cook(user ? user.id : dinner.cook.id, dinner.date, signOff).then(output => {
                if (user && output.result && output.result.cook && output.result.cook.id === this.user.id) {
                    this.snackBar.openSnackBar(`Cooking by ${this.user.housemate.display_name} set.`, 'Ok');
                } else {
                    this.snackBar.openSnackBar(`Cooking free to be claimed again.`, 'Ok');
                }
                this.currentDinner = this.updateDinner(output.result, dinner.date);
                this.updateWeek();
            },
            error => {
                this.snackBar.openSnackBar(`Failed action for ${user.housemate.display_name}!`, 'Shit');
            });
    }

    closeDinner(dinner: IDinner) {
        const cost = dinner.cost;
        this.dinnerListService.close(dinner).then(output => {
                const d: IDinner = output.result;
                if (d && !d.open) {
                    this.snackBar.openSnackBar(`Dinner closed.`, 'Ok');
                } else {
                    if (cost && !d.cost) {
                        this.snackBar.openSnackBar(`Dinner opened (cost refunded).`, 'Ok');
                    } else {
                        this.snackBar.openSnackBar(`Dinner opened.`, 'Ok');
                    }
                }
                this.currentDinner = this.updateDinner(d, d.date);
                this.updateWeek();
            },
            error => {
                this.snackBar.openSnackBar(`Failed action for ${this.user.housemate.display_name}!`, 'Shit');
            });
    }

    costDinner(dinner: IDinner = this.currentDinner) {
        if (!this.dinnerCostCtrl.valid) {
            this.dinnerCostCtrl.markAsTouched();
            return;
        }
        const cost = this.dinnerCostCtrl.value;
        this.dinnerListService.cost(dinner, cost).then(output => {
                const d: IDinner = output.result;
                if (d && d.cost) {
                    this.snackBar.openSnackBar(`Dinner cost set ${d.cost}.`, 'Ok');
                }
                this.currentDinner = this.updateDinner(d, d.date);
                this.updateWeek();
            },
            error => {
                this.snackBar.openSnackBar(`Failed cost action for ${this.user.housemate.display_name}!`, 'Shit');
            });
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

    findToday(day = new Date()) {
        let foundDinner = null;
        if (this.weekDinners != null) {
            this.weekDinners.forEach(dinner => {
                if (isSameDay(dinner.date, day)) {
                    foundDinner = dinner;
                }
            });
        }
        return foundDinner;
    }

    getWeekday(date: Date) {
        return dayNames[(new Date(date)).getDay()];
    }

    onUserDinnerKey($event: KeyboardEvent) {
        // Avoid duplicate event and check if something was entered.
        return;
        // if (this.userDinnerInput.nativeElement.value && !this.filteredActiveUsers[0]) {
        //     const user: IUser = this.matAutocomplete.options.first.value;
        //
        //     if (this.preConfirm === false && user.id !== this.user.id) {
        //         this.preConfirm = true;
        //     }
        //     this.signupDinner(this.currentDinner, user);
        // }
    }

    onDinnerCostMouseWheel($event: WheelEvent) {
        const cost = this.dinnerCostCtrl.value;
        if ($event.deltaY > 0 && cost >= 1) {
            this.dinnerCostCtrl.setValue(cost - 1);
        } else if ($event.deltaY < 0 && cost <= 99) {
            this.dinnerCostCtrl.setValue(cost + 1);
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
