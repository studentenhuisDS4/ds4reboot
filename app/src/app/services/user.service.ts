import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IUser} from '../models/profile.model';
import {AuthService} from './auth.service';
import {FormGroup} from '@angular/forms';
import {map} from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class UserService {

    API_URL: string = environment.baseUrl;

    constructor(private httpClient: HttpClient, private auth: AuthService) {
    }

    // Jwt-claim based profile getter (guaranteed by guard)
    getProfile(user: number = this.auth.getTokenClaims().user_id) {
        return this.httpClient.get<IUser>(`${this.API_URL}/user/${user.toString()}/`, {}).toPromise();
    }

    // Jwt-claim based user-id getter (guaranteed by guard)
    getUserId(): number {
        return this.auth.getTokenClaims().user_id;
    }

    checkUsername(username: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?username__iexact=${username}`);
    }

    checkEmail(email: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?email__iexact=${email}`);
    }

    createOrUpdate(userForm: FormGroup) {
        return this.httpClient.post<IUser>(`${this.API_URL}/user-full/`, userForm.value).toPromise();
    }
}
