import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
        console.log(environment.baseUrl);
    }

    public sendAuth(username: string, password: string) {
        return this.httpClient.post(`${this.API_URL}/auth-jwt/`, {
            username, password
        });
    }
}
