import {Component, OnDestroy, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';
import {SnackBarService} from '../../services/snackBar.service';
import {emailValidator} from '../../services/validators/async.validator';
import {ActivatedRoute} from '@angular/router';
import {Subscription} from 'rxjs';

@Component({
    selector: 'app-user-edit',
    templateUrl: './user-edit.component.html',
    styleUrls: ['./user-edit.component.scss']
})
export class UserEditComponent implements OnInit, OnDestroy {
    editedUserId: number;
    editedUser: IUser;
    private routeSub: Subscription;
    private editUserForm: FormGroup;
    private isAdmin: boolean;

    constructor(
        private userService: UserService,
        private snackBarService: SnackBarService,
        private route: ActivatedRoute
    ) {
    }

    matchValues(matchTo: string): (AbstractControl) => ValidationErrors | null {
        return (control: AbstractControl): ValidationErrors | null => {
            return !!control.parent &&
            !!control.parent.value &&
            control.value === control.parent.controls[matchTo].value ? null : {isNotMatching: true};
        };
    }

    ngOnDestroy() {
        if (this.routeSub) {
            this.routeSub.unsubscribe();
        }
    }

    ngOnInit() {
        this.route.params.subscribe(params => {
            this.editedUserId = params.id;
            this.userService.getFullProfile(this.editedUserId).then(result => {
                this.editedUser = result;
                this.editUserForm.patchValue(result);
            });
            this.userService.getProfile().then(result => {
                this.isAdmin = result.is_staff;
            });
        });

        this.editUserForm = new FormGroup({
            email: new FormControl(null,
                {
                    validators: [Validators.pattern('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[a-z]{2,4}$')],
                    asyncValidators: [emailValidator(this.userService, this.editedUserId)]
                }),
            password: new FormControl(null,
                [Validators.minLength(6)]),
            password_repeat: new FormControl(null,
                [Validators.minLength(6), this.matchValues('password')]),
            first_name: new FormControl(null,
                [Validators.required, Validators.minLength(2), Validators.maxLength(30)]),
            last_name: new FormControl(null,
                [Validators.required, Validators.minLength(2), Validators.maxLength(150)]),
            housemate: new FormGroup({
                display_name: new FormControl(null,
                    [Validators.required, Validators.maxLength(100)]),
                room_number: new FormControl(null,
                    [Validators.required, Validators.min(1)]),
                diet: new FormControl(null, [Validators.maxLength(300)])
            }),
        });
    }

    editUser() {
        this.editUserForm.markAllAsTouched();
        if (this.editUserForm.valid) {
            this.userService.updateUserFull(this.editUserForm, this.editedUser.id).then(result => {
                this.snackBarService.openSnackBar('User edit succesful.', 'Ok.');
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

    public V(control: string) {
        return this.editUserForm.get(control).value;
    }

    public E(control: string) {
        return this.editUserForm.controls[control].errors;
    }

    public C(control: string) {
        return this.editUserForm.controls[control];
    }

}
