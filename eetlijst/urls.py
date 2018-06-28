from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='eetlijst index'),
    url(r'^doorbell/$', views.doorbell, name='eetlijst doorbell'),
    url(r'^go/$', views.goto_date, name='goto date'),
    url(r'^enroll/$', views.enroll, name='enroll'),
    url(r'^close/$', views.close, name='close'),
    url(r'^cost/$', views.cost, name='cost'),
    url(r'^ho/$', views.add_ho, name='ho'),
    url(r'^ho/log/$', views.ho_log, name='ho log'),
    url(r'^ho/log/(?P<page>[0-9]+)/?$', views.ho_log, name='ho log'),
    url(r'^transfer/$', views.bal_transfer, name='transfer'),
    url(r'^transfer/log/$', views.transfer_log, name='transfer log'),
    url(r'^transfer/log/(?P<page>[0-9]+)/?$', views.transfer_log, name='transfer log'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.index, name='index'),
]
