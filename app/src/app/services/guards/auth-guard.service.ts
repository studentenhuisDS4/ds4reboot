import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { SnackBarService } from '../snackBar.service';
import { UserService } from '../user.service';

declare var ClientIP: string;

@Injectable()
export class AuthGuardService implements CanActivate {
    constructor(
        public auth: AuthService,
        public router: Router,
        private snackBar: SnackBarService,
        private userService: UserService
    ) {
    }

    canActivate(): boolean {
        if (ClientIP === '10.0.4.123' && this.auth.isAuthTokenValid() && !this.userService.checkHouse(null)) {
            console.log('GR PC detected and login on personal account.');
            this.snackBar.openSnackBar('Logging into house account after 30 seconds...', 'Noice');

            setTimeout(() => {
                this.auth.loginHouse();
                this.snackBar.openSnackBar('Logging into house account now...', 'Noice');
            }, 30000);
        }

        if (!this.auth.isAuthTokenValid()) {
            return false;
        }
        return true;
    }
}
