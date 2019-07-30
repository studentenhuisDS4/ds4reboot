import {Component, OnInit} from '@angular/core';
import {OrganizationService} from '../services/organization.service';
import {IAttachments} from '../models/attachments.model';
import {IReceipt} from '../models/receipt.model';

@Component({
    selector: 'app-organization',
    templateUrl: './organization.component.html',
    styleUrls: ['./organization.component.scss']
})
export class OrganizationComponent implements OnInit {
    receiptAttachments: File[];
    receipt: IReceipt;

    constructor(private organisationService: OrganizationService) {
    }

    ngOnInit() {
    }

    submitImage(files) {
        const upload: IAttachments<IReceipt> = {
                attachments: this.receiptAttachments,
                json_object: this.receipt,
            };
        this.organisationService.uploadReceipt(upload).then(
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

}
