import {Component, OnInit} from '@angular/core';
import {AuthService} from '../services/auth.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

    login: ILogin = {
        username: '',
        password: ''
    };

    constructor(private authService: AuthService) {
    }

    ngOnInit() {
    }

    verifyLogin() {
        this.authService.sendAuth(this.login.username, this.login.password).subscribe((token) => {
            console.log(token);
        }, (error => {
            console.log('error');
        }));
    }
}

interface ILogin {
    username: string;
    password: string;
}
