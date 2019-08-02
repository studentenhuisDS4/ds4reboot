import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../models/attachments.model';
import {IReceipt} from '../../models/receipt.model';
import {OrganisationService} from '../../services/organisation.service';

@Component({
    selector: 'app-receipt',
    templateUrl: './receipts.component.html',
    styleUrls: ['./receipts.component.scss']
})
export class ReceiptsComponent implements OnInit {
    receipts: IReceipt[];

    constructor(private organisationService: OrganisationService) {
    }

    ngOnInit() {
    }



}
