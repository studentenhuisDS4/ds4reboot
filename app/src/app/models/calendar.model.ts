interface IEventMember {
    email: string;
    self?: boolean;
}

interface IEventTime {
    dateTime: Date;
    timeZone: string;
}

interface IEventProperty {
    private: string[];
}

export interface ICalendarEvent {
    id: string;
    creator: IEventMember;
    created: Date;
    htmllink: URL;
    start: IEventTime;
    end: IEventTime;
    organizer: IEventMember;
    summary: string;
    status: string;
    updated: Date;
    kind: string;
    sequence: number;
    extendedProperties: IEventProperty;
}
