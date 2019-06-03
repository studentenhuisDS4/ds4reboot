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

    sendAuth(user: string, password: string) {
        return this.httpClient.get(`${this.API_URL}/contacts`);
    }
}
