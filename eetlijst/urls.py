from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^go/$', views.goto_date, name='goto date'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.index, name='index'),
]
