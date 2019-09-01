import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {IAttachments} from '../models/attachments.model';
import {IReceipt} from '../models/receipt.model';
import {environment} from '../../environments/environment';
import {map} from 'rxjs/operators';
import {IResult} from '../models/api.model';

@Injectable({
    providedIn: 'root'
})
export class ReceiptService {

    API_URL: string = environment.baseUrl;

    constructor(private  httpClient: HttpClient) {
    }

    uploadReceipt(upload: IAttachments<IReceipt>) {
        const formData: FormData = new FormData();
        Array.from(upload.attachments).forEach((a, b) => {
            console.log(a, b);
            formData.append('attachment', a, a.name);
        });
        if (upload.json_object) {
            formData.append('json_data', JSON.stringify(upload.json_object));
        } else {
            return Promise.reject(new Error('The receipts was empty.'));
        }
        return this.httpClient.put(`${this.API_URL}/receipt/`, formData).toPromise();
    }

    getReceipt(receiptId): Promise<IReceipt> {
        return this.httpClient.get<IReceipt[]>(`${this.API_URL}/receipt/?id=${receiptId.toString()}`)
            .pipe(
                map(result => result[0])
            ).toPromise();
    }

    getReceipts(user = null): Promise<IReceipt[]> {
        if (user) {
            return this.httpClient.get<IReceipt[]>(`${this.API_URL}/receipt/?upload_user_id${user.id}`).toPromise();
        } else {
            return this.httpClient.get<IReceipt[]>(`${this.API_URL}/receipt/`).toPromise();
        }
    }

    deleteReceipt(receipt: IReceipt) {
        return this.httpClient.delete<any>(`${this.API_URL}/receipt/${receipt.id}`).toPromise();
    }

    acceptReceipt(receipt: IReceipt) {
        return this.httpClient.post<IResult<IReceipt>>(`${this.API_URL}/receipt/${receipt.id}/accept/`, {}).toPromise();
    }

    unacceptReceipt(receipt: IReceipt) {
        return this.httpClient.post<IResult<IReceipt>>(`${this.API_URL}/receipt/${receipt.id}/unaccept/`, {}).toPromise();
    }
}
