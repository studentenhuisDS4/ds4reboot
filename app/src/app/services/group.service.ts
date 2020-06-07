import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { IGroup } from '../models/group.model';
import { IResult } from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class GroupService {
    API_URL = environment.baseUrl;
    URL_GROUP = `${this.API_URL}/group/`;

    constructor(private httpClient: HttpClient) {
    }

    getGroupList() {
        return this.httpClient.get<IGroup[]>(`${this.URL_GROUP}`).toPromise();
    }

    // addUserToGroup(userId: number, groupId: number) {
    //     return this.httpClient.post<IResult<IGroup>>(this.URL_GROUP, {
    //         user_id: userId,
    //         group_id: groupId
    //     }).toPromise();
    // }
}
