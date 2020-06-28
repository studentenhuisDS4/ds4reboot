import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {UserService} from '../services/user.service';
import {AuthService} from '../services/auth.service';
import {SnackBarService} from '../services/snackBar.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
    public loginForm: FormGroup;
    awaitingLogin = false;
    signInMessage = '';

    constructor(
        private http: HttpClient,
        private router: Router,
        private userService: UserService,
        private authService: AuthService,
        private snackbar: SnackBarService,
    ) {
    }

    ngOnInit() {
        // Show loader while waiting for authService?
        if (this.authService.isAuthTokenValid()) {
            this.router.navigate(['/home']);
        }

        this.loginForm = new FormGroup({
            'username-or-email': new FormControl('', [
                Validators.required,
                Validators.minLength(3),
            ]),
            password: new FormControl('', [
                Validators.required,
                Validators.minLength(3),
            ])
        });
    }

    signIn() {
        this.awaitingLogin = true;
        this.signInMessage = '';
        if (this.loginForm.valid) {
            this.authService.sendLogin(this.V('username-or-email'), this.V('password'))
                .subscribe(res => {
                    this.awaitingLogin = false;
                    this.router.navigateByUrl('/home');
                }, (error: HttpErrorResponse) => {
                    if (error.message.indexOf('Timeout!') > -1) {
                        // Timeout
                        this.snackbar.openSnackBar('Could not connect to server. Please check your internet connection', 'Okay');
                        this.signInMessage = 'Please check your internet connection.';
                    } else if (error.status === 0) {
                        this.signInMessage = 'Couldnt connect. Check your internet connection.';
                    } else {
                        try {
                            this.signInMessage = error.error.detail;
                            this.snackbar.openSnackBar('Error received: ' + error.error.detail, 'Okay');
                        } catch (e) {
                            if (e instanceof TypeError) {
                                this.snackbar.openSnackBar('It seems the server is not responding. Ouch.',
                                    'Okay');
                            }
                        }
                    }
                    this.awaitingLogin = false;
                });
        } else {
            this.awaitingLogin = false;
        }
    }

    public V(control: string) {
        return this.loginForm.get(control).value;
    }

    public E(control: string) {
        return this.loginForm.controls[control].errors;
    }

    public C(control: string) {
        return this.loginForm.controls[control];
    }
}
