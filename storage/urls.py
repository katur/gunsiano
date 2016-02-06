from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^storage/$', views.storage, name='storage_url'),
    url(r'^storage/(?P<container_id>.+)/$', views.storage_detail,
        name='storage_detail_url'),
]
