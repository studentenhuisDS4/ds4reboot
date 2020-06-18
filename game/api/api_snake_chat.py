from django.utils.timezone import timedelta, datetime, utc
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import IsSuperUser, illegal_action, success_action
from game.api.serializers.snake_chatmessage import SnakeChatMessageSchema
from game.models import SnakeChatMessage


class SnakeChatMessageViewSet(RetrieveModelMixin,
                              ListModelMixin,
                              GenericViewSet):
    # This is not dynamic
    queryset = SnakeChatMessage.objects.filter(time__gte=(datetime.utcnow() - timedelta(days=7)).replace(tzinfo=utc))
    serializer_class = SnakeChatMessageSchema
    filter_fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.queryset = SnakeChatMessage.objects.filter(
            time__gte=(datetime.utcnow() - timedelta(days=7)).replace(tzinfo=utc))
        super().__init__(*args, **kwargs)

    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = SnakeChatMessageSchema(data=request.data, context={
            'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return success_action(serializer.data)
        else:
            return illegal_action(serializer.errors)


class SnakeChatMessageAdminViewSet(GenericViewSet):
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
