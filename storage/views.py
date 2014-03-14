from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from storage.models import *
from worm_strains.models import *


@login_required
def storage(request):
  """
  Page showing all available vats
  """
  vats = Container.objects.all().filter(
      type_id__supertype_id__is_outermost=True)

  return render_to_response('storage.html', {
      'vats':vats
  }, context_instance=RequestContext(request))


@login_required
def storage_detail(request, container_id):
  """
  Page showing the contents of some container
  """
  container = get_object_or_404(Container, id=container_id)
  children = Container.objects.all().filter(parent_id=container, is_thawed=0)

  try:
    grid = [
        [list() for i in range(container.type.slots_horizontal)]
        for j in range(container.type.slots_vertical)
    ]

    for child in children:
      (grid[child.vertical_position-1][child.horizontal_position-1]).append(
          child)
      try:
        if child.stock.stockable.type.id == 1:
          child.strain = get_object_or_404(WormStrainLine,
              stockable=child.stock.stockable).strain
      except AttributeError:
        child.strain = None

  except AttributeError:
    grid = [[list()]]
    for child in children:
      grid[0][0].append(child)

  # generate page title
  temp = container
  try:
    title = """%s %s""" % ( temp.type.supertype.name, temp.name )
  except AttributeError:
    title = temp.name

  while temp.parent:
    temp = temp.parent
    try:
      title = """%s %s -> %s""" % ( temp.type.supertype.name, temp.name, title)
    except AttributeError:
      title = """%s -> %s""" % ( temp.name, title )

  return render_to_response('storage_detail.html', {
      'container':container,
      'container_title':title,
      'grid':grid,
  }, context_instance=RequestContext(request))
