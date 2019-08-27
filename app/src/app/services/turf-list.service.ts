import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ITurfItem, ITurfLogAggregation, ITurfLogEntry, TurfLogFilter} from '../models/turf.model';
import {IHousemate} from '../models/user.model';
import {IPagination, IResult} from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class TurfListService {

    API_URL = environment.baseUrl;
    URL_TURF = `${this.API_URL}/turf/turf_item/`;
    URL_LOG = `${this.API_URL}/turf/`;

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

    getBoeteHR() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getBoeteOpen() {
        return null; // this.httpClient.get<IDinner[]>(`${this.URL_WEEK}`).toPromise();
    }

    getTurfLog(filter: TurfLogFilter, aggregation: ITurfLogAggregation) {
        return this.httpClient.get<IPagination<ITurfLogEntry[]>>(`${this.URL_LOG}${filter.serialize()}`).toPromise();
    }
}
