// src/app/auth/token.interceptor.ts
import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {AuthService} from '../auth.service';
import {Observable} from 'rxjs';
import {switchMap} from 'rxjs/operators';
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

            if (!this.authService.authRefreshSubject == null) {
                // The subject is waiting completion
                this.authService.authRefreshSubject.subscribe(result => {
                    console.log('asyncSubject complete:', result);
                });
            } else {
                return this.authService
                    .attemptRefreshAuth()
                    .pipe(
                        switchMap(result => {
                            if (!result) {
                                console.log('not result', result);
                                this.authService.logoutAndReturn();
                                return next.handle(request);
                            } else {
                                this.snackBarService.openSnackBar('Had to refresh your login.', 'Thx fam');
                                return this.cloneBearerRequest(request, next);
                            }
                        })
                    );
            }
        }

        return this.cloneBearerRequest(request, next);
    }

    private cloneBearerRequest(request, next): Observable<HttpEvent<any>> {
        request = request.clone({
            setHeaders: {
                Authorization: `Bearer ${this.authService.getToken()}`
            }
        });
        return next.handle(request);
    }
}
