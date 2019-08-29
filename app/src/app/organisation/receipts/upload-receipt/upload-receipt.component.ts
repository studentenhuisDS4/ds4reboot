import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../../models/attachments.model';
import {IReceipt} from '../../../models/receipt.model';
import {ReceiptService} from '../../../services/receipt.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {emailValidator} from '../../../services/validators/async.validator';

@Component({
    selector: 'app-upload-receipt',
    templateUrl: './upload-receipt.component.html',
    styleUrls: ['./upload-receipt.component.scss']
})
export class UploadReceiptComponent implements OnInit {
    receiptAttachments: File[];
    receipt: IReceipt;

    uploadReceiptForm = new FormGroup({
        email: new FormControl(null,
            {
                validators: [Validators.pattern('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[a-z]{2,4}$')],
            }),
    });

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

    public V(control: string) {
        return this.uploadReceiptForm.get(control).value;
    }

    public E(control: string) {
        return this.uploadReceiptForm.controls[control].errors;
    }

    public C(control: string) {
        return this.uploadReceiptForm.controls[control];
    }

}
