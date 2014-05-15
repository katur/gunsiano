from django.conf.urls import patterns, url


urlpatterns = patterns(
    'website.views',
    url(r'^$', 'home', name='home_url'),
    url(r'^lab_members$', 'lab_members', name='lab_members_url'),
    url(r'^lab_member/(?P<username>.+)$', 'lab_member', name='lab_member_url'),
    url(r'^publications$', 'publications', name='publications_url'),
    url(r'^resources$', 'resources', name='resources_url'),
    url(r'^join$', 'join', name='join_url'),
    url(r'^contact$', 'contact', name='contact_url'),
    url(r'^lab_tools$', 'lab_tools', name='lab_tools_url'),
)


urlpatterns += patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout_url'),
)
