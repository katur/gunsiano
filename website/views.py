from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from website.models import User, UserProfile, Resource
from django.contrib.auth.decorators import login_required
import xml.etree.ElementTree as ET
import urllib2


def home(request):
	"""
	Homepage
	"""
	# render page
	return render_to_response('home.html', context_instance=RequestContext(request))


def research(request):
	"""
	Research Areas
	"""
	# render page
	return render_to_response('research.html', context_instance=RequestContext(request))


def lab_members(request):
	"""
	Page listing all lab members
	"""
	# get all lab members
	profiles = UserProfile.objects.all().order_by('-is_current', 'position__display_order', 'user__last_name')
	for profile in profiles:
		if profile.is_current:
			profile.display_position = profile.position.position
		else:
			profile.display_position = "Former Lab Member"

	return render_to_response('lab_members.html', {
		'profiles':profiles
	}, context_instance=RequestContext(request))


def lab_member(request, username):
	"""
	Page for each lab member
	"""
	user = get_object_or_404(User, username=username)
	return render_to_response('lab_member.html', {
		'user':user,
	}, context_instance=RequestContext(request))


def resources(request):
	"""
	Resources Page
	"""
	r = Resource.objects.all().order_by('name')

	return render_to_response('resources.html', {
		'resources':r
	}, context_instance=RequestContext(request))


def contact(request):
	"""
	Contact Page
	"""
	return render_to_response('contact.html', context_instance=RequestContext(request))


@login_required
def lab_tools(request):
	"""
	Internal Lab Tools landing page
	"""
	# render page
	return render_to_response('lab_tools.html', context_instance=RequestContext(request))


def publications(request):
	"""
	Page for publications, fetched dynamically from PubMed
	"""
	xmldoc = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1piP1Xotxtp6HZi3WJ-3lHVH9brJqC2fnqZNpmbUOOOEUSLkU3")
	tree = ET.parse(xmldoc)
	root = tree.getroot()

	items = []
	for item in root.iter('item'):
		item.description = item.find('description').text
		items.append(item)

	return render_to_response('publications.html', {
		'items':items,
	}, context_instance=RequestContext(request))
