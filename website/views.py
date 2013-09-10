from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from website.models import User, UserProfile, Resource
from django.contrib.auth.decorators import login_required
import string
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
	PubMed search term:
	(Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author]) OR (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])
	"""
	xmldoc = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1v9I1sARILc4F30I7IyGwVTatLAIvtPsS641znyxpiAdx0xgXy")
	tree = ET.parse(xmldoc)
	root = tree.getroot()

	items = []
	for item in root.iter('item'):
		description = item.find('description').text

		# italicize species names, and embolden PI names
		description = string.replace(description,
			"Drosophila",
			"<i>Drosophila</i>"
		)
		description = string.replace(description,
			"Protorhabditis",
			"<i>Protorhabditis</i>"
		)
		description = string.replace(description,
			"C. elegans",
			"<i>C. elegans</i>"
		)
		description = string.replace(description,
			"Caenorhabditis elegans",
			"<i>Caenorhabditis elegans</i>"
		)
		description = string.replace(description,
			"Piano F",
			"<b>Piano F</b>"
		)
		description = string.replace(description,
			"Gunsalus KC",
			"<b>Gunsalus KC</b>"
		)
		description = string.replace(description,
			"Gunsalus K",
			"<b>Gunsalus K</b>"
		)

		item.description = description
		items.append(item)

	return render_to_response('publications.html', {
		'items':items,
	}, context_instance=RequestContext(request))
