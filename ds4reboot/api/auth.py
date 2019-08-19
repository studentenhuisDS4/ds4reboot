from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers.user import UserSchema

User = get_user_model()


class TokenObtainSerializer(serializers.Serializer):
    identity_field = 'username-or-email'
    identity_rename = 'username'

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.identity_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.identity_rename: attrs[self.identity_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class TokenClaimSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['username'] = str(user.username)
        token['email'] = str(user.email)
        return token

    def validate(self, attrs):
        data = super(TokenClaimSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        return data


class TokenPairView(TokenObtainPairView):
    serializer_class = TokenClaimSerializer


class LoginHouse(APIView):
    def post(self, request):
        user = User.objects.get(username='huis')
        token = TokenClaimSerializer.get_token(user)
        return Response({
            'token': str(token.access_token),
            'refresh': str(token),
            'user': UserSchema(user).data
        })
