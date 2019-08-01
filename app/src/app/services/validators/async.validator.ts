import {map, switchMap, tap} from 'rxjs/operators';
import {FormControl} from '@angular/forms';
import {UserService} from '../user.service';
import {timer} from 'rxjs';

export const usernameValidator =
    (userService: UserService, time: number = 500) => {
        return (input: FormControl) => {
            return timer(time).pipe(
                switchMap(() => userService.checkUsername(input.value)),
                map(res => {
                    return res.length ? {usernameExists: true} : null;
                })
            );
        };
    };

export const emailValidator =
    (userService: UserService, time: number = 500) => {
        return (input: FormControl) => {
            return timer(time).pipe(
                switchMap(() => userService.checkEmail(input.value)),
                map(res => {
                    return res.length ? {emailExists: true} : null;
                })
            );
        };
    };
