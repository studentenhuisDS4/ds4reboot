from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profiel/$', views.profile, name='profile'),
    url(r'^profiel/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^instellingen/$', views.settings, name='settings'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^huis/$', views.login_huis, name='login_huis'),
]