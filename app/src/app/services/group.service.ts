import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { IGroup, ICreateGroup } from '../models/group.model';
import { IResult } from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class GroupService {
    API_URL = environment.baseUrl;
    URL_GROUP = `${this.API_URL}/group/`;
    URL_GROUP_ADMIN = `${this.API_URL}/group-admin/`;

    constructor(private httpClient: HttpClient) {
    }

    getGroupList() {
        return this.httpClient.get<IGroup[]>(`${this.URL_GROUP}`).toPromise();
    }

    checkGroupName(groupName: string) {
        return this.httpClient.get<IGroup[]>(`${this.URL_GROUP}?name__iexact=${groupName}`);
    }

    createGroup(newGroup: ICreateGroup) {
        return this.httpClient.post<IGroup[]>(`${this.URL_GROUP_ADMIN}`, newGroup).toPromise();
    }

    // addUserToGroup(userId: number, groupId: number) {
    //     return this.httpClient.post<IResult<IGroup>>(this.URL_GROUP, {
    //         user_id: userId,
    //         group_id: groupId
    //     }).toPromise();
    // }
}
