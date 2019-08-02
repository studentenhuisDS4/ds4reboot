import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {UserService} from './user.service';
import {SnackBarService} from './snackBar.service';

@Injectable()
export class AdminGuardService implements CanActivate {
    constructor(
        public userService: UserService,
        public router: Router,
        private snackBar: SnackBarService
    ) {
    }

    canActivate(): Promise<boolean> {
        return this.userService.getProfile().then(
            result => {
                if (!result.is_superuser) {
                    this.snackBar.openSnackBar('You\'re no admin of mine.', 'Jeez');
                    this.router.navigate(['home']);
                }
                return result.is_superuser;
            },
        );
    }
}
