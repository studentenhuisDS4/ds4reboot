import {IUser} from './user.model';

export interface ITransfer {
    id: number;
    time: Date;
    amount: number;
    note: string;
    user_id: number;
    from_user: IUser;
    to_user: IUser;
}

export interface ISplitTransfer {
    id: number;
    time: Date;
    amount: number;
    user: number;
    affected_users: number[];

    delta_remainder: number;
    total_balance_before: number;
    total_balance_after: number;
}
