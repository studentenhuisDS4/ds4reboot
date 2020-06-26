import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {JwtHelperService} from '@auth0/angular-jwt';
import {mergeMap, tap} from 'rxjs/operators';
import {Router} from '@angular/router';
import {ITokenClaims} from '../models/auth.model';
import {of} from 'rxjs';

const REFRESH_TOKEN = 'refresh';
const AUTH_TOKEN = 'token';

interface IRefreshResponse {
    access: string;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    API_URL: string = environment.baseUrl;
    API_LOGIN_URL = `${this.API_URL}/auth-jwt/`;
    API_REFRESH_URL = `${this.API_URL}/auth-jwt-refresh/`;
    jwtHelper: JwtHelperService = new JwtHelperService();

    constructor(private httpClient: HttpClient, private router: Router) {
    }

    public getToken() {
        // Used by JWT interceptor, so public
        return localStorage.getItem(AUTH_TOKEN);
    }

    public setAuthToken(token: string) {
        // Used by JWT interceptor, so public
        return localStorage.setItem(AUTH_TOKEN, token);
    }

    public getRefreshToken() {
        return localStorage.getItem(REFRESH_TOKEN);
    }

    // Sending verification is technically best, but not required if we can validate the token beforehand
    // public sendVerifyAuth(token: string) {
    //
    //     // Checking the token for expiry is quite sufficient
    //     if (environment.debug) {
    //         console.log('Verifying token:', token);
    //     }
    //     return this.httpClient.post(`${this.API_URL}/auth-jwt-verify/`, {token});
    // }

    public attemptRefreshAuth() {
        if (this.isAuthRefreshTokenValid()) {
            return this.httpClient.post<IRefreshResponse>(this.API_REFRESH_URL, {
                [REFRESH_TOKEN]: this.getRefreshToken()
            }).pipe(
                mergeMap(result => {
                    if (result && this.isAuthTokenValid(result?.access)) {
                        this.setAuthToken(result.access);
                    } else {
                        throw Error('Refresh token was rejected, or something went wrong with it.');
                    }
                    return of(result);
                })
            );
        } else {
            console.log('refresh invalid');
            return of(null);
        }
    }

    public getTokenClaims(): ITokenClaims | any {
        const token = this.getToken();
        if (token != null) {
            try {
                const tokenClaims: ITokenClaims = this.jwtHelper.decodeToken(token);
                tokenClaims.user_id = +tokenClaims.user_id;
                return tokenClaims;
            } catch {
                console.log('Json decoding error occurred: probably malformed');
                return {
                    user_id: null
                };
            }
        }
        return {
            user_id: null
        };
    }

    public sendLogin(usernameOrEmail: string, password: string) {
        return this.httpClient.post<any>(this.API_LOGIN_URL, {
            'username-or-email': usernameOrEmail, password
        }).pipe(
            tap(result => {
                    localStorage.setItem(AUTH_TOKEN, result.token.toString());
                    localStorage.setItem(REFRESH_TOKEN, result.refresh.toString());
                },
                e => {
                    // Bad auth credentials?
                    if (environment.debug) {
                        // TODO log this somewhere
                        console.log('[Auth service] Error', e);
                    }
                })
        );
    }

    public loginHouse() {
        if (this.isAuthTokenValid()) {
            return this.httpClient.post<any>(`${this.API_URL}/auth-house/`, null)
                .pipe(
                    tap(result => {
                        localStorage.setItem(AUTH_TOKEN, result.token.toString());
                        window.location.href = window.location.href;
                    })
                )
                .toPromise();
        } else {
            return null;
        }
    }

    public logoutAndReturn() {
        localStorage.removeItem(AUTH_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        this.router.navigate(['login']);
    }

    public isAuthTokenUnset(): boolean {
        return this.getToken() == null;
    }

    public isAuthTokenValid(providedString = null): boolean {
        if (providedString) {
            return !(this.jwtHelper.isTokenExpired(providedString));
        }
        const token = this.getToken();
        if (token === null) {
            return false;
        }
        return !(this.jwtHelper.isTokenExpired(token));
    }

    public isAuthRefreshTokenValid(): boolean {
        const token = localStorage.getItem(REFRESH_TOKEN);
        if (token === null) {
            return false;
        }
        return !(this.jwtHelper.isTokenExpired(token));
    }
}
