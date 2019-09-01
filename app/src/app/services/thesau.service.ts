import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IUser} from '../models/user.model';
import {environment} from '../../environments/environment';
import {IResult} from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class ThesauService {
    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
    }

    getBillableUsers(): Promise<IResult<IUser[]>> {
        return this.httpClient.get<IResult<IUser[]>>(`${this.API_URL}/user-full/hr_active/`, {})
            .toPromise();
    }

    getAllUsers(oldUsers: boolean): Promise<IUser[]> {
        if (oldUsers) {
            return this.httpClient.get<IUser[]>(`${this.API_URL}/user-full/`, {})
                .toPromise();
        } else {
            return this.httpClient.get<IUser[]>(`${this.API_URL}/user-full/?housemate__moveout_set!=true`, {})
                .toPromise();
        }

    }
}
