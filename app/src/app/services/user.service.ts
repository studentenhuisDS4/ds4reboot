import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { IUser } from '../models/user.model';
import { GROUP, IGroup } from '../models/group.model';

import { AuthService } from './auth.service';
import { FormGroup } from '@angular/forms';
import { map, tap } from 'rxjs/operators';
import { ITokenClaims } from '../models/auth.model';
import { of } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class UserService {
    user: IUser;
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

    isThesau(userId: number = this.auth.getTokenClaims().user_id): Promise<boolean> {
        if (userId !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user/${userId.toString()}/`, {})
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

    findThesauGroup(groups: IGroup[]) {
        return groups.find(group => group.id === GROUP.THESAU);
    }

    getHouseProfile(userId: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (userId === 2 && userId) {
            return this.httpClient.get<IUser>(`${this.API_URL}/house/${userId.toString()}/`, {}).toPromise();
        }
        return Promise.resolve(null);
    }

    // Jwt-claim based profile getter (guaranteed by guard)
    getProfile(userId: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (this.user && userId === this.user.id) {
            return Promise.resolve(this.user);
        }
        if (userId !== 2 && userId) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user/${userId.toString()}/`, {})
                .pipe(
                    tap(result => {
                        this.user = result;
                    })
                ).toPromise();
        }
        return Promise.resolve(null);
    }

    getFullProfile(userId: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (userId !== 2 && userId) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user-full/${userId.toString()}/`, {})
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

    checkEmail(email: string, userId: number = this.auth.getTokenClaims().user_id) {
        if (email !== '') {
            return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?email__iexact=${email}`).pipe(
                map(result => {
                    if (userId != null) {
                        return result.filter(user => user.id === userId);
                    }
                    return result;
                })
            );
        } else {
            return of([]);
        }
    }

    createUser(userForm: FormGroup) {
        return this.httpClient.post<IUser>(`${this.API_URL}/user-full/`, userForm.value).toPromise();
    }

    updateProfile(userForm: FormGroup) {
        const user_id = this.auth.getTokenClaims().user_id;
        if (user_id !== 2) {
            const data = this.purgeForm(userForm);
            return this.httpClient.patch<IUser>(`${this.API_URL}/user/${user_id}/`, data).toPromise();
        } else {
            return Promise.reject();
        }
    }

    updateUserFull(userForm: FormGroup, userId: number) {
        if (userId && userId !== 2) {
            const data = this.purgeForm(userForm);
            return this.httpClient.patch<IUser>(`${this.API_URL}/user-full/${userId}/`, data).toPromise();
        }
    }

    private purgeForm(form: FormGroup) {
        const data = { ...form.value };
        if (data.password === '') {
            delete data.password;
            delete data.password_repeat;
        }
        this.clean(data);
        return data;
    }

    private clean(obj) {
        for (const propName in obj) {
            if (obj[propName] === null || obj[propName] === undefined) {
                delete obj[propName];
            }
        }
    }

}
