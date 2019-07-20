from datetime import timedelta

from django.utils import timezone
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from eetlijst.api.serializers.dinner import DinnerSchema
from eetlijst.models import Dinner


class TransferCostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = DinnerSchema
    queryset = Dinner.objects.order_by('-date')

    def get_queryset(self):
        """
        This view should return a list of all dinners
        entered this week.
        """
        return Dinner.objects \
            .filter(date__gte=timezone.now() - timedelta(days=timezone.now().weekday())) \
            .filter(date__lte=timezone.now() + timedelta(days=(7 - timezone.now().weekday()))) \
            .order_by('date')
