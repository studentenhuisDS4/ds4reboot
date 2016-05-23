from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^remove/$', views.remove_housemate, name='remove housemate'),
    url(r'^set/(?P<group_type>\w+)/(?P<user_id>[0-9]+)/$', views.toggle_group, name='toggle group'),
]
