from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from website.models import *

def home(request):
	"""
	Homepage
	"""
	# render page
	return render_to_response('home.html', context_instance=RequestContext(request))

def research(request):
	"""
	Research Areas
	"""
	# render page
	return render_to_response('research.html', context_instance=RequestContext(request))

def contact(request):
	"""
	Contact Page
	"""
	return render_to_response('contact.html', context_instance=RequestContext(request))

def lab_members(request):
	"""
	Page listing all lab members
	"""
	# get all lab members
	l = Person.objects.all()

	return render_to_response('lab_members.html', {'lab_members':l}, context_instance=RequestContext(request))

def lab_member(request, url_name):
	"""
	Page for each lab member
	"""
	person = get_object_or_404(Person, url_name=url_name)
	return render_to_response('lab_member.html', {
		'person': person,
	}, context_instance=RequestContext(request))
