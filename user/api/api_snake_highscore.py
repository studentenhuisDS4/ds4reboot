from user.models import SnakeHighScore
from user.api.serializers.snake_highscore import SnakeHighScoreSchema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import IsSuperUser, illegal_action, success_action

class SnakeHighScoreViewSet(RetrieveModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = SnakeHighScoreSchema(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)

class SnakeHighScoreAdminViewSet(
                    DestroyModelMixin, 
                    GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'
    permission_classes = [IsSuperUser, ]