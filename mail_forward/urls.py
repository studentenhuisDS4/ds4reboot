from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from ds4reboot import settings
from mail_forward.api.api_mijndomein import MijndomeinMailForwardViewSet

router = DefaultRouter()
# router.register(r'mail', MailViewSet, basename='mail_forward')
router.register(r'mijndomein', MijndomeinMailForwardViewSet, basename='mijndomein_forwards')

urlpatterns = [
    path(f'{settings.API_BASE_URL}', include((router.urls, 'mail'))),
]