from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='housemates', permanent=False)),
    url(r'^huisgenoten/$', views.housemates, name='housemates'),
    url(r'^balance/$', views.balance, name='balance'),
    url(r'^permissies/$', views.permissions, name='permissions'),
    url(r'^permissies/set/(?P<group_type>\w+)/(?P<user_id>[0-9]+)/$', views.toggle_group, name='toggle group'),
    url(r'^remove/$', views.remove_housemate, name='remove housemate'),
]
