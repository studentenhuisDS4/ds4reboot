export interface IResult<T> {
    exception: string;
    traceback: string;
    errors: string[];
    result: T;

    status: IStatus;
}

export enum IStatus {
    SUCCESS = 'success',
    FAILURE = 'failure',
    NOT_IMPL = 'under-construction'
}
