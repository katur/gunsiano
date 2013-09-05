from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^$', 'home', name='home_url'),
	url(r'^research$', 'research', name='research_url'),
	url(r'^lab_members$', 'lab_members', name='lab_members_url'),
	url(r'^lab_member/(?P<username>.+)$', 'lab_member', name='lab_member_url'),
	url(r'^resources$', 'resources', name='resources_url'),
	url(r'^contact$', 'contact', name='contact_url'),
	url(r'^worm_portal$', 'worm_portal', name='worm_portal_url'),
)

urlpatterns += url(r'^login/$', 'django.contrib.auth.views.login', {
	'template_name':'login.html',
}), url(r'^logout/$', 'django.contrib.auth.views.logout', {
	'next_page':'/',
}),
