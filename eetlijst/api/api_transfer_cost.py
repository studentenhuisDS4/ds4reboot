from decimal import Decimal
from math import floor, ceil

from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import illegal_action, success_action
from eetlijst.api.serializers.transfer_cost import TransferCostSchema, SplitTransferSchema
from eetlijst.models import Transfer, SplitTransfer
from user.api.serializers.user import UserSchema
from user.models import get_movedin_users, get_total_balance


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

    @action(detail=False, methods=['get'])
    def total_balance(self, request):
        users = get_movedin_users()
        total_balance = get_total_balance()
        split_min = -total_balance / len(users)
        split_min = floor(split_min * 100) / 100.0 if split_min >= 0 else ceil(split_min * 100) / 100.0
        split_min = round(Decimal(split_min), 2)
        return success_action({
            'total_balance': total_balance,
            'users': len(users),
            'split': split_min,
            'remainder': total_balance + split_min * len(users)
        })

    @action(detail=False, methods=['post'])
    def reset_total(self, request):
        if not request.user.is_staff or not request.user.is_superuser:
            return illegal_action('You are no admin.')
        else:
            users = get_movedin_users()
            house = User.objects.get(id=2)
            count = len(users)

            total_balance = get_total_balance()
            if abs(total_balance) < 0.01 * count:
                return illegal_action('Resetting balance is not required (<0.22). TOTAL=' + str(total_balance)
                                      + ', APPLIED_USERS=' + str(count) + ', MINIUM_DEV=' + str(0.01 * count))

            split_min = -(total_balance + house.housemate.balance) / count
            split_min = floor(split_min * 100) / 100.0 if split_min >= 0 else ceil(split_min * 100) / 100.0
            split_min = round(Decimal(split_min), 2)
            total_balance_after = Decimal(0)
            for user in users:
                user.housemate.balance += split_min
                total_balance_after += user.housemate.balance
            total_balance_after += house.housemate.balance

            users_serialized = UserSchema(many=True).dump(users)
            user_ids = [user.id for user in users]
            transfer = SplitTransfer(
                amount=split_min*count,
                user=request.user,
                note='Total balance reset',
                affected_users=user_ids,
                total_balance_after=total_balance_after,
                total_balance_before=total_balance,
                delta_remainder=total_balance - get_total_balance()
            )

            # commit operation
            transfer.save()
            for user in users:
                user.housemate.save()
            house.housemate.balance -= Decimal(total_balance_after)
            house.housemate.save()
            transfer_house = SplitTransfer(
                amount=-total_balance_after,
                user=request.user,
                note='Reset remainder',
                affected_users=[2],
                total_balance_after=get_total_balance(),
                total_balance_before=total_balance_after
            )
            transfer_house.save()

            data = {
                'transaction': TransferCostSchema(exclude=['user', ]).dump(transfer),
                'transaction_remainder': TransferCostSchema(exclude=['user', ]).dump(transfer_house),
                'users': users_serialized,
            }
            return success_action(data)


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
