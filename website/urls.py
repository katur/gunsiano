from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home_url'),
    url(r'^people/$', views.people, name='people_url'),
    url(r'^person/(?P<username>.+)/$', views.person, name='person_url'),
    url(r'^publications/$', views.publications, name='publications_url'),
    url(r'^resources/$', views.resources, name='resources_url'),
    url(r'^join/$', views.join, name='join_url'),
    url(r'^contact/$', views.contact, name='contact_url'),
    url(r'^lab-tools/$', views.lab_tools, name='lab_tools_url'),
]
