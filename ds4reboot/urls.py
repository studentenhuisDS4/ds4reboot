"""ds4reboot URL Configuration
"""
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView)

from bierlijst.api.api_views import BoeteViewSet, TurfViewSet
from ds4reboot import settings
from ds4reboot.api.auth import LoginHouse, TokenPairView
from ds4reboot.secret_settings import DEBUG
from eetlijst.api.api_dinner import DinnerViewSet, DinnerWeekViewSet, UserDinnerViewSet
from eetlijst.api.api_transfer_cost import TransferCostViewSet, SplitCostViewSet
from organisation.api.api_views import KeukenDienstViewSet, ReceiptViewSet
from user.api.api_user import UserViewSet, UserFullViewSet, UserActionViewSet, HouseViewSet

router = DefaultRouter()
router.register(r'dinner', DinnerViewSet, basename='dinner')
router.register(r'dinnerweek', DinnerWeekViewSet, basename='dinnerweek')
router.register(r'userdinner', UserDinnerViewSet, basename='userdinner')
router.register(r'transfer', TransferCostViewSet, basename='transfer')
router.register(r'split-cost', SplitCostViewSet, basename='split-cost')
router.register(r'boete', BoeteViewSet, basename='boete')
router.register(r'turf', TurfViewSet, basename='Turf')
router.register(r'house', HouseViewSet, basename='House')
router.register(r'user', UserViewSet, basename='User')
router.register(r'user-full', UserFullViewSet, basename='User full')
router.register(r'user-action', UserActionViewSet, basename='User action')
router.register(r'keukendienst', KeukenDienstViewSet, basename='Keukendienst')
router.register(r'receipt', ReceiptViewSet, basename='Receipts')

urlpatterns = \
    [
        path('', include('django.contrib.auth.urls')),
        path('', include('base.urls')),
        path('user/', include('user.urls')),
        path('bierlijst/', include('bierlijst.urls')),
        path('eetlijst/', include('eetlijst.urls')),
        path('thesau/', include('thesau.urls')),
        path('admin/', admin.site.urls),
        path('organisation/', include('organisation.urls')),
        path('ds4admin/', include('ds4admin.urls')),

        path('wiki/notifications/', include('django_nyt.urls')),
        path('wiki/', include('wiki.urls')),

        path(f'{settings.API_BASE_URL}auth-jwt/', TokenPairView.as_view(), name='token'),
        path(f'{settings.API_BASE_URL}auth-jwt-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path(f'{settings.API_BASE_URL}auth-jwt-verify/', TokenVerifyView.as_view(), name='token_verify'),
        path(f'{settings.API_BASE_URL}auth-house/', LoginHouse.as_view()),
        path(f'{settings.API_BASE_URL}', include((router.urls, 'ds4_api'))),
    ]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
