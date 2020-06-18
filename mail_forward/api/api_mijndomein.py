from rest_framework.decorators import action
from django.http import HttpResponse

from ds4reboot.api.auth import User
from mail_forward.client_api.actions import get_mijndomein_filters, update_mijndomein_filters
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import EmptySchema, success_action
from ds4reboot.secret_settings import DEBUG


class MijndomeinMailForwardViewSet(GenericViewSet):
    serializer_class = EmptySchema
    filter_fields = '__all__'

    @action(detail=False, methods=['GET'])
    def get_filters(self, request, pk=None):
        if not DEBUG and (request.user.is_superuser or request.user.is_staff):
            return HttpResponse('Denied (not admin)')
        else:
            filters = get_mijndomein_filters()
            return HttpResponse(filters)

    @action(detail=False, methods=['POST'])
    def update_filters(self, request, pk=None):
        if not DEBUG and (request.user.is_superuser or request.user.is_staff):
            return HttpResponse('Denied (not admin)')
        else:
            active_users = User.objects.filter(is_active=True)
            buckets_four = [[]]
            index = 0
            for user in active_users:
                if user.email == "admin@ds4.nl" or user.email == "mail@ds4.nl":
                    continue
                elif not user.email:
                    continue

                if len(buckets_four[index]) == 4:
                    buckets_four.append([])
                    index += 1
                buckets_four[index].append(user.email)

            entries_response = update_mijndomein_filters(buckets_four)
            return success_action(data=entries_response)
