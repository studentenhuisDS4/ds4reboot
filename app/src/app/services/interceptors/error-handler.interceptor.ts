import { ErrorHandler, Injectable } from '@angular/core';
import { SnackBarService } from '../snackBar.service';
import { environment } from '../../../environments/environment';

@Injectable({
    providedIn: 'root',
})
export class GlobalErrorHandler implements ErrorHandler {
    constructor(
        private snackBar: SnackBarService
    ) {
    }

    handleError(error) {
        console.log('Caught error!');
        console.log(error);
        if (error != null) {
            this.snackBar.openSnackBar('Error! ' + error.toString().substring(0, 40), 'Ouch');
        }
        // if (environment.debug) {
        //     throw error;
        // }
    }
}
