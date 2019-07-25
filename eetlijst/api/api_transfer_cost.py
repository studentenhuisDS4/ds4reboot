from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import illegal_action, success_action, unimplemented_action
from eetlijst.api.serializers.transfer_cost import TransferCostSchema, SplitTransferSchema
from eetlijst.models import Transfer


class TransferCostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TransferCostSchema

    def get_queryset(self):
        """
        This view should return a list of all transfers
        entered this week.
        """
        return Transfer.objects \
            .filter(time__gte=timezone.now() - timedelta(days=7)) \
            .order_by('time')

    @action(detail=False, methods=['post'])
    def exchange(self, request):
        serializer = TransferCostSchema(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)

    @action(detail=False, methods=['post'])
    def split(self, request):
        serializer = SplitTransferSchema(data=request.data, context={'user_id': request.user.id})

        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)

    @action(detail=False,methods=['post'])
    def filter(self, request):

