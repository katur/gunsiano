from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from worm_strains.models import *

def strains(request):
	"""
	Page listing worms strains, with possible filtering
	"""
	# get all worm strains
	strains = WormStrain.objects.all().order_by('name')	

	# render page
	return render_to_response('strains.html', {
		'strains':strains
	}, context_instance=RequestContext(request))
