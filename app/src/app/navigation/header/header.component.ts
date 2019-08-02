import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {Router} from '@angular/router';
import {SnackBarService} from '../../services/snackBar.service';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

    @Output() public sidenavToggle = new EventEmitter();

    constructor(
        private authService: AuthService,
        private router: Router,
        private snackbarService:SnackBarService
    ) {
    }

    ngOnInit() {
    }

    onToggleSidenav() {
        this.sidenavToggle.emit();
    }

    loginHouse() {
        this.authService.loginHouse().then(
            r => {
                this.router.navigateByUrl('/home');
            }
        );
    }

    logout() {
        this.authService.logout();
        return this.router.navigateByUrl('login');
    }

}
