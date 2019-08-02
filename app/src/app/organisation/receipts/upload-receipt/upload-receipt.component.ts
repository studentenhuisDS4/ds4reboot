import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../../models/attachments.model';
import {IReceipt} from '../../../models/receipt.model';
import {ReceiptService} from '../../../services/receipt.service';

@Component({
    selector: 'app-upload-receipt',
    templateUrl: './upload-receipt.component.html',
    styleUrls: ['./upload-receipt.component.scss']
})
export class UploadReceiptComponent implements OnInit {
    receiptAttachments: File[];
    receipt: IReceipt;

    constructor(private receiptService: ReceiptService) {
    }

    submitImage(files) {
        const upload: IAttachments<IReceipt> = {
            attachments: this.receiptAttachments,
            json_object: this.receipt,
        };
        this.receiptService.uploadReceipt(upload).then(
            data => {
                files = [];
            },
            error => {
                console.log(error);
                alert(error);
            }
        );
    }

    handleFileInput(files) {
        this.receiptAttachments = files;
    }

    ngOnInit() {
    }

}
