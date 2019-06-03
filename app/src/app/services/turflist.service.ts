import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class TurflistService {

    constructor(private  httpClient: HttpClient) {
    }
}
