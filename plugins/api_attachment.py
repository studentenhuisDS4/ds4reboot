import traceback
from pprint import pprint

from PIL import Image
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.utils import json

from base.templatetags.resource_tags import full_media_url
from ds4reboot.api.utils import illegal_action, log_validation_errors, log_exception, success_action
from plugins.models import RestAttachment
from plugins.serializers.attachment import AttachmentsSchema


class AttachmentsUploadMixin():
    parser_classes = (MultiPartParser,)

    def local_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return instance

    def __init_subclass__(cls, **kwargs):
        if not getattr(cls, 'content_type', None):
            raise ValueError("content_type needs to be specified in ViewSet/APIView class to define attachments")

    def put(self, request):
        batch = []
        marsh = AttachmentsSchema().load(data=request.data)
        if not marsh.errors:
            # Flatten data important to the creation of subclass
            json_data = json.loads(request.data['json_data'])
            for key, value in json_data.items():
                request.data[key] = value
            request.data.pop('json_data')
            attachments = request.data.pop('attachment')

            # Propagate create and expect instance
            object = self.local_create(request)
            if not object.id:
                return log_exception(f"The {object} was not created and uploading attachment was skipped.")

            for file in attachments:
                try:
                    img = Image.open(file)
                    img.verify()
                except Exception as e:
                    return illegal_action("Unsupported attachment type" + str(e))
                attachment = RestAttachment(creator_id=request.user.id,
                                            content_type=self.content_type, object_id=object.id)
                try:
                    attachment.attachment_file.save(name=file.name, content=file)
                except Exception as e:
                    return log_exception(e, traceback.format_exc())
        else:
            return log_validation_errors(marsh.errors)

        if getattr(self, 'RESPONSE_ROOT_NAME', None):
            output = {
                self.RESPONSE_ROOT_NAME: self.get_serializer(object).data,
            }
        else:
            output = self.get_serializer(object).data,
        return success_action(data=output, status=status.HTTP_201_CREATED)
