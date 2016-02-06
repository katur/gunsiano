from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^strains/', views.strains, name='strains_url'),
    url(r'^strain/(?P<name>.+)/$', views.strain, name='strain_url'),
]
