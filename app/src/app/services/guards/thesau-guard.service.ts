import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {UserService} from '../user.service';
import {SnackBarService} from '../snackBar.service';

@Injectable()
export class ThesauGuardService implements CanActivate {
    constructor(
        public userService: UserService,
        public router: Router,
        private snackBar: SnackBarService
    ) {
    }

    canActivate(): Promise<boolean> {
        return this.userService.isThesau().then(result => {
            if (!result) {
                this.snackBar.openSnackBar('You\'re no thesau.', 'Jeez');
                this.router.navigate(['home']);
            }
            return result;
        }, error => {
            this.snackBar.openSnackBar('An error occurred. Lets hope someone finds out: ' + error.toString(), 'Jeez');
            this.router.navigate(['home']);
            return false;
        });
    }
}
