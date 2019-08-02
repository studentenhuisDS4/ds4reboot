import {Component, Input, OnInit} from '@angular/core';
import {TurfListService} from '../services/turf-list.service';
import {TurfType} from '../models/turf.model';
import {UserService} from '../services/user.service';
import {IUser} from '../models/user.model';
import {IStatus} from '../models/api.model';
import {SnackBarService} from '../services/snackBar.service';
import {EasterEggService} from '../services/easter.service';

@Component({
    selector: 'app-turf-list',
    templateUrl: './turf-list.component.html',
    styleUrls: ['./turf-list.component.scss']
})
export class TurfListComponent implements OnInit {
    user: IUser = null;
    busy = false;
    turfUsers: IUser[] = [];
    isHouse = false;

    @Input() miniView = false;

    constructor(private turfListService: TurfListService,
                private userService: UserService,
                private snackBarService: SnackBarService,
                private easterEggService: EasterEggService) {
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
    }

    turfItem(turfType: TurfType = TurfType.BEER, amount = 1, turfUser = null) {
        if (turfUser == null) {
            turfUser = this.user;
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
                this.user.housemate = output.result;
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
        });
    }

}
