from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^protocols/$', views.protocols, name='protocols_url'),
    url(r'^protocol/(?P<title_url>.+)/$', views.protocol,
        name='protocol_url'),
]
