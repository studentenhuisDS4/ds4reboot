import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ITurfItem, ITurfResult} from '../models/turf.model';

@Injectable({
    providedIn: 'root'
})
export class TurfListService {

    API_URL = environment.baseUrl;
    URL_TURF = `${this.API_URL}/turf/turf_item/`;

    constructor(private  httpClient: HttpClient) {
    }

    turfItem(turfItemData: ITurfItem) {
        return this.httpClient.post<ITurfResult>(`${this.URL_TURF}`, turfItemData).toPromise();
    }

    getTurfDay() {
        return null; // this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

    getTurfWeek() {
        return null; // this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

    getTurfList() {
        return null; // this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

    getBoeteHR() {
        return null; // this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

    getBoeteOpen() {
        return null; // this.httpClient.get<IDinnerDate[]>(`${this.URL_WEEK}`).toPromise();
    }

}
