from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

SNAKE_NICK_LENGTH = 100
MAX_CHAT_MESSAGE_LENGTH = 1000


# Create your models here.
class SnakeHighScore(models.Model):
    """
    The DSnake4 game keeps its score in this model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=SNAKE_NICK_LENGTH)
    score = models.IntegerField(null=False)
    time = models.DateTimeField(default=timezone.now)


class SnakeChatMessage(models.Model):
    """
    Simple message storage
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=SNAKE_NICK_LENGTH)
    message = models.CharField(max_length=MAX_CHAT_MESSAGE_LENGTH)
    time = models.DateTimeField(default=timezone.now)
