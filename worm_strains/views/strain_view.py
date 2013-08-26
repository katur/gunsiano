from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from worm_strains.models import *

def strain(request, name):
	"""
	Page showing information on a particular worm strain.
	"""
	strain_name = get_object_or_404(WormStrain, name=name)
	return render_to_response('strain.html', {
		'strain_name':name
	}, context_instance=RequestContext(request))
