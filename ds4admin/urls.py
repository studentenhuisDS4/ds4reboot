from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^remove/$', views.remove_housemate, name='remove housemate'),
]
