from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'worm_strains.views',
    url(r'^strains$', 'strains', name='strains_url'),
    url(r'^strain/(?P<name>.+)$', 'strain', name='strain_url'),
)
