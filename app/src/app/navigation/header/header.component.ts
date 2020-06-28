import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {Router} from '@angular/router';
import {SnackBarService} from '../../services/snackBar.service';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
    user: IUser;
    isHouse = false;
    @Output() public sidenavToggle = new EventEmitter();

    constructor(
        private authService: AuthService,
        private userService: UserService,
        private router: Router,
        private snackbarService: SnackBarService
    ) {
    }

    ngOnInit() {
        this.isHouse = this.userService.checkHouse(null);
        this.userService.getProfile().then(r => {
                this.user = r;
            }
        );
    }

    onToggleSidenav() {
        this.sidenavToggle.emit();
    }

    loginHouse() {
        if (confirm('This will log you in as house. Continue?')) {
            this.authService.loginHouse().then(
                r => {
                    this.router.navigateByUrl('/home');
                }
            );
            this.userService.getHouseProfile().then(r => {
                    this.user = r;
                }
            );
        }
    }

    logout() {
        this.authService.logoutAndReturn();
        delete this.user;
        return this.router.navigateByUrl('login');
    }

}
