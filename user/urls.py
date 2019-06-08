from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiel/', views.profile, name='profile'),
    url(r'^profiel/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('huis/', views.login_huis, name='login huis'),
]