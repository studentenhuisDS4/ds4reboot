"""ds4reboot URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from ds4reboot.secret_settings import DEBUG
from bierlijst.api.api import BoeteViewSet, TurfViewSet
from ds4reboot import settings
from eetlijst.api.api import DinnerViewSet, DinnerWeekViewSet

router = DefaultRouter()
router.register(r'dinner', DinnerViewSet, basename='dinner')
router.register(r'dinnerweek', DinnerWeekViewSet, basename='dinnerweek')
router.register(r'boete', BoeteViewSet, basename='boete')
router.register(r'turf', TurfViewSet, basename='Turf')

urlpatterns = \
    [
        path('', include('django.contrib.auth.urls')),
        path('', include('base.urls')),
        path('user/', include('user.urls')),
        path('bierlijst/', include('bierlijst.urls')),
        path('eetlijst/', include('eetlijst.urls')),
        path('thesau/', include('thesau.urls')),
        path('admin/', admin.site.urls),

        path('ds4admin/', include('ds4admin.urls')),

        path('wiki/notifications/', include('django_nyt.urls')),
        path('wiki/', include('wiki.urls')),

        path('auth-jwt/', obtain_jwt_token),
        path('auth-jwt-refresh/', refresh_jwt_token),
        path('auth-jwt-verify/', verify_jwt_token),
    ] + router.urls

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)