import {Component, OnInit} from '@angular/core';
import {OrganisationService} from '../../services/organisation.service';
import {ICalendarEvent} from '../../models/calendar.model';

@Component({
    selector: 'app-calendar',
    templateUrl: './calendar.component.html',
    styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit {

    calendarEvents: ICalendarEvent[];

    constructor(
        private organisationService: OrganisationService
    ) {
    }

    ngOnInit() {
        this.organisationService.getEvents().then(response => {
            this.calendarEvents = response;
        });
    }

}
