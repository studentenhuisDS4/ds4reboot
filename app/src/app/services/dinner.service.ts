import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IDinner} from '../models/dinner.models';
import {Time} from '@angular/common';
import {IResult} from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class DinnerService {
    API_URL = environment.baseUrl;
    URL_WEEK = `${this.API_URL}/dinnerweek/`;
    URL_SIGNUP = `${this.API_URL}/userdinner/signup/`;
    URL_SIGNOFF = `${this.API_URL}/userdinner/signoff/`;
    URL_COOK = `${this.API_URL}/userdinner/cook/`;

    URL_CLOSE = `${this.API_URL}/dinner/{ID}/close/`;
    URL_COST = `${this.API_URL}/dinner/{ID}/cost/`;
    URL_ETA_TIME = `${this.API_URL}/dinner/{ID}/close/`;


    constructor(private  httpClient: HttpClient) {
    }

    getDinnerWeek() {
        return this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    signUp(userId: number, dinnerDate: Date) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_SIGNUP, {
            user_id: userId,
            dinner_date: dinnerDate
        }).toPromise();
    }

    signOff(userId: number, dinnerDate: Date) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_SIGNOFF, {
            user_id: userId,
            dinner_date: dinnerDate
        }).toPromise();
    }

    cook(userId: number, dinnerDate: Date, signOff: boolean = false) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_COOK, {
            user_id: userId,
            dinner_date: dinnerDate,
            sign_off: signOff // if user wants to explicitly sign off instead of invert
        }).toPromise();
    }

    // The following dont require user_id, because login supplies that information
    close(dinner: IDinner) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_CLOSE.replace('{ID}', dinner.id.toString()), {}).toPromise();
    }

    cost(dinner: IDinner, dinnerCost: number) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_COST.replace('{ID}', dinner.id.toString()), {
            cost: dinnerCost
        }).toPromise();
    }

    eta_time(dinner: IDinner, etaTime: Time) {
        return this.httpClient.post<IResult<IDinner>>(this.URL_ETA_TIME.replace('{ID}', dinner.id.toString()), {
            eta_time: etaTime
        }).toPromise();
    }
}
