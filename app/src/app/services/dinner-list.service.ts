import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class DinnerListService {
    API_URL = environment.baseUrl;
    URL_BASE = `${this.API_URL}/dinner/`;

    constructor(private  httpClient: HttpClient) {
        console.log(this.URL_BASE);
    }

    getDinnerList() {
        return this.httpClient.get<IDinnerDate[]>(`${this.URL_BASE}`);
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
