from marshmallow import Schema, fields

DATE_NO_TZ = '%Y-%m-%dT%H:%M:%SZ'
DATE_TZ = '%Y-%m-%dT%H:%M:%S+02:00'

class EventTimeSchema(Schema):
    dateTime = fields.DateTime()
    timeZone = fields.Str()


class EventOrganizerSchema(Schema):
    email = fields.Email()
    self = fields.Boolean()


class EventCreatorSchema(Schema):
    email = fields.Email()


class PrivateEventProperty(Schema):
    eventAttendeeList = fields.List(fields.Str())


class ExtendedEventPropertiesSchema(Schema):
    private = fields.Nested(PrivateEventProperty)

# TODO delete if not useful, datetime are giving issues
class GoogleEventSchema(Schema):
    id = fields.Str()

    creator = fields.Nested(EventCreatorSchema, many=False)
    # created = fields.DateTime()
    htmllink = fields.Url()
    # start = fields.Nested(EventTimeSchema)
    # end = fields.Nested(EventTimeSchema)
    organizer = fields.Nested(EventOrganizerSchema)
    summary = fields.Str()
    status = fields.Str()
    # updated = fields.DateTime()

    kind = fields.Str()
    sequence = fields.Int()

    extendedProperties = fields.Nested(ExtendedEventPropertiesSchema)
