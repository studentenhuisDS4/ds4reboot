import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IDinnerDate} from '../models/dinner.models';

@Injectable({
    providedIn: 'root'
})
export class DinnerListService {
    API_URL = environment.baseUrl;
    URL_WEEK = `${this.API_URL}/dinnerweek/`;

    dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    constructor(private  httpClient: HttpClient) {
        // console.log(this.URL_BASE);
    }

    getDinnerWeek() {
        return this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }



}
