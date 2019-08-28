import {BaseFilter, mapping} from './filter.model';

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

export interface ITurfLogEntry {
    id: number;
    turf_to: string;
    torf_by: string;
    turf_user_id: number;
    turf_note: string;
    turf_count: number;
    turf_time: Date;
}

export class TurfLogFilter extends BaseFilter {
    @mapping({name: 'turf_count'}) count?: number = null;
    @mapping({name: 'turf_user'}) userTo?: string = null;
    @mapping({name: 'turf_by'}) userBy?: string = null;
    date?: Date;
}

export interface ITurfLogAggregation {
    aggregate_hours?: boolean;
    aggregate_days?: boolean;
    aggregate_since?: Date;
}
