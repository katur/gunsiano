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
	PubMed search terms:
	both: (Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author]) OR (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])
	kris_only: Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author]
	fabio_only: Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author]
	"""
	xml_file_both = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1v9I1sARILc4F30I7IyGwVTatLAIvtPsS641znyxpiAdx0xgXy")
	xml_file_kris = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1HM5Uxfu7f2MxGrKDT9ZkYODwEeTitazig0NejO4Lw9dlj9kdA")
	xml_file_fabio = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1-ONS2P_EKbiHxur7eYe8GZYYiix15mspfs-N0HFxYmGQWLsU7")

	def generate_items(xml_file):
		# define functions to bolden or italicize a search term in a string
		def embolden(s, term):
			return string.replace(s, term, "<b>" + term + "</b>")

		def italicize(s, term):
			return string.replace(s, term, "<i>" + term + "</i>")

		# generate tree representing the tags of an xml file and get the root
		tree = ET.parse(xml_file)
		root = tree.getroot()

		# define an empty list to fill with the publications given in the xml file
		publications = []
		for publication in root.iter('item'):
			d = publication.find('description').text

			# italicize species names, and embolden PI names
			d = embolden(d, "Piano F")
			d = embolden(d, "Gunsalus KC")
			d = embolden(d, "Gunsalus K")
			d = string.replace(d, "Caenorhabditis  elegans", "Caenorhabditis elegans")
			d = italicize(d, "Caenorhabditis elegans")
			d = italicize(d, "C. elegans")
			d = italicize(d, "Drosophila")
			d = italicize(d, "Protorhabditis")

			publication.description = d
			publications.append(publication)
		return publications

	pub_both = generate_items(xml_file_both)
	pub_kris = generate_items(xml_file_kris)
	pub_fabio = generate_items(xml_file_fabio)

	return render_to_response('publications.html', {
		'pub_both':pub_both,
		'pub_kris':pub_kris,
		'pub_fabio':pub_fabio,
	}, context_instance=RequestContext(request))

