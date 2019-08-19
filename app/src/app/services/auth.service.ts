import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {JwtHelperService} from '@auth0/angular-jwt';
import {tap} from 'rxjs/operators';
import {Router} from '@angular/router';
import {ITokenClaims} from '../models/auth.model';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    API_URL: string = environment.baseUrl;
    jwtHelper: JwtHelperService = new JwtHelperService();

    constructor(private  httpClient: HttpClient, private router: Router) {
    }

    public isAuthenticated(): boolean {
        const token = localStorage.getItem('token');
        if (token === null) {
            return false;
        }

        if (environment.debug) {
            this.validateAuth(token).subscribe(result => {
                console.log('%c[Auth]/debug=true: %ctoken marked and verified as valid!', 'color: green', 'color: blue');
            }, error => {
                console.log('Token didnt validate...', error);
                this.logout();
                this.router.navigateByUrl('/login');
            });
        }

        // TODO consider checking with server
        return !(this.jwtHelper.isTokenExpired(token));
    }

    public getToken() {
        return localStorage.getItem('token');
    }

    public getTokenClaims(): ITokenClaims | any {
        const token = localStorage.getItem('token');
        if (token != null) {
            const tokenClaims: ITokenClaims = this.jwtHelper.decodeToken(token);
            tokenClaims.user_id = +tokenClaims.user_id;
            return tokenClaims;
        }
        return {
            user_id: null
        };
    }

    public sendAuth(usernameOrEmail: string, password: string) {
        return this.httpClient.post<any>(`${this.API_URL}/auth-jwt/`, {
            'username-or-email': usernameOrEmail, password
        }).pipe(
            tap(result => localStorage.setItem('token', result.token.toString()),
                e => {
                    // Bad auth credentials?
                    if (environment.debug) {
                        // TODO log this somewhere
                        console.log('[Auth service] Error', e);
                    }
                })
        );
    }

    public validateAuth(token: string) {
        return this.httpClient.post(`${this.API_URL}/auth-jwt-verify/`, {token});
    }

    public loginHouse() {
        if (this.isAuthenticated()) {
            return this.httpClient.post<any>(`${this.API_URL}/auth-house/`, null)
                .pipe(
                    tap(result => {
                        localStorage.setItem('token', result.token.toString());
                        window.location.href = window.location.href;
                    })
                )
                .toPromise();
        } else {
            return null;
        }
    }

    public logout() {
        localStorage.removeItem('token');
    }
}
