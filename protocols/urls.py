from django.conf.urls import patterns, include, url

urlpatterns = patterns('protocols.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^protocols$', 'protocols', name='protocols_url'),
	url(r'^protocol/(?P<url_title>.+)$', 'protocol', name='protocol_url'),
)
