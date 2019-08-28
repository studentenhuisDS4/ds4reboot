import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ITurfItem, ITurfLogAggregation, ITurfLogEntry, TurfLogFilter} from '../models/turf.model';
import {IHousemate} from '../models/user.model';
import {IPagination, IResult} from '../models/api.model';
import {IPage} from '../models/page.model';

@Injectable({
    providedIn: 'root'
})
export class TurfService {

    API_URL = environment.baseUrl;
    URL_TURF = `${this.API_URL}/turf/turf_item/`;
    URL_LOG = `${this.API_URL}/turf/`;

    constructor(private  httpClient: HttpClient) {
    }

    turfItem(turfItemData: ITurfItem) {
        return this.httpClient.post<IResult<IHousemate>>(`${this.URL_TURF}`, turfItemData).toPromise();
    }

    getTurfLog(filter: TurfLogFilter, aggregation: ITurfLogAggregation, page: IPage) {
        const offset = page.index * page.size;
        const limit = page.size;

        const query = `${this.URL_LOG}${filter.serialize()}&offset=${offset}&limit=${limit}`;
        return this.httpClient.get<IPagination<ITurfLogEntry[]>>(query);
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
}
