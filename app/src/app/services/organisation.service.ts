import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IAttachments} from '../models/attachments.model';
import {IReceipt} from '../models/receipt.model';
import {environment} from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class OrganisationService {

    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
    }

}
