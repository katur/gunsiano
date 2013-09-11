from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from protocols.models import *


@login_required
def protocols(request):
	"""
	Page listing protocols
	"""
	# get all worm strains
	protocols = Protocol.objects.all()

	# render page
	return render_to_response('protocols.html', {
		'protocols':protocols
	}, context_instance=RequestContext(request))


@login_required
def protocol(request, url_title):
	"""
	Page listing protocol
	"""
	# get all worm strains
	protocol = get_object_or_404(Protocol, url_title=url_title)

	# render page
	return render_to_response('protocol.html', {
		'protocol':protocol
	}, context_instance=RequestContext(request))
