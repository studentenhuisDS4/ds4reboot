from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import illegal_action, success_action, unimplemented_action
from eetlijst.api.serializers.transfer_cost import TransferCostSchema, SplitCostSchema, AllCostSchema
from eetlijst.models import Transfer
from user.models import Housemate


class TransferCostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = TransferCostSchema

    def get_queryset(self):
        """
        This view should return a list of all dinners
        entered this week.
        """
        return Transfer.objects \
            .filter(time__gte=timezone.now() - timedelta(days=timezone.now().weekday())) \
            .filter(time__lte=timezone.now() + timedelta(days=(7 - timezone.now().weekday()))) \
            .order_by('time')

    @action(detail=False, methods=['post'])
    def exchange(self, request):
        serializer = TransferCostSchema(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            from_user = Housemate.objects.get(display_name=serializer.validated_data['from_user'])
            from_user.balance -= amount
            from_user.save()

            to_user = Housemate.objects.get(display_name=serializer.validated_data['to_user'])
            to_user.balance += amount
            to_user.save()

            serializer.validated_data['user_id'] = request.user.id
            instance = TransferCostSchema(serializer.save()).data
            return success_action(instance)
        else:
            return illegal_action(serializer.errors)

    @action(detail=False, methods=['post'])
    def split(self, request):
        serializer = SplitCostSchema(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            return unimplemented_action(serializer.validated_data)
            # amount = serializer.validated_data['amount']
            # from_user = Housemate.objects.get(display_name=serializer.validated_data['from_user'])
            # from_user.balance -= amount
            # from_user.save()
            #
            # to_user = Housemate.objects.get(display_name=serializer.validated_data['to_user'])
            # to_user.balance += amount
            # to_user.save()
            #
            # serializer.validated_data['user_id'] = request.user.id
            # instance = TransferCostSchema(serializer.save()).data
            # return success_action(instance)
        else:
            return illegal_action(serializer.errors)

    @action(detail=False, methods=['post'])
    def split_all(self, request):
        serializer = AllCostSchema(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            return unimplemented_action(serializer.validated_data)
            # amount = serializer.validated_data['amount']
            # from_user = Housemate.objects.get(display_name=serializer.validated_data['from_user'])
            # from_user.balance -= amount
            # from_user.save()
            #
            # to_user = Housemate.objects.get(display_name=serializer.validated_data['to_user'])
            # to_user.balance += amount
            # to_user.save()
            #
            # serializer.validated_data['user_id'] = request.user.id
            # instance = TransferCostSchema(serializer.save()).data
            # return success_action(instance)
        else:
            return illegal_action(serializer.errors)
