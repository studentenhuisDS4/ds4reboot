import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {JwtHelperService} from '@auth0/angular-jwt';
import {tap} from 'rxjs/operators';
import {Router} from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    API_URL: string = environment.baseUrl;

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
        return !(new JwtHelperService().isTokenExpired(token));
    }

    public getToken() {
        return localStorage.getItem('token');
    }

    public sendAuth(username: string, password: string) {
        return this.httpClient.post<any>(`${this.API_URL}/auth-jwt/`, {
            username, password
        }).pipe(
            tap(result => localStorage.setItem('token', result.token.toString()),
                e => {
                    // Bad auth credentials?
                    if (environment.debug) {
                        // TODO log this somewhere
                        console.log('[Auth service] Error', e.toString());
                    }
                })
        );
    }

    public validateAuth(token: string) {
        return this.httpClient.post(`${this.API_URL}/auth-jwt-verify/`, {token});
    }

    public logout() {
        localStorage.removeItem('token');
    }
}
