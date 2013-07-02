from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from website.models import *

def home(request):
	"""
	Homepage
	"""
	# render page
	return render_to_response('home.html', context_instance=RequestContext(request))
