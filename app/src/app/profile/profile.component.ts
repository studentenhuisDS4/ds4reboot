import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {SnackBarService} from '../services/snackBar.service';

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

    public userForm: FormGroup;
    public housemateForm: FormGroup;
    input: any = {
        email: String,
    };

    constructor(private snackBarService: SnackBarService) {
    }

    ngOnInit() {
        this.userForm = new FormGroup({
            email: new FormControl('', [Validators.required, Validators.maxLength(60)]),
            first_name: new FormControl('', [Validators.required, Validators.maxLength(60)]),
            last_name: new FormControl('', [Validators.required, Validators.maxLength(60)]),
            password: new FormControl(''),
            password_repeat: new FormControl(''),
        });
        this.housemateForm = new FormGroup({
            display_name: new FormControl('', [Validators.required, Validators.maxLength(100)]),
            room_number: new FormControl('', [Validators.required, Validators.maxLength(100)]),
            movein_date: new FormControl('', [Validators.required, Validators.maxLength(100)]),
            diet: new FormControl('', [Validators.required, Validators.maxLength(300)])
        });
    }

    createUser() {
        this.snackBarService.openSnackBar('This form is currently in the making. Have patience!', 'I will.');
    }
}
