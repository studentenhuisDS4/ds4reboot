from user.models import SnakeHighScore
from user.api.serializers.snake_highscore import SnakeHighScoreSchema
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import IsSuperUser

class SnakeHighScoreViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'

class SnakeHighScoreAdminViewSet(
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'
    permission_classes = [IsSuperUser, ]