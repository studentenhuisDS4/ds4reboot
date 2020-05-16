from game.models import SnakeChatMessage
from game.api.serializers.snake_chatmessage import SnakeChatMessageSchema, SnakeChatClearSchema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
import json

from ds4reboot.api.utils import IsSuperUser, illegal_action, success_action
from django.utils.datetime_safe import datetime
from _datetime import timedelta


class SnakeChatMessageViewSet(RetrieveModelMixin,
                              ListModelMixin,
                              GenericViewSet):
    queryset = SnakeChatMessage.objects.filter(time__gte=datetime.now()-timedelta(days=7))
    serializer_class = SnakeChatMessageSchema
    filter_fields = '__all__'

    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = SnakeChatMessageSchema(data=request.data, context={
                                            'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)


class SnakeChatMessageAdminViewSet(
        GenericViewSet
):
    queryset = SnakeChatMessage.objects.all()
    serializer_class = SnakeChatMessageSchema
    filter_fields = '__all__'
    permission_classes = [IsSuperUser, ]

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        serializer = SnakeChatMessageSchema(data=request.data, many=False)
        if serializer.is_valid():
            chatmessages = None
            data = serializer.data
            if data["remove_all"]:
                chatmessages = SnakeChatMessage.objects.all()
            else:
                chatmessages = SnakeChatMessage.objects.filter(
                    user_id=data["remove_user"])
            deleted_chatmessages = list(chatmessages)
            chatmessages.delete()
            return success_action(SnakeChatMessageSchema().dump(deleted_chatmessages, many=True))
        else:
            return illegal_action(serializer.errors)
