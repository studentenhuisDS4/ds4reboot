import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IUser} from '../models/user.model';
import {environment} from '../../environments/environment';
import {IMoveout} from '../models/admin.model';
import {IResult} from '../models/api.model';
import {FormGroup} from '@angular/forms';

@Injectable({
    providedIn: 'root'
})
export class AdminService {
    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
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
}
