import {Component, OnInit} from '@angular/core';
import {SnackBarService} from '../services/snackBar.service';
import {UserService} from '../services/user.service';
import {IUser} from '../models/user.model';
import {FormControl, FormGroup} from '@angular/forms';

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
    profileForm: FormGroup;

    profile: IUser;
    isHouse = false;

    constructor(
        private userService: UserService,
        private snackBarService: SnackBarService) {
    }

    ngOnInit(): void {
        this.profileForm = new FormGroup({
            first_name: new FormControl({value: '', disabled: true}),
            last_name: new FormControl({value: '', disabled: true}),
            housemate: new FormGroup({
                display_name: new FormControl({value: '', disabled: true}),
                room_number: new FormControl({value: '', disabled: true}),
                diet: new FormControl({value: '', disabled: true}),
            }),
        });

        this.userService.getProfile().then(result => {
            if (result == null) {
                this.isHouse = this.userService.checkHouse(null);
            } else {
                this.profile = result;
                this.profileForm.patchValue(result);
            }
        });


    }

}
