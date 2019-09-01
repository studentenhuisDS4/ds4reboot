import {IHousemate, IUser} from './user.model';

export interface IUserDinner {
    id: number;

    user: IUser;
    housemate: IHousemate;
    dinner_date: Date;
    count: number;
    is_cook: boolean;
    split_cost: number;
}

export interface IDinner {
    id: number;
    num_eating: number;
    userdinners: IUserDinner[];
    cost: number;
    open: boolean;
    date: Date;

    cook: IUser;

    signup_time: Date;
    close_time: Date;
    eta_time: Date;
}

export function userEntry(dinner: IDinner, user: IUser): IUserDinner {
    if (dinner && dinner.userdinners && user) {
        return dinner.userdinners.find(ud => ud.user.id === user.id);
    }
    return null;
}

export const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export const dayNamesShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function weekDates(current) {
    const week = [];

    if (current.getDay() === 0) {
        current.setDate((current.getDate() - 6));
    } else {
        current.setDate((current.getDate() - current.getDay() + 1));
    }
    for (let i = 1; i < 8; i++) {
        week.push(
            new Date(current)
        );
        current.setDate(current.getDate() + 1);
    }
    return week;
}

export function convertStringToDate(date: string) {
    return (new Date(date)).getDay();
}

