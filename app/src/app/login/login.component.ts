import {Component, HostListener, OnInit} from '@angular/core';
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
    stateSecondary = '';
    DEBUG = environment.debug;
    awaitingLogin = false;

    emailFormControl = new FormControl('', [
        Validators.required,
        Validators.minLength(4),
    ]);
    passwordFormControl = new FormControl('', [
        Validators.required,
        Validators.minLength(4),
    ]);
    matcher = new MyErrorStateMatcher();

    @HostListener('document:keypress', ['$event'])
    handleKeyboardPress(event: any) {
        if (event.key === 'Enter') {
            this.verifyLogin();
        }
    }

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
                this.awaitingLogin = true;
                this.authService.sendAuth(this.emailFormControl.value, this.passwordFormControl.value).subscribe((token) => {
                    this.state = 'logged in';
                    this.router.navigate(['home']);
                    this.awaitingLogin = false;
                }, (error => {
                    if (environment.debug) {
                        console.log('Login panel error', error);
                    }
                    if (error.status === 0) {
                        this.state = 'Server did not respond!';
                    } else if (error.status === 400) {
                        this.state = 'Server responded with an error:';
                        this.stateSecondary = error.error.non_field_errors[0];
                    }
                    this.awaitingLogin = false;
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
