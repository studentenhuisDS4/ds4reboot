import {IUser} from './user.model';

export enum SHARE {
    ALL = 'share_all',
    CUSTOM = 'specific',
    HOUSE = 'house'
}

export interface IReceipt {
    id: number;
    receipt_title: string;
    receipt_description: string;
    receipt_cost: number;
    upload_user?: IUser;

    accepted: boolean;
    accepted_user: IUser;
    accepted_time: Date;

    receipt_costs_split: IReceiptCost[];
}

export interface IReceiptCost {
    cost_user: number;
    affected_user_id: number;
}
