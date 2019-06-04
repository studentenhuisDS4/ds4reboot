from rest_framework import serializers, viewsets

from eetlijst.models import DateList


class DinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateList
        fields = '__all__'  # Change back to specifics when model is stable
        read_only_field = []


class DinnerViewSet(viewsets.ModelViewSet):
    queryset = DateList.objects.order_by(
        '-date')
    serializer_class = DinnerSerializer


# Week list
# class DinnerWeekViewSet(viewsets.ModelViewSet):
#     queryset = DateList.objects.filter(date__gte=).order_by(
#         'date')
#     serializer_class = DinnerSerializer
