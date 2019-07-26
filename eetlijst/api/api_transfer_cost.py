from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import illegal_action, success_action
from eetlijst.api.serializers.transfer_cost import TransferCostSchema, SplitTransferSchema
from eetlijst.models import Transfer, SplitTransfer


class TransferCostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferCostSchema
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = TransferCostSchema(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)


class SplitCostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = SplitTransfer.objects.all()
    serializer_class = SplitTransferSchema
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = SplitTransferSchema(data=request.data, context={'user_id': request.user.id})

        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)
