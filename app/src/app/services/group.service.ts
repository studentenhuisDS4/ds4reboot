import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ICreateGroup, IGroup} from '../models/group.model';

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

    createGroup(newGroup: ICreateGroup): Promise<IGroup[]> {
        return this.httpClient.post<IGroup[]>(`${this.URL_GROUP_ADMIN}`, newGroup).toPromise();
    }

    updateGroup(group: IGroup): Promise<IGroup> {
        return this.httpClient.put<IGroup>(`${this.URL_GROUP_ADMIN}${group.id}/`, group).toPromise();
    }

    // addUserToGroup(userId: number, groupId: number) {
    //     return this.httpClient.post<IResult<IGroup>>(this.URL_GROUP, {
    //         user_id: userId,
    //         group_id: groupId
    //     }).toPromise();
    // }
    deleteGroup(group: IGroup) {
        return this.httpClient.delete<IGroup>(`${this.URL_GROUP_ADMIN}${group.id}`).toPromise();
    }
}
