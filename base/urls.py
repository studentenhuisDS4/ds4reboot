from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home page'),
    path('contact/', views.contact, name='contact'),

]