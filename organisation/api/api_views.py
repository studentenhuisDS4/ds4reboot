from django.contrib.contenttypes.models import ContentType
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from organisation.api.serializers.keukendienst import KeukenDienstSchema
from organisation.api.serializers.receipt import ReceiptSchema
from organisation.models import KeukenDienst, Receipt
from plugins.api_attachment import AttachmentsUploadMixin


class KeukenDienstViewSet(ModelViewSet):
    queryset = KeukenDienst.objects.filter(done=False)
    serializer_class = KeukenDienstSchema


class ReceiptViewSet(ListModelMixin, AttachmentsUploadMixin, GenericViewSet):
    RESPONSE_ROOT_NAME = 'receipt'  # upload mixin will pick this up

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSchema

    try:
        content_type = ContentType.objects.get(app_label="organisation", model="receipt")
    except:
        # pass compilation in case of missing migration
        content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
