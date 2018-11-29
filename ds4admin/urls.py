from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='housemates', permanent=False)),
    path('huisgenoten/', views.housemates, name='housemates'),
    path('balance/', views.balance, name='balance'),
    path('permissies/', views.permissions, name='permissions'),
    path('summary/', views.summary, name='summary'),
    path('create_user/', views.create_user, name='create user'),
    path('create_user/post', views.create_user_post, name='create user post'),
    url(r'^permissies/set/(?P<group_type>\w+)/(?P<user_id>[0-9]+)/$', views.toggle_group, name='toggle group'),
    url(r'^activate/$', views.activate_housemate, name='activate housemate'),
    url(r'^deactivate/$', views.deactivate_housemate, name='deactivate housemate'),
    url(r'^remove/$', views.remove_housemate, name='remove housemate'),
]
