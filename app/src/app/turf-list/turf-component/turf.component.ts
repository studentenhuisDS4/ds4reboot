import {Component, Input, OnInit} from '@angular/core';
import {HOUSE_ID, IUser} from '../../models/user.model';
import {TurfListService} from '../../services/turf-list.service';
import {UserService} from '../../services/user.service';
import {SnackBarService} from '../../services/snackBar.service';
import {EasterEggService} from '../../services/easter.service';
import {TurfType} from '../../models/turf.model';
import {IStatus} from '../../models/api.model';

@Component({
    selector: 'app-turf-component',
    templateUrl: './turf.component.html',
    styleUrls: ['./turf.component.scss']
})
export class TurfComponent implements OnInit {
    user: IUser = null;
    busy = false;
    turfUsers: IUser[] = [];
    turfMultiplier = '1';
    isHouse = false;
    otherTurfVal = 1;
    showOther = false;

    @Input() miniView = false;

    constructor(
        private turfListService: TurfListService,
        private userService: UserService,
        private snackBarService: SnackBarService,
        private easterEggService: EasterEggService
    ) {
        this.isHouse = this.userService.checkHouse();
        if (this.isHouse) {
            this.userService.getHouseProfile().then(result => {
                this.user = result;
            });
        } else {
            this.userService.getProfile().then(result => {
                this.user = result;
            });
        }
        this.userService.getActiveUsers().then(result => {
            this.turfUsers = result;
        });
    }

    ngOnInit() {
        this.turfMultiplier = '1';
    }

    turfItem(turfType: TurfType = TurfType.BEER, amount = 1, turfUser = null) {
        if (turfUser == null) {
            turfUser = this.user;
        }
        let numericAmount: number;
        if (typeof amount === 'string') {
            numericAmount = parseInt(amount, 10);
        } else if (typeof amount === 'number') {
            numericAmount = amount;
        }
        if (turfType === TurfType.BEER && !Number.isInteger(numericAmount)) {
            this.snackBarService.openSnackBar(
                `Cant turf a beer partly.`,
                this.easterEggService.easterEggo());
            return;
        }
        if (this.user.id !== turfUser.id) {
            if (!confirm('Different housemate/kutSjaarsch. Confirm please.')) {
                return;
            }
        }
        this.busy = true;
        this.turfListService.turfItem({
            turf_count: amount,
            turf_note: `${turfUser.housemate.display_name} turved in BETA phase. Prev_amount${turfUser.housemate.sum_bier}`,
            turf_type: turfType,
            turf_user_id: turfUser.id
        }).then(output => {
            if (output.status === IStatus.SUCCESS) {
                if (!this.isHouse) {
                    this.user.housemate = output.result;
                } else if (turfUser.id === HOUSE_ID) {
                    this.user.housemate = output.result;
                }
                let prop;
                if (turfType === TurfType.BEER) {
                    prop = 'sum_bier';
                } else if (turfType === TurfType.RWINE) {
                    prop = 'sum_rwijn';
                } else if (turfType === TurfType.WWINE) {
                    prop = 'sum_wwijn';
                }
                this.snackBarService.openSnackBar(
                    `Turved ${amount} ${turfType} on ${turfUser.housemate.display_name}. Total: ${turfUser.housemate[prop]}`,
                    this.easterEggService.easterEggo());
            }
            this.busy = false;
            this.turfMultiplier = '1';
            this.otherTurfVal = 1;
            this.showOther = false;
        });
    }

}
