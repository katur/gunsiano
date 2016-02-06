from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
        name='login_url'),
    url(r'^logout/$', auth_views.logout, name='logout_url'),
    url(r'^', include('website.urls')),
    url(r'^', include('worm_strains.urls')),
    url(r'^', include('storage.urls')),
    url(r'^', include('protocols.urls')),
]
