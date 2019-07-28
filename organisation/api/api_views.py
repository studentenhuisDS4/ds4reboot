from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin

from ds4reboot.api.plugins.api_attachment import AttachmentUploadMixin
from ds4reboot.api.utils import EmptySchema
from organisation.api.serializers.keukendienst import KeukenDienstSchema
from organisation.api.serializers.receipt import ReceiptSchema
from organisation.models import KeukenDienst, Receipt


class KeukenDienstViewSet(ModelViewSet):
    queryset = KeukenDienst.objects.filter(done=False)
    serializer_class = KeukenDienstSchema


class ReceiptViewSet(ListModelMixin, AttachmentUploadMixin, GenericViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSchema
