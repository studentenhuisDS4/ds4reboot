from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home page'),
    url(r'^contact/', views.contact, name='contact'),
]