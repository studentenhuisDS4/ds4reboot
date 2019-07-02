export interface IResult {
    exception: string;
    traceback: string;
    errors: string[];
    result: any;

    status: IStatus;
}

export enum IStatus {
    SUCCESS = 'success',
    FAILURE = 'failure',
    NOT_IMPL = 'under-construction'
}
