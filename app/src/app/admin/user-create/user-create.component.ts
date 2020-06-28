import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { AbstractControl, FormControl, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { SnackBarService } from '../../services/snackBar.service';
import { IUser } from '../../models/user.model';
import { emailValidator, usernameValidator } from '../../services/validators/async.validator';
import { format } from 'date-fns';
import { environment } from '../../../environments/environment';

@Component({
    selector: 'app-user-create',
    templateUrl: './user-create.component.html',
    styleUrls: ['./user-create.component.scss']
})
export class UserCreateComponent implements OnInit {
    public createUserForm: FormGroup;
    lastFirstName = '';
    lastLastName = '';
    user: IUser;

    private storeFormKey = 'user-create-formdata';

    constructor(
        private userService: UserService,
        private snackBarService: SnackBarService
    ) {
    }

    matchValues(matchTo: string): (AbstractControl) => ValidationErrors | null {
        return (control: AbstractControl): ValidationErrors | null => {
            return !!control.parent &&
                !!control.parent.value &&
                control.value === control.parent.controls[matchTo].value ? null : { isNotMatching: true };
        };
    }

    ngOnInit() {
        this.userService.getFullProfile().then(result => {
            this.user = result;
        });

        this.createUserForm = new FormGroup({
            email: new FormControl('',
                {
                    validators: [Validators.required, Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$')],
                    asyncValidators: [emailValidator(this.userService, null)]
                }),
            first_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(30)]),
            last_name: new FormControl('',
                [Validators.required, Validators.minLength(2), Validators.maxLength(150)]),
            username: new FormControl('', {
                validators: [Validators.required, Validators.minLength(4), Validators.maxLength(150)],
                asyncValidators: [usernameValidator(this.userService)]
            }),
            password: new FormControl('',
                [Validators.required, Validators.minLength(6)]),
            password_repeat: new FormControl('',
                [Validators.required, Validators.minLength(6), this.matchValues('password')]),
            housemate: new FormGroup({
                display_name: new FormControl('',
                    [Validators.required, Validators.maxLength(100)]),
                room_number: new FormControl('',
                    [Validators.required, Validators.min(1)]),
                movein_date: new FormControl('', [Validators.required]),
                diet: new FormControl('', [Validators.maxLength(300)])
            }),
        });

        this.createUserForm.get('housemate').get('movein_date').setValue(format(new Date(), 'YYYY-MM-DD'));

        const savedForm = localStorage.getItem(this.storeFormKey);
        if (savedForm) {
            this.createUserForm.setValue(JSON.parse(savedForm));
            this.lastFirstName = this.V('first_name');
            this.lastLastName = this.V('last_name');
        }

        this.createUserForm.valueChanges.subscribe(val => {
            localStorage.setItem(this.storeFormKey, JSON.stringify(this.createUserForm.value));

            const firstName = this.createUserForm.get('first_name');
            const lastName = this.createUserForm.get('last_name');
            if (firstName.valid && lastName.valid && (this.lastFirstName !== firstName.value || this.lastLastName !== lastName.value)) {
                const username = firstName.value[0].toLowerCase() + lastName.value.toLowerCase();
                if (this.createUserForm.get('username').value !== username) {
                    this.createUserForm.get('username').setValue(username);
                    this.lastLastName = lastName.value;
                    this.lastFirstName = firstName.value;
                }
            }
        });
    }

    createUser() {
        this.createUserForm.markAllAsTouched();
        if (this.createUserForm.valid) {
            this.userService.createUser(this.createUserForm).then(result => {
                localStorage.removeItem(this.storeFormKey);
                this.createUserForm.reset();

                if (environment.debug) {
                    console.log(result);
                }
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
        return this.createUserForm.get(control).value;
    }

    public E(control: string) {
        return this.createUserForm.controls[control].errors;
    }

    public C(control: string) {
        return this.createUserForm.controls[control];
    }

}
