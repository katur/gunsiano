from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from storage.models import Container


@login_required
def storage(request):
    """
    Page showing all available vats
    """
    containers = Container.objects.filter(parent_id__isnull=True)
    context = {
        'containers': containers,
    }
    return render(request, 'storage.html', context)


@login_required
def container(request, container_id):
    """
    Page showing the contents of some container
    """
    container = get_object_or_404(Container, id=container_id)

    children = container.container_set.filter(is_thawed=0)

    # Create 3D grid to hold positioned children.
    # 3rd dimension is in case there are multiple objects within a
    # slot (e.g., multiple plates within a freezer rack slot)
    grid = [[list() for i in range(container.type.slots_horizontal)]
            for j in range(container.type.slots_vertical)]

    # Create list to hold unpositioned children.
    overflow_children = []

    for child in children:
        try:
            x = child.horizontal_position - 1  # Positions are 1-indexed
            y = child.vertical_position - 1
            (grid[y][x]).append(child)

        except IndexError:
            overflow_children.append(child)

    context = {
        'container': container,
        'grid': grid,
        'overflow_children': overflow_children,
    }

    return render(request, 'container.html', context)
