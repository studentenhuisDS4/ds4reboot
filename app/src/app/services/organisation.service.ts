import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {ICalendarEvent} from '../models/calendar.model';
import {IResult} from '../models/api.model';
import {map} from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class OrganisationService {

    API_URL: string = environment.baseUrl;

    constructor(
        private httpClient: HttpClient,
    ) {
    }

    getEvents(): Promise<ICalendarEvent[]> {
        return this.httpClient.get<IResult<ICalendarEvent[]>>(`${this.API_URL}/calendar/`)
            .pipe(
                map(response => response.result)
            ).toPromise();
    }


}
