from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import UserProfile

def lab_members(request):
	"""
	Page listing all lab members
	"""
	# get all lab members
	profiles = UserProfile.objects.all().order_by('-is_current', 'position__display_order', 'user__last_name')
	for profile in profiles:
		if profile.is_current:
			profile.display_position = profile.position.position
		else:
			profile.display_position = "Former Lab Member"

	return render_to_response('lab_members.html', {
		'profiles':profiles
	}, context_instance=RequestContext(request))
