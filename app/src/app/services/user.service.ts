import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IUser} from '../models/user.model';
import {AuthService} from './auth.service';
import {FormGroup} from '@angular/forms';
import {map} from 'rxjs/operators';
import {ITokenClaims} from '../models/auth.model';

@Injectable({
    providedIn: 'root'
})
export class UserService {

    API_URL: string = environment.baseUrl;

    constructor(
        private httpClient: HttpClient,
        private auth: AuthService) {
    }

    checkHouse(token: ITokenClaims = this.auth.getTokenClaims()) {
        if (token) {
            return token.user_id === 2;
        }
        return false;
    }

    isThesau(user: number = this.auth.getTokenClaims().user_id): Promise<boolean> {
        if (user !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user/${user.toString()}/`, {})
                .pipe(
                    map(r => {
                        let isThesau = false;
                        r.groups.forEach(g => {
                            if (g.name === 'thesau') {
                                isThesau = true;
                            }
                        });
                        return isThesau;
                    })
                )
                .toPromise();
        }
        return Promise.resolve(null);
    }


    getHouseProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user === 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/house/${user.toString()}/`, {}).toPromise();
        }
        return Promise.resolve(null);
    }

    // Jwt-claim based profile getter (guaranteed by guard)
    getProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user/${user.toString()}/`, {}).toPromise();
        }
        return Promise.resolve(null);
    }

    getFullProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user-full/${user.toString()}/`, {})
                .toPromise();
        }
        return Promise.resolve(null);
    }

    getActiveUsers(): Promise<IUser[]> {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/`, {})
            .toPromise();
    }

    checkUsername(username: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?username__iexact=${username}`);
    }

    checkEmail(email: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?email__iexact=${email}`);
    }

    createUser(userForm: FormGroup) {
        return this.httpClient.post<IUser>(`${this.API_URL}/user-full/`, userForm.value).toPromise();
    }

    updateProfile(userForm: FormGroup) {
        const user_id = this.auth.getTokenClaims().user_id;
        if (user_id !== 2) {
            const data = this.purgePassword(userForm);
            return this.httpClient.patch<IUser>(`${this.API_URL}/user/${user_id}/`, data).toPromise();
        } else {
            return Promise.reject();
        }
    }

    updateUserFull(userForm: FormGroup, user: number = this.auth.getTokenClaims().user_id) {
        const data = this.purgePassword(userForm);
        return this.httpClient.post<IUser>(`${this.API_URL}/user-full/${user}/`, data).toPromise();
    }

    private purgePassword(form: FormGroup) {
        const data = {...form.value};
        if (data.password === '') {
            delete data.password;
            delete data.password_repeat;
        }
        return data;
    }
}
