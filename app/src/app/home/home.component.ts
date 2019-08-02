import {Component, OnInit} from '@angular/core';
import {UserService} from '../services/user.service';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

    isHouse = false;

    constructor(
        private userService: UserService
    ) {
    }

    ngOnInit() {
        this.isHouse = this.userService.checkHouse();
    }

}
