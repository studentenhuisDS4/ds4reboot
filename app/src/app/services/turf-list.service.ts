import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ITurfItem} from '../models/turf.model';
import {IHousemate} from '../models/profile.model';
import {IResult} from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class TurfListService {

    API_URL = environment.baseUrl;
    URL_TURF = `${this.API_URL}/turf/turf_item/`;

    constructor(private  httpClient: HttpClient) {
    }

    turfItem(turfItemData: ITurfItem) {
        return this.httpClient.post<IResult<IHousemate>>(`${this.URL_TURF}`, turfItemData).toPromise();
    }

    getTurfDay() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getTurfWeek() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getTurfList() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getBoeteHR() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getBoeteOpen() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

}
