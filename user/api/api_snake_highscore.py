from user.models import SnakeHighScore
from user.api.serializers.snake_highscore import SnakeHighScoreSchema, SnakeHighScoreClearSchema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
import json

from ds4reboot.api.utils import IsSuperUser, illegal_action, success_action


class SnakeHighScoreViewSet(RetrieveModelMixin,
                            ListModelMixin,
                            GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = SnakeHighScoreSchema(data=request.data, context={
                                          'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)


class SnakeHighScoreAdminViewSet(
    # DestroyModelMixin,
        GenericViewSet):
    queryset = SnakeHighScore.objects.all()
    serializer_class = SnakeHighScoreSchema
    filter_fields = '__all__'
    permission_classes = [IsSuperUser, ]

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        serializer = SnakeHighScoreClearSchema(data=request.data, many=False)
        if serializer.is_valid():
            highscores = None
            data = serializer.data
            if data["remove_all"]:
                highscores = SnakeHighScore.objects.all()
            else:
                highscores = SnakeHighScore.objects.filter(
                    user_id=data["remove_user"])
            deleted_highscores = list(highscores)
            highscores.delete()
            return success_action(SnakeHighScoreSchema().dump(deleted_highscores, many=True))
        else:
            return illegal_action(serializer.errors)
