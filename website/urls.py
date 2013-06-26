from django.conf.urls import patterns, include, url
# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^$', 'home', name='home_url'),
	url(r'^research$', 'research', name='research_url'),
	url(r'^lab_members$', 'lab_members', name='lab_members_url'),
	url(r'^lab_member/(?P<url_name>.+)$', 'lab_member', name='lab_member_url'),
	url(r'^resources$', 'resources', name='resources_url'),
	url(r'^contact$', 'contact', name='contact_url'),
)
