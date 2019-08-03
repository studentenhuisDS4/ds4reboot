import {Component, OnInit} from '@angular/core';
import {IUser} from '../../models/user.model';
import {UserService} from '../../services/user.service';

@Component({
    selector: 'app-user-manage',
    templateUrl: './user-manage.component.html',
    styleUrls: ['./user-manage.component.scss']
})
export class UserManageComponent implements OnInit {
    user: IUser;

    constructor(private userService: UserService) {

    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            this.user = result;
        });

    }

}
