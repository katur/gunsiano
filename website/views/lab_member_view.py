from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from website.models import User

def lab_member(request, username):
	"""
	Page for each lab member
	"""
	user = get_object_or_404(User, username=username)
	return render_to_response('lab_member.html', {
		'user':user,
	}, context_instance=RequestContext(request))
