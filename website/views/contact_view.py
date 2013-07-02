from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from website.models import *

def contact(request):
	"""
	Contact Page
	"""
	return render_to_response('contact.html', context_instance=RequestContext(request))
