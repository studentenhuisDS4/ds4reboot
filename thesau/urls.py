from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hr/$', views.hr, name='hr'),
    url(r'^hr/add_item/$', views.add_item, name='hr'),
    url(r'^hr/archief/$', views.hr_archive, name='hr archive'),
    url(r'^hr/report/$', views.hr, name='hr report index'),
    url(r'^hr/report/([0-9])/$', views.hr, name='hr report'),
    url(r'^hr/make/$', views.submit_hr, name='submit hr'),
]