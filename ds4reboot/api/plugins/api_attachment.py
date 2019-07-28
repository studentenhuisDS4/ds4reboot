from PIL import Image
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'


class AttachmentUploadMixin:
    parser_class = (ImageUploadParser,)

    def put(self, request, format=None):
        if 'image' not in request.data:
            raise ParseError("Empty content")

        f = request.data['image']

        try:
            img = Image.open(f)
            img.verify()
        except:
            raise ParseError("Unsupported image type")

        # mymodel.my_file_field.save(f.name, f, save=True)
        print(img)
        return Response(status=status.HTTP_201_CREATED)