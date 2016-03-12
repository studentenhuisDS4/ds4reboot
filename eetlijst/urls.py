from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^go/$', views.goto_date, name='goto date'),
    url(r'^enroll/$', views.enroll, name='enroll'),
    url(r'^close/$', views.close, name='close'),
    url(r'^cost/$', views.cost, name='cost'),
    url(r'^ho/$', views.add_ho, name='ho'),
    url(r'^transfer/$', views.bal_transfer, name='transfer'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.index, name='index'),
]
