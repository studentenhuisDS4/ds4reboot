from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from ds4reboot.api.utils import illegal_action, success_action
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
    filter_fields = '__all__'

    content_type = {
        'app_label': 'organisation',
        'model': 'receipt'
    }

    @action(detail=True, methods=['POST'])
    def accept(self, request, pk=None):
        if request.user.groups.filter(name='thesau').exists():
            receipt = self.get_object()
            receipt.accepted = True
            receipt.accepted_user_id = request.user.id
            receipt.accepted_time = now()
            receipt.save()
            return success_action('')
        else:
            return illegal_action('You are no thesau')

    @action(detail=True, methods=['POST'])
    def unaccept(self, request, pk=None):
        if request.user.groups.filter(name='thesau').exists():
            receipt = self.get_object()
            receipt.accepted = True
            receipt.accepted_user_id = None
            receipt.accepted_time = None
            receipt.save()
            return success_action('')
        else:
            return illegal_action('You are no thesau')

    def destroy(self, request, pk=None):
        if request.user.groups.filter(name='thesau').exists():
            if not pk:
                return illegal_action('No object specified.')
            receipt = self.get_object()
            receipt.receiptcost_set.all().delete()
            receipt.get_attachments().delete()
            receipt.delete()
            return success_action('')
        else:
            return illegal_action('You are no thesau')
