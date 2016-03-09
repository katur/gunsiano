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
def storage_detail(request, container_id):
    """
    Page showing the contents of some container
    """
    container = get_object_or_404(Container, id=container_id)

    unpositioned_children = container.container_set.filter(
        is_thawed=0, horizontal_position__isnull=True,
        vertical_position__isnull=True)

    positioned_children = container.container_set.filter(
        is_thawed=0, horizontal_position__isnull=False,
        vertical_position__isnull=False)

    # If the child has a stock, attach the actual instance of the
    # stockable that makes up that stock (i.e. the specific
    # WormStrainLine, Primer, Antibody, etc.)
    for child in unpositioned_children:
        if child.stock:
            child.stockable = child.stock.stockable.get_actual_instance()

    for child in positioned_children:
        if child.stock:
            child.stockable = child.stock.stockable.get_actual_instance()

    if not positioned_children:
        grid = [[[container]]]

    else:
        # Create an empty 3D grid.
        # 3rd dimension is in case there are multiple objects within a
        # slot (e.g., multiple plates within a freezer rack slot)
        grid = [[list() for i in range(container.type.slots_horizontal)]
                for j in range(container.type.slots_vertical)]

        # Populate the grid with this container's children
        for child in positioned_children:
            x = child.horizontal_position - 1  # Positions are 1-indexed
            y = child.vertical_position - 1

            (grid[y][x]).append(child)

    context = {
        'container': container,
        'grid': grid,
        'unpositioned_children': unpositioned_children,
    }

    return render(request, 'storage_detail.html', context)
