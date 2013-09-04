from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from storage.models import *

def storage(request):
	"""
	Page showing all available vats
	"""
	vats = Container.objects.all().filter(parent_id__isnull=True)

	# render page
	return render_to_response('storage.html', {
		'vats':vats
	}, context_instance=RequestContext(request))


def storage_detail(request, parent_container_id):
	"""
	Page showing the contents of some parent container
	"""
	parent_container = get_object_or_404(Container, id=parent_container_id)

	parent_temp = parent_container
	title = parent_temp.type.supertype.name + " " + parent_temp.name
	while parent_temp.parent:
		parent_temp = parent_temp.parent
		title = parent_temp.type.supertype.name + " " + parent_temp.name + " -> " + title


	containers = Container.objects.all().filter(parent_id=parent_container)

	grid = [
		[list() for i in range(parent_container.type.slots_horizontal)]
		for j in range(parent_container.type.slots_vertical)
	]

	for container in containers:
		(grid[container.vertical_position-1][container.horizontal_position-1]).append(container)


	# render page
	return render_to_response('storage_detail.html', {
		'title':title,
		'parent_container':parent_container,
		'containers':containers,
		'vertical_range':range(parent_container.type.slots_vertical),
		'horizontal_range':range(parent_container.type.slots_horizontal),
		'grid':grid,
		'container_title':title,
	}, context_instance=RequestContext(request))
