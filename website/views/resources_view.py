from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import Resource

def resources(request):
	"""
	Resources Page
	"""
	r = Resource.objects.all().order_by('name')

	return render_to_response('resources.html', {
		'resources':r
	}, context_instance=RequestContext(request))
