from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from storage.models import Container
from worm_strains.models import WormStrainLine


@login_required
def storage(request):
    """
    Page showing all available vats
    """
    containers = Container.objects.all().filter(parent_id__isnull=True)

    template_dictionary = {
        'containers': containers,
    }
    return render_to_response('storage.html', template_dictionary,
                              context_instance=RequestContext(request))


@login_required
def storage_detail(request, container_id):
    """
    Page showing the contents of some container
    """
    container = get_object_or_404(Container, id=container_id,
                                  type__slots_vertical__isnull=False,
                                  type__slots_horizontal__isnull=False)
    children = Container.objects.all().filter(parent_id=container, is_thawed=0)

    # Create an empty grid with this container's dimensions
    grid = [[list() for i in range(container.type.slots_horizontal)]
            for j in range(container.type.slots_vertical)]

    # Populate this grid with this container's children
    for child in children:
        x = child.horizontal_position - 1 # Position is 1-indexed
        y = child.vertical_position - 1
        (grid[y][x]).append(child)

        if child.has_children():
            child.has_children = True
        elif child.stock:
            s = child.stock.stockable
            if s.type.name == 'worm strain':
                line = get_object_or_404(WormStrainLine, stockable=s)
                child.worm = line.strain

    # Create title for this page
    title = str(container)
    temp = container
    while temp.parent:
        temp = temp.parent
        title = "{0} -> {1}".format(str(temp), title)

    template_dictionary = {
        'container': container,
        'container_title': title,
        'grid': grid,
    }
    return render_to_response('storage_detail.html', template_dictionary,
                              context_instance=RequestContext(request))
