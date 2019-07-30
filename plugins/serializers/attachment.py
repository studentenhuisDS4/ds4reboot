from marshmallow import Schema, fields, post_dump

from ds4reboot.api.utils import full_media_url


class AttachmentsSchema(Schema):
    attachment = fields.List(fields.Raw(), required=True, load_only=True)
    json_data = fields.Raw(required=True, load_only=True)

    id = fields.Int(dump_only=True)
    upload_url = fields.Url(dump_only=True)
    attachment_file = fields.Str(dump_only=True)
    created = fields.Time(dump_only=True)
    modified = fields.Time(dump_only=True)

    @post_dump
    def add_upload_url(self, data):
        data['upload_url'] = full_media_url(self.context) + data['attachment_file']
