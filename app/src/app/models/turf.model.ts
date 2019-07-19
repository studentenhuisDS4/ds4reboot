import {IHousemate} from './profile.model';
import {IResult} from './api.model';

export interface ITurfItem {
    turf_count: number;
    turf_user_id: number;
    turf_type: TurfType;
    turf_note: string;
}

export enum TurfType {
    BEER = 'beer',
    RWINE = 'red-wine',
    WWINE = 'white-wine'
}
