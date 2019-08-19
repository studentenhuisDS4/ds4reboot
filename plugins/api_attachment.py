import traceback
from json import JSONDecodeError

from PIL import Image
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.utils import json

from ds4reboot.api.utils import illegal_action, log_validation_errors, log_exception, success_action, Map
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
        if not 'model' in cls.content_type or not 'app_label' in cls.content_type:
            raise ValueError("content_type needs to be a Dict with model and app_label key/value pairs.")

    def put(self, request):
        batch = []
        marsh = AttachmentsSchema().load(data=request.data)
        if not 'errors' in marsh:
            # Flatten data important to the creation of subclass
            try:
                json_data = json.loads(request.data['json_data'])
            except JSONDecodeError as e:
                return log_exception(f"The attachments were found, but the json_data field was not parsable.")

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
                                            content_type=ContentType.objects.get(**self.content_type),
                                            object_id=object.id)
                try:
                    attachment.attachment_file.save(name=file.name, content=file)
                except Exception as e:
                    return log_exception(e, traceback.format_exc())
        else:
            return log_validation_errors(Map(marsh).errors)

        if getattr(self, 'RESPONSE_ROOT_NAME', None):
            output = {
                self.RESPONSE_ROOT_NAME: self.get_serializer(object).data,
            }
        else:
            output = self.get_serializer(object).data,
        return success_action(data=output, status=status.HTTP_201_CREATED)
