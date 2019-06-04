import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {Router} from '@angular/router';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

    @Output() public sidenavToggle = new EventEmitter();

    constructor(private authService: AuthService, private router: Router) {
    }

    ngOnInit() {
    }

    onToggleSidenav() {
        this.sidenavToggle.emit();
    }

    logout() {
        this.authService.logout();
        return this.router.navigateByUrl('login');
    }

}
