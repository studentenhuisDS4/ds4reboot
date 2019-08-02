import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';
import {SnackBarService} from '../../services/snackBar.service';
import {emailValidator} from '../../services/validators/async.validator';

@Component({
    selector: 'app-user-edit',
    templateUrl: './user-edit.component.html',
    styleUrls: ['./user-edit.component.scss']
})
export class UserEditComponent implements OnInit {
    user: IUser;
    private editUserForm: FormGroup;

    constructor(
        private userService: UserService,
        private snackBarService: SnackBarService
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
            this.user = result;
            this.editUserForm.patchValue(result);
        });

        this.editUserForm = new FormGroup({
            email: new FormControl('',
                {
                    validators: [Validators.required, Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')],
                    asyncValidators: [emailValidator(this.userService)]
                }),
            password: new FormControl('',
                [Validators.minLength(6)]),
            password_repeat: new FormControl('',
                [Validators.minLength(6), this.matchValues('password')]),
            first_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(30)]),
            last_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(150)]),
            housemate: new FormGroup({
                room_number: new FormControl('',
                    [Validators.required, Validators.min(1), Validators.max(22)]),
                diet: new FormControl('', [Validators.maxLength(300)])
            }),
        });
    }

    editUser() {
        this.editUserForm.markAllAsTouched();
        if (this.editUserForm.valid) {
            this.userService.updateUserFull(this.editUserForm).then(result => {
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
