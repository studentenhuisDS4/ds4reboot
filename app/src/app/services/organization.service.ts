import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class OrganizationService {

    constructor(private  httpClient: HttpClient) {
    }
}
