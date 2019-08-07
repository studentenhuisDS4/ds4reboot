import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';
import {SnackBarService} from '../../services/snackBar.service';
import {Router} from '@angular/router';

@Component({
    selector: 'app-profile-edit',
    templateUrl: './profile-edit.component.html',
    styleUrls: ['./profile-edit.component.scss']
})
export class ProfileEditComponent implements OnInit {
    user: IUser;
    isHouse = false;
    private editProfileForm: FormGroup;

    constructor(
        private userService: UserService,
        private snackBarService: SnackBarService,
        private router: Router
    ) {
    }

    matchValues(matchTo: string): (AbstractControl) => ValidationErrors | null {
        return (control: AbstractControl): ValidationErrors | null => {
            return !!control.parent &&
            !!control.parent.value &&
            control.value === control.parent.controls[matchTo].value ? null : {isNotMatching: true};
        };
    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            if (result == null) {
                this.isHouse = this.userService.checkHouse();
                if (this.isHouse) {
                    this.router.navigateByUrl('/home');
                }
            } else {
                this.user = result;
                this.editProfileForm.patchValue(result);
            }
        });

        this.editProfileForm = new FormGroup({
            first_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(30)]),
            last_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(150)]),
            password: new FormControl('',
                [Validators.minLength(6)]),
            password_repeat: new FormControl('',
                [Validators.minLength(6), this.matchValues('password')]),
            housemate: new FormGroup({
                display_name: new FormControl('',
                    [Validators.required, Validators.minLength(2), Validators.maxLength(30)]),
                room_number: new FormControl('',
                    [Validators.required, Validators.min(1), Validators.max(22)]),
                diet: new FormControl('', [Validators.maxLength(300)])
            }),
        });
    }

    editUser() {
        this.editProfileForm.markAllAsTouched();
        if (this.editProfileForm.valid) {
            this.userService.updateProfile(this.editProfileForm).then(result => {
                this.snackBarService.openSnackBar('Profile edit successful.', 'Ok.');
                this.router.navigateByUrl('/profile');
            }, error => {
                if (error) {
                    console.error(error);
                }
                this.snackBarService.openSnackBar('Error occurred.', 'Ok.');
            });
        } else {
            this.snackBarService.openSnackBar('Correct the highlighted fields.', 'Ok.');
        }
    }

    private V(control: string) {
        return this.editProfileForm.get(control).value;
    }

    private E(control: string) {
        return this.editProfileForm.controls[control].errors;
    }

    private H_E(control: string) {
        return (this.editProfileForm.controls.housemate as FormGroup).controls[control].errors;
    }

    private C(control: string) {
        return this.editProfileForm.controls[control];
    }

}
