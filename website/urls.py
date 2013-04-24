from django.conf.urls import patterns, include, url
# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^$', 'home', name='home_url'),
	url(r'^contact$', 'contact', name='contact_url'),
	url(r'^lab_members$', 'lab_members', name='lab_members_url'),
	url(r'^research_areas$', 'research_areas', name='research_areas_url'),
	url(r'^research_area/(?P<research_area>.+)$', 'research_area', name='research_area_url'),
)
