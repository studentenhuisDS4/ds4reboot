import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class DinnerListService {
    API_URL = environment.baseUrl;
    URL_WEEK = `${this.API_URL}/dinnerweek/`;

    constructor(private  httpClient: HttpClient) {
        // console.log(this.URL_BASE);
        this.getDinnerWeek().then(result => {
            console.log(result);
        });
    }

    getDinnerWeek() {
        return this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

}

export interface IDinnerDate {
    id: number;
    num_eating: number;
    cost: number;
    open: boolean;
    date: Date;

    signup_time: Date;
    close_time: Date;
}
