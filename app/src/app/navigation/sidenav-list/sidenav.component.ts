import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {UserService} from '../../services/user.service';
import {GROUP} from '../../models/user.model';
import {MatSidenav} from '@angular/material';

@Component({
    selector: 'app-sidenav-list',
    templateUrl: './sidenav.component.html',
    styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent implements OnInit {
    @Output() sidenavClose = new EventEmitter();
    isAdmin = false;
    isThesau = false;
    loggedIn = false;

    constructor(
        private userService: UserService
    ) {
    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            if (result) {
                this.isAdmin = result.is_superuser;
                const thesauGroup = result.groups.find(g => g.id === GROUP.THESAU);
                this.isThesau = thesauGroup != null;

                this.loggedIn = true;
            }
        });
    }

    public onSidenavClose = () => {
        this.sidenavClose.emit();
    }

}
