from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'', include('website.urls')),
    url(r'', include('worm_strains.urls')),
    url(r'', include('storage.urls')),
    url(r'', include('protocols.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
