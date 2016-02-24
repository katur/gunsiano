from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^worms/', views.worms, name='worms_url'),
    url(r'^worm/(?P<name>.+)/$', views.worm, name='worm_url'),
]
