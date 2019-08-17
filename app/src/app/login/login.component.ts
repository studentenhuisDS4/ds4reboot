import {Component, HostListener, OnInit} from '@angular/core';
import {AuthService} from '../services/auth.service';
import {FormControl, FormGroupDirective, NgForm, Validators} from '@angular/forms';
import {ErrorStateMatcher} from '@angular/material';
import {Router} from '@angular/router';
import {environment} from '../../environments/environment';
import {SnackBarService} from '../services/snackBar.service';

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

    constructor(private authService: AuthService,
                private router: Router,
                private snackBarService: SnackBarService) {
    }

    @HostListener('document:keypress', ['$event'])
    handleKeyboardPress(event: any) {
        if (event.key === 'Enter') {
            this.verifyLogin();
        }
    }

    ngOnInit() {
        if (this.authService.isAuthenticated()) {
            this.state = 'logged in';
            this.router.navigateByUrl('/home');
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
                    this.snackBarService.openSnackBar('Login error', 'Hmm');
                    if (environment.debug) {
                        console.log('Login panel error', error);
                    }

                    if (error.status !== 400) {
                        if (error.status === 0) {
                            this.state = 'Server did not respond!';
                        } else if (error.status === 400) {
                            this.state = 'Server responded with an error:';
                            this.stateSecondary = error.error.non_field_errors[0];
                        }
                    } else {
                        if (error.error && error.error.non_field_errors) {
                            this.state = error.error.non_field_errors[0];
                        } else {
                            this.state = 'Server didnt accept this login. We sent a report to fix this!';
                            //  TODO log error
                        }
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
