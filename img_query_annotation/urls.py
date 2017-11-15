"""img_query_annotation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^experiment/$', RedirectView.as_view(url='/experiment/login/')),
    url(r'^experiment/login/$', django.contrib.auth.views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^experiment/logout/$', django.contrib.auth.views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^experiment/admin/', admin.site.urls),
    url(r'^experiment/annotation/', include('annotation.urls'), name='annotation'),
]
