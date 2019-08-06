import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {UserService} from '../../services/user.service';
import {GROUP} from '../../models/user.model';

@Component({
    selector: 'app-sidenav-list',
    templateUrl: './sidenav-list.component.html',
    styleUrls: ['./sidenav-list.component.scss']
})
export class SidenavListComponent implements OnInit {
    @Output() sidenavClose = new EventEmitter();
    isAdmin = false;
    isThesau = false;

    constructor(
        private userService: UserService
    ) {
    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            this.isAdmin = result.is_superuser;
            const thesauGroup = result.groups.find(g => g.id === GROUP.THESAU);
            this.isThesau = thesauGroup != null;
        });
    }

    public onSidenavClose = () => {
        this.sidenavClose.emit();
    };

}
