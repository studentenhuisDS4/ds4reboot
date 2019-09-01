import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {UserService} from './user.service';
import {IReceipt} from '../models/receipt.model';

@Injectable({
    providedIn: 'root'
})
export class OrganisationService {

    API_URL: string = environment.baseUrl;

    constructor(
        private httpClient: HttpClient,
    ) {
    }



}
