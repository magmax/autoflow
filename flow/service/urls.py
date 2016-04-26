from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<project>[^/]+)/(?P<status>[^/]+)/?', views.add_status),
]
