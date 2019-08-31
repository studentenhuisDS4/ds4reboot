import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../../models/attachments.model';
import {IReceipt} from '../../../models/receipt.model';
import {ReceiptService} from '../../../services/receipt.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {FileValidator} from 'ngx-material-file-input';

@Component({
    selector: 'app-upload-receipt',
    templateUrl: './upload-receipt.component.html',
    styleUrls: ['./upload-receipt.component.scss']
})
export class UploadReceiptComponent implements OnInit {
    readonly maxAttachmentSize = 50 * 2 ** 20;

    uploadReceiptForm = new FormGroup({
        receipt_title: new FormControl(null,
            {
                validators: [Validators.maxLength(100), Validators.required],
            }),
        receipt_description: new FormControl(null,
            {
                validators: [Validators.maxLength(300)],
            }),
        receipt_cost: new FormControl(null,
            {
                validators: [Validators.required],
            },
        ),
        share_cost_method: new FormControl({value: 1}),
        attachment: new FormControl(null,
            {
                validators: [Validators.required, FileValidator.maxContentSize(this.maxAttachmentSize)]
            })
    });

    constructor(private receiptService: ReceiptService) {
        this.uploadReceiptForm.valueChanges.subscribe((result) => {

        });
    }

    submitReceipt() {
        if (this.uploadReceiptForm.valid) {
            const receipt = this.uploadReceiptForm.value;
            delete receipt.attachment;
            const attachments = this.V('attachment')._files;

            const upload: IAttachments<IReceipt> = {
                attachments,
                json_object: receipt,
            };
            this.receiptService.uploadReceipt(upload).then(
                data => {
                    this.C('attachment').reset();
                },
                error => {
                    console.log(error);
                    alert(error);
                }
            );
        } else {
            this.uploadReceiptForm.markAllAsTouched();
        }
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
