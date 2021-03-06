import {IUser} from './user.model';
import {ISplitTransfer} from './transfer.model';

export interface IMoveout {
    user: IUser;
    transfer: ISplitTransfer;
}

export interface IActivation {
    user: IUser;
    activation: boolean;
}

