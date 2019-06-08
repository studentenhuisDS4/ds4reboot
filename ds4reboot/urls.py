"""ds4reboot URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from eetlijst.api import DinnerViewSet

router = DefaultRouter()
router.register(r'dinner', DinnerViewSet, basename='dinner')

urlpatterns = [
                  url('^', include('django.contrib.auth.urls')),
                  url(r'^', include('base.urls')),
                  url(r'^user/', include('user.urls')),
                  url(r'^bierlijst/', include('bierlijst.urls')),
                  url(r'^eetlijst/', include('eetlijst.urls')),
                  url(r'^thesau/', include('thesau.urls')),
                  url(r'^ds4admin/', include('ds4admin.urls')),
                  url(r'^admin/', admin.site.urls),
                  path('wiki/notifications/', include('django_nyt.urls')),
                  path('wiki/', include('wiki.urls')),

                  path('auth-jwt/', obtain_jwt_token),
                  path('auth-jwt-refresh/', refresh_jwt_token),
                  path('auth-jwt-verify/', verify_jwt_token),

                  # path('', include('pwa.urls')),
              ] + router.urls
