import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IProfile} from '../models/profile.model';
import {AuthService} from './auth.service';

@Injectable({
    providedIn: 'root'
})
export class ProfileService {

    API_URL: string = environment.baseUrl;

    constructor(private httpClient: HttpClient, private auth: AuthService) {
    }

    // Jwt-claim based profile getter (guaranteed by guard)
    getProfile(user: number = this.auth.getTokenClaims().user_id) {
        return this.httpClient.get<IProfile>(`${this.API_URL}/profile/${user.toString()}/`, {}).toPromise();
    }

    // Jwt-claim based user-id getter (guaranteed by guard)
    getUserId(): number {
        return this.auth.getTokenClaims().user_id;
    }

}
