from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Housemate


class SimpleHouseMateSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField()
    balance = serializers.DecimalField(max_digits=7, decimal_places=2)
    diet = serializers.CharField()

    class Meta:
        model = Housemate
        exclude = ('id',
                   'moveout_date', 'moveout_set', 'deleted_at',
                   'boetes_geturfd_rwijn', 'boetes_geturfd_wwijn', 'boetes_open',
                   'cell_phone', 'parent_phone')
        readOnly = '__all__'


class SimpleUserSerializer(serializers.ModelSerializer):
    housemate = SimpleHouseMateSerializer()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'email', 'date_joined','is_staff', 'is_active', 'is_superuser')
        readOnly = '__all__'
