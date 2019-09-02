from rest_framework.viewsets import ModelViewSet

from organisation.api.serializers.keukendienst import KeukenDienstSchema
from organisation.models import KeukenDienst


class KeukenDienstViewSet(ModelViewSet):
    queryset = KeukenDienst.objects.filter(done=False)
    serializer_class = KeukenDienstSchema
