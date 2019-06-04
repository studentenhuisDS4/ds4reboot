import {Component, OnInit} from '@angular/core';
import {AuthService} from '../services/auth.service';
import {FormControl, FormGroupDirective, NgForm, Validators} from '@angular/forms';
import {ErrorStateMatcher} from '@angular/material';
import {Router} from '@angular/router';
import {environment} from '../../environments/environment';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
    isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
        const isSubmitted = form && form.submitted;
        return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
    }
}

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
    state = '';
    DEBUG = environment.debug;

    emailFormControl = new FormControl('', [
        Validators.required,
        Validators.minLength(4),
    ]);
    passwordFormControl = new FormControl('', [
        Validators.required,
        Validators.minLength(4),
    ]);

    matcher = new MyErrorStateMatcher();

    constructor(private authService: AuthService, private router: Router) {
    }

    ngOnInit() {
        if (this.authService.isAuthenticated()) {
            this.state = 'logged in';
        }
    }

    verifyLogin() {
        // Assume login can be unnecessary
        if (this.passwordFormControl.valid && this.emailFormControl.valid) {
            if (!this.authService.isAuthenticated()) {
                // Not logged in
                this.state = 'logging in';
                this.authService.sendAuth(this.emailFormControl.value, this.passwordFormControl.value).subscribe((token) => {
                    this.state = 'logged in';
                    this.router.navigate(['home']);
                }, (error => {
                    if (environment.debug) {
                        console.log('Login panel error', error);
                    }
                    this.state = 'error logging in';
                }));
            } else {
                // Logged in
                this.state = 'logged in';
                this.router.navigate(['home']);
            }
        } else {
            this.state = 'Please fill in correct credentials.';
        }
    }
}
