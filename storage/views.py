from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from storage.models import Container
from worm_strains.models import WormStrainLine


@login_required
def storage(request):
    """
    Page showing all available vats
    """
    containers = Container.objects.all().filter(parent_id__isnull=True)
    return render(request, 'storage.html', {'containers': containers})


@login_required
def storage_detail(request, container_id):
    """
    Page showing the contents of some container
    """
    container = get_object_or_404(Container, id=container_id,
                                  type__slots_vertical__isnull=False,
                                  type__slots_horizontal__isnull=False)
    children = Container.objects.all().filter(parent_id=container,
                                              is_thawed=0)

    # Create an empty 2D grid
    grid = [[list() for i in range(container.type.slots_horizontal)]
            for j in range(container.type.slots_vertical)]

    # Populate with this container's children
    for child in children:
        # position is 1-indexed
        x = child.horizontal_position - 1
        y = child.vertical_position - 1
        (grid[y][x]).append(child)

        if child.stock:
            s = child.stock.stockable
            if s.type.name == 'worm strain':
                line = get_object_or_404(WormStrainLine, stockable=s)
                child.worm = line.strain

    context = {
        'container': container,
        'grid': grid,
    }

    return render(request, 'storage_detail.html', context)
