// src/app/auth/token.interceptor.ts
import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {AuthService} from '../auth.service';
import {Observable} from 'rxjs';
import {tap} from 'rxjs/operators';
import {SnackBarService} from '../snackBar.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
    constructor(
        private authService: AuthService,
        private snackBarService: SnackBarService
    ) {
    }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        if (!this.authService.isAuthTokenValid()) {
            if (request.url === this.authService.API_REFRESH_URL || request.url === this.authService.API_LOGIN_URL) {
                return next.handle(request);
            }
            this.authService.attemptRefreshAuth().pipe(
                tap(result => {
                    if (!result) {
                        this.authService.logoutAndReturn();
                    } else {
                        this.snackBarService.openSnackBar('Had to refresh your login.', 'Thx fam');
                    }
                    return next.handle(request);
                }, error => {
                    console.log('Couldnt refresh login.');
                    this.authService.logoutAndReturn();
                    return next.handle(request);
                })
            );
        }

        request = request.clone({
            setHeaders: {
                Authorization: `Bearer ${this.authService.getToken()}`
            }
        });
        return next.handle(request);
    }

}
