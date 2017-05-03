from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bank_mutations/$', views.bank_mutations, name='bank mutations'),
    url(r'^bank_mutations/change/(?P<type>\w+)/(?P<file_id>[0-9]+)/$', views.bank_mutations_change, name='mutations file change'),
    url(r'^process/$', views.process, name='process'),
    url(r'^hr/$', views.hr, name='hr'),
    url(r'^hr/report/$', views.hr, name='hr report index'),
    url(r'^hr/report/([0-9])/$', views.hr, name='hr report'),
    url(r'^hr/make/$', views.submit_hr, name='submit hr'),
]