from rest_framework import serializers
from eetlijst.models import DateList
from user.api.api import SimpleUserSerializer


class DinnerSerializer(serializers.ModelSerializer):
    cook = SimpleUserSerializer()

    class Meta:
        model = DateList
        fields = '__all__'  # Change back to specifics when model is stable
        read_only_fields = ()
        depth = 1
