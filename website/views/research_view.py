from django.template import RequestContext
from django.shortcuts import render_to_response

def research(request):
	"""
	Research Areas
	"""
	# render page
	return render_to_response('research.html', context_instance=RequestContext(request))
