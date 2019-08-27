import {Filter} from './filter.model';

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

function f() {
    console.log('f(): evaluated');
    return function(target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log('f(): called');
    };
}

function g() {
    console.log('g(): evaluated');
    return function(target, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log('g(): called');
    };
}

export class TurfLogFilter implements Filter {
    @f()
    @g()
    count?: number = null;
    userTo?: string = null;
    userNy?: string = null;
    date?: Date;

    serialize(): string {
        let query = '';
        Object.keys(this).forEach(key => {
            if (this[key]) {
                query += this[key] + '&';
            }
        });
        return `?${query}`;

    }

}

export interface ITurfLogAggregation {
    aggregate_hours?: boolean;
    aggregate_days?: boolean;
    aggregate_since?: Date;
}
