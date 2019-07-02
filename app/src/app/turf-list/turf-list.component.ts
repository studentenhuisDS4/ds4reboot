import {Component, OnInit} from '@angular/core';
import {TurfListService} from '../services/turf-list.service';
import {TurfType} from '../models/turf.model';
import {ProfileService} from '../services/profile.service';
import {IProfile} from '../models/profile.model';
import {IStatus} from '../models/api.model';
import {MatSnackBar} from '@angular/material';

@Component({
    selector: 'app-turf-list',
    templateUrl: './turf-list.component.html',
    styleUrls: ['./turf-list.component.scss']
})
export class TurfListComponent implements OnInit {
    user: IProfile = null;

    constructor(private turfListService: TurfListService, private profileService: ProfileService, private snackBar: MatSnackBar) {
        this.profileService.getProfile().then(result => {
            this.user = result;
        });
    }

    ngOnInit() {
    }

    turfItem(turfType: TurfType = TurfType.BEER) {
        this.turfListService.turfItem({
            turf_count: 1,
            turf_note: `${this.user.username} turved in BETA phase. Prev_amount${this.user.housemate.sum_bier}`,
            turf_type: turfType,
            turf_user_id: this.user.id
        }).then(result => {
            if (result.status === IStatus.SUCCESS) {
                this.user.housemate = result.housemate;
                this.openSnackBar(`Turved 1 beer. Total: ${this.user.housemate.sum_bier}`, 'Ok');
            }
        });
    }

    openSnackBar(message: string, action: string) {
        this.snackBar.open(message, action, {
            duration: 2000,
            verticalPosition: 'top',
        });
    }

}
