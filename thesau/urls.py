from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hr/', views.hr, name='hr'),
    path('hr/report/', views.hr, name='hr report index'),
    url(r'^hr/report/([0-9])/$', views.hr, name='hr report'),
    path('hr/make/', views.submit_hr, name='submit hr'),
]