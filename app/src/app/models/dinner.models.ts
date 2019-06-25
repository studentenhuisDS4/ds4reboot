export interface IDinnerDate {
    id: number;
    num_eating: number;
    cost: number;
    open: boolean;
    date: string;

    cook: number;

    signup_time: Date;
    close_time: Date;
    eta_time: Date;
}

export const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export const dayNamesShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function weekDates(current) {
    const week = [];

    // Starting Monday not Sunday
    current.setDate((current.getDate() - current.getDay() + 1));
    for (let i = 0; i < 7; i++) {
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

