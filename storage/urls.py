from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^storage/$', views.storage, name='storage_url'),
    url(r'^container/(?P<container_id>.+)/$', views.container,
        name='container_url'),
]
