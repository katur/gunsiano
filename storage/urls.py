from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable
urlpatterns = patterns('storage.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^storage$', 'storage', name='storage_url'),
	url(r'^storage/(?P<parent_container_id>.+)$', 'storage_detail', name='storage_detail_url')
)
