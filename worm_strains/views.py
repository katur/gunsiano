from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from worm_strains.models import WormLab, WormStrain


@login_required
def worms(request):
    """
    Page listing worms strains.
    """
    worms = WormStrain.objects.all()

    if 'query' in request.GET:
        # Whitespace-separated terms need be present, not necessarily adjacent
        terms = request.GET['query'].split()
        if 'not_frozen' in terms:
            worms = [worm for worm in worms if not worm.is_frozen()]
        else:
            for term in terms:
                worms = worms.filter(
                    Q(id__icontains=term) |
                    Q(genotype__icontains=term) |
                    Q(remarks__icontains=term) |
                    Q(created_by__first_name__icontains=term) |
                    Q(created_by__last_name__icontains=term) |
                    Q(species__name__icontains=term)
                )

    worms = sorted(worms)

    return render(request, 'worms.html', {'worms': worms})


@login_required
def worm(request, id):
    """
    Page showing information on a particular worm strain.
    """
    worm = get_object_or_404(WormStrain, id=id)

    lines = worm.wormstrainline_set.order_by('date_received')

    lab_code = worm.get_lab_code()
    if lab_code:
        worm.lab = WormLab.objects.filter(strain_code=lab_code).first()

    for line in lines:
        line.stocks = line.stock_set.order_by('date_prepared')

        for stock in line.stocks:
            tubes = stock.container_set.all()

            thawed_tubes = []
            unthawed_tubes = []

            for tube in tubes:
                tube.position = tube.get_ancestry_string(position=True)

                if tube.is_thawed:
                    thawed_tubes.append(tube)
                else:
                    unthawed_tubes.append(tube)

            stock.thawed_tubes = thawed_tubes
            stock.unthawed_tubes = unthawed_tubes

    context = {
        'worm': worm,
        'lines': lines,
    }

    return render(request, 'worm.html', context)
