import {Component, Input, OnInit} from '@angular/core';
import {TurfListService} from '../services/turf-list.service';
import {TurfType} from '../models/turf.model';
import {UserService} from '../services/user.service';
import {HOUSE_ID, IUser} from '../models/user.model';
import {IStatus} from '../models/api.model';
import {SnackBarService} from '../services/snackBar.service';
import {EasterEggService} from '../services/easter.service';

@Component({
    selector: 'app-turf-list',
    templateUrl: './turf-list.component.html',
    styleUrls: ['./turf-list.component.scss']
})
export class TurfListComponent implements OnInit {

    @Input() miniView = false;

    constructor() {

    }

    ngOnInit() { }

}
