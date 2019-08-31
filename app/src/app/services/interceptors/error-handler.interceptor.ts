import {ErrorHandler, Injectable} from '@angular/core';
import {SnackBarService} from '../snackBar.service';
import {environment} from '../../../environments/environment';

@Injectable({
    providedIn: 'root',
})
export class GlobalErrorHandler implements ErrorHandler {
    constructor(
        private snackBar: SnackBarService
    ) {
    }

    handleError(error) {
        console.log('Caught error!', error);
        this.snackBar.openSnackBar('Error! ' + error, 'Ouch');
        if (environment.debug) {
            throw error;
        }
    }
}
