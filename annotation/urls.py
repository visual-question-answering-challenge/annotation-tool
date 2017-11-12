from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^store_query/$', views.receive_query_search, name='store_query'),
    url(r'^$', views.index, name='index'),
]