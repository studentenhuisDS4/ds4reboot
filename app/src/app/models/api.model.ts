export interface IResult<T> {
    exception: string;
    traceback: string;
    errors: string[];
    result: T;

    status: IStatus;
}

export interface IPagination<T> {
    count: number;
    next: URL;
    previous: URL;
    results: T;
}

export enum IStatus {
    SUCCESS = 'success',
    FAILURE = 'failure',
    NOT_IMPL = 'under-construction'
}
