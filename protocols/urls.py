from django.conf.urls import patterns, url


urlpatterns = patterns(
    'protocols.views',
    url(r'^protocols$', 'protocols', name='protocols_url'),
    url(r'^protocol/(?P<title_url>.+)$', 'protocol', name='protocol_url'),
)
