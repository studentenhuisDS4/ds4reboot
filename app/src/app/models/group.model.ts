import { IUser } from './user.model';

export interface IGroup {
    id: number;
    name?: string;
    members?: IUser[];
}

export interface ICreateGroup {
    name: string;
    members: number[];
}

export enum GROUP {
    THESAU = 1,
    ACTIVE = 2,
    WIKI = 3
}
