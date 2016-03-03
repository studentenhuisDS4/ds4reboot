from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log/', views.show_log, name='log'),
    url(r'^boetes/', views.boetes, name='boetes'),
    url(r'^turf/(?P<user_id>[0-9]+)/$', views.turf_item, name='turf'),
]