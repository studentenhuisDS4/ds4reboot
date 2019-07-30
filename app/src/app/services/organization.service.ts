import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IAttachments} from '../models/attachments.model';
import {IReceipt} from '../models/receipt.model';
import {environment} from '../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class OrganizationService {

    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
    }

    uploadReceipt(upload: IAttachments<IReceipt>) {
        const formData: FormData = new FormData();
        Array.from(upload.attachments).forEach((a, b) => {
            formData.append('attachment', a, a.name);
        });
        if (upload.json_object) {
            formData.append('json_data', JSON.stringify(upload.json_object));
        } else {
            return Promise.reject(new Error('The receipt was empty.'));
        }
        return this.httpClient.put(`${this.API_URL}/receipt/`, formData).toPromise();
    }
}
