from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from website.models import User, UserProfile, ResearchArea, Resource
from django.contrib.auth.decorators import login_required
import string, math
import xml.etree.ElementTree as ET
import urllib2


def home(request):
	"""
	Homepage
	"""
	n = get_object_or_404(ResearchArea, id=1)
	c = get_object_or_404(ResearchArea, id=2)
	e = get_object_or_404(ResearchArea, id=3)
	g = get_object_or_404(ResearchArea, id=4)
	r = get_object_or_404(ResearchArea, id=5)
	m = get_object_or_404(ResearchArea, id=6)

	return render_to_response('home.html', {
		'network':n,
		'cell':c,
		'evolution':e,
		'gi':g,
		'rna':r,
		'mouse':m
	}, context_instance=RequestContext(request))


def lab_members(request):
	"""
	Page listing all lab members
	"""
	# current lab members must be ordered by position to utilize "group by" in template
	current = UserProfile.objects.all().filter(is_current=True).order_by(
		'position__display_order',
		'user__last_name'
	)

	former = UserProfile.objects.all().filter(is_current=False).order_by(
		'user__last_name'
	)

	column_length = math.ceil(len(former) / 3.0)
	print column_length

	return render_to_response('lab_members.html', {
		'current':current,
		'former':former,
		'column_length':column_length,
	}, context_instance=RequestContext(request))


def lab_member(request, username):
	"""
	Page for each lab member.
	Note: avoid 'user' as variable name to avoid conflict with the global variable
	(which is referenced for authentication purposes)
	"""
	member = get_object_or_404(User, username=username)
	return render_to_response('lab_member.html', {
		'member':member,
	}, context_instance=RequestContext(request))


def resources(request):
	"""
	Resources Page
	"""
	r = Resource.objects.all()

	return render_to_response('resources.html', {
		'resources':r
	}, context_instance=RequestContext(request))


def contact(request):
	"""
	Contact Page
	"""
	return render_to_response('contact.html', context_instance=RequestContext(request))


def jobs(request):
	"""
	Jobs Page
	"""
	return render_to_response('jobs.html', context_instance=RequestContext(request))


def publications(request):
	"""
	Page for publications, fetched dynamically from PubMed
	PubMed search term:
	(Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author]) OR (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])
	"""
	xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=12Wu35auLMyC-bw6heubsB4Aa1vq6MH4xOLj1ILBD4Wimwikba")
	# used to work: xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=18qVEVbjJjoq2mO-bQKE6E_-D4pje3l2O5Jd1cFE70SdwIYw_1")
	# used to work: xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1v9I1sARILc4F30I7IyGwVTatLAIvtPsS641znyxpiAdx0xgXy")

	# fxns to bolden or italicize a search term in a string
	def embolden(s, term):
		return string.replace(s, term, "<b>" + term + "</b>")

	def italicize(s, term):
		return string.replace(s, term, "<i>" + term + "</i>")

	# empty lists to fill with publications from the xml file
	pub_both = []
	pub_kris = []
	pub_fabio = []

	# create tree of the xml file tags, and iterate over the items/publications
	tree = ET.parse(xml_file)
	root = tree.getroot()
	for publication in root.iter('item'):
		# extract the description for manipulation
		d = publication.find('description').text

		# italicize species names
		d = string.replace(d, "Caenorhabditis  elegans", "Caenorhabditis elegans")
		d = italicize(d, "Caenorhabditis elegans")
		d = italicize(d, "C. elegans")
		d = italicize(d, "Drosophila")
		d = italicize(d, "Protorhabditis")
		d = italicize(d, "S. cerevisiae")

		# embolden PI names, and add the publication to PI-specific lists
		if "Piano F" in d:
			pub_fabio.append(publication)
			d = embolden(d, "Piano F")
		if "Gunsalus K" in d:
			pub_kris.append(publication)
			d = embolden(d, "Gunsalus KC")
			d = embolden(d, "Gunsalus K")

		# update the description, and add to the list for both PIs
		publication.description = d
		pub_both.append(publication)

	return render_to_response('publications.html', {
		'pub_both':pub_both,
		'pub_kris':pub_kris,
		'pub_fabio':pub_fabio,
	}, context_instance=RequestContext(request))


@login_required
def lab_tools(request):
	"""
	Internal Lab Tools landing page
	"""
	# render page
	return render_to_response('lab_tools.html', context_instance=RequestContext(request))
