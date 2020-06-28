import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { IUser } from '../models/user.model';
import { GROUP } from '../models/group.model';
import { environment } from '../../environments/environment';
import { IActivation, IMoveout } from '../models/admin.model';
import { IResult } from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class AdminService {
    API_URL: string = environment.baseUrl;

    constructor(private httpClient: HttpClient) {
    }

    getAdminUsers(): Promise<IUser[]> {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user-full/?housemate__moveout_set!=true`, {})
            .toPromise();
    }

    deleteUser(user: IUser) {
        if (user && user.id) {
            return this.httpClient.delete<IResult<IMoveout>>(`${this.API_URL}/user-action/${user.id}/moveout/`, {})
                .toPromise();
        }
    }

    toggleUserActivation(user: IUser) {
        if (user && user.id) {
            return this.httpClient.post<IResult<IActivation>>(`${this.API_URL}/user-action/${user.id}/toggle_activation/`, {})
                .toPromise();
        }
    }

    toggleAdmin(adminUser: IUser) {
        if (adminUser && adminUser.id) {
            return this.httpClient.post<IResult<IUser>>(`${this.API_URL}/user-action/${adminUser.id}/toggle_admin/`, {})
                .toPromise();
        }
    }

    toggleThesau(adminUser: IUser) {
        const userGroups = adminUser.groups;
        const index = userGroups.findIndex(g => g.id === GROUP.THESAU);
        if (index !== -1) {
            userGroups.splice(index, 1);
        } else {
            userGroups.push({
                id: GROUP.THESAU,
            });
        }

        if (adminUser && adminUser.id) {
            return this.httpClient.post<IResult<IUser>>(`${this.API_URL}/user-action/${adminUser.id}/set_groups/`,
                userGroups
            ).toPromise();
        }
    }
}
