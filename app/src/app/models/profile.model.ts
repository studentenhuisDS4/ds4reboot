export interface IPermission {
    id: number;
}

export interface IGroup {
    id: number;
}

export interface IHousemate {
    display_name: string;
    user: number;
    diet: string;
    room_number: number;
    movein_date: Date;

    balance: string; // TODO: fix into number later?
    boetes_total: number;
    sum_bier: number;
    sum_rwijn: number;
    sum_wwijn: number;
    total_bier: number;
    total_rwijn: number;
    total_wwijn: number;
}

export interface IProfile {
    id: number;
    last_name: string;
    first_name: string;
    username: string;
    housemate: IHousemate;

    user_permissions: IPermission[];
    groups: IGroup[];
}
