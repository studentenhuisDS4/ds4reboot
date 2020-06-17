from rest_framework.viewsets import ModelViewSet

from organisation.api.serializers.keukendienst import KeukenDienstSchema
from organisation.models import KeukenDienst


class KeukenDienstViewSet(ModelViewSet):
    # This was never finished. Feel free to do so, if the house needs a better cleaning schedule :)
    # Kind regards, D. Zwart, May 2020
    
    queryset = KeukenDienst.objects.filter(done=False)
    serializer_class = KeukenDienstSchema
