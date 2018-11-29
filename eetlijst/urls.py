from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eetlijst index'),
    path('go/', views.goto_date, name='goto date'),
    path('enroll/', views.enroll, name='enroll'),
    path('close/', views.close, name='close'),
    path('cost/', views.cost, name='cost'),
    path('ho/', views.add_ho, name='ho'),
    path('ho/log/', views.ho_log, name='ho log'),
    url(r'^ho/log/(?P<page>[0-9]+)/?$', views.ho_log, name='ho log'),
    path('transfer/', views.bal_transfer, name='transfer'),
    path('transfer/log/', views.transfer_log, name='transfer log'),
    url(r'^transfer/log/(?P<page>[0-9]+)/?$', views.transfer_log, name='transfer log'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.index, name='index'),
]
