from django.template import RequestContext
from django.shortcuts import render_to_response

def contact(request):
	"""
	Contact Page
	"""
	return render_to_response('contact.html', context_instance=RequestContext(request))
