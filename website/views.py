# Create your views here.
from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from django.db.models import Q # enables AND and OR in SQL filters
from website.models import *

def home(request):
	"""
	Homepage
	"""
	# render page
	return render_to_response('home.html', context_instance=RequestContext(request))

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

def lab_member(request, last_name):
	"""
	Page for each lab member
	"""
	member = get_object_or_404(Person, last_name = last_name)
	return render_to_response('lab_member.html', {
		'member': member,
	}, context_instance=RequestContext(request))
