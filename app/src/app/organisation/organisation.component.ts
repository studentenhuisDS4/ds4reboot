import {Component, OnInit} from '@angular/core';
import {OrganisationService} from '../services/organisation.service';
import {IAttachments} from '../models/attachments.model';
import {IReceipt} from '../models/receipt.model';

@Component({
    selector: 'app-organization',
    templateUrl: './organisation.component.html',
    styleUrls: ['./organisation.component.scss']
})
export class OrganisationComponent implements OnInit {
    constructor(private organisationService: OrganisationService) {
    }

    ngOnInit() {
    }

}
