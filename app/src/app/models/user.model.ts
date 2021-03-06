import { IGroup } from './group.model';

export interface IPermission {
    id: number;
}

export const HOUSE_ID = 2;
export const ADMIN_ID = 1;

export interface IHousemate {
    display_name: string;
    user: number;
    diet: string;
    room_number: number;
    movein_date: Date;
    sublet_date: Date;
    moveout_set: boolean;
    moveout_date: Date;


    balance: string; // TODO: fix into number later?
    boetes_total: number;
    sum_bier: number;
    sum_rwijn: number;
    sum_wwijn: number;
    total_bier: number;
    total_rwijn: number;
    total_wwijn: number;
}

export interface IUser {
    id: number;
    last_name: string;
    first_name: string;
    username: string;
    housemate: IHousemate;
    email: string;

    is_superuser: boolean;
    is_staff: boolean;      // Has no permissions by default, but is still admin.
    is_active: boolean;

    user_permissions: IPermission[];
    groups: IGroup[];
}
