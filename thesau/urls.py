from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hr/$', views.hr, name='hr'),
    url(r'^hr/bank_mutationss/$', views.bank_mutationss, name='hr'),
    url(r'^hr/report/$', views.hr, name='hr report index'),
    url(r'^hr/report/([0-9])/$', views.hr, name='hr report'),
    url(r'^hr/make/$', views.submit_hr, name='submit hr'),
]