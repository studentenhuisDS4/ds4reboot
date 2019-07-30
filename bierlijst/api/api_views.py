import traceback

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bierlijst.api.api import BoeteSerializer, TurfSerializer, TurfSchema, BEER, WWINE, RWINE
from bierlijst.models import Turf, Boete
from ds4reboot.api.utils import log_exception, log_validation_errors, success_action, unimplemented_action
from user.api.serializers.user import HousemateSchema
from user.models import Housemate


class TurfViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = Turf.objects.order_by('-turf_time')
    serializer_class = TurfSerializer
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def turf_item(self, request):
        try:
            serializer = TurfSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)
            else:
                # Auto-generate data
                serializer.validated_data['turf_by'] = self.request.user.username
                serializer.validated_data['turf_to'] = User.objects.get(
                    id=serializer.validated_data['turf_user_id']).username
                turf_obj = serializer.save()

                # Update and serialize housemate
                hm_turf = Housemate.objects.get(user_id__exact=turf_obj.turf_user)
                if turf_obj.turf_type == BEER:
                    hm_turf.sum_bier += turf_obj.turf_count
                elif turf_obj.turf_type == WWINE:
                    hm_turf.sum_wwijn += turf_obj.turf_count
                elif turf_obj.turf_type == RWINE:
                    hm_turf.sum_rwijn += turf_obj.turf_count
                hm_turf.save()
                hm_json = HousemateSchema(hm_turf, many=False)

                # Return turf and housemate data
                return success_action(hm_json.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    @action(detail=True, methods=['post'])
    def turf_edit(self, request):
        input = request
        # (success, data) = self.save_turf_data(request)
        return unimplemented_action({})

    @action(detail=True, methods=['post'])
    def turf_remove(self, request):
        input = request
        # (success, data) = self.save_turf_data(request)
        return unimplemented_action({})


class BoeteViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Boete.objects.order_by(
        '-created_time')
    serializer_class = BoeteSerializer
    filter_fields = '__all__'

    @action(detail=True, methods=['post'])
    def turf_boete(self, request, pk=None):
        return unimplemented_action({})

    @action(detail=True, methods=['post'])
    def create_boete(self, request, pk=None):
        return unimplemented_action({})
