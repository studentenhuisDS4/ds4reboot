"""ds4reboot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^bierlijst/', include('bierlijst.urls')),
    url(r'^eetlijst/', include('eetlijst.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^thesau/', include('thesau.urls')),
    url(r'^ds4admin/', include('ds4admin.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('gcm.urls')),
]
