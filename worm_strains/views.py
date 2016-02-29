from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from worm_strains.models import WormLab, WormStrain, WormStrainLine
from storage.models import Stock, Container


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
                    Q(name__icontains=term) |
                    Q(genotype__icontains=term) |
                    Q(remarks__icontains=term) |
                    Q(created_by__first_name__icontains=term) |
                    Q(created_by__last_name__icontains=term) |
                    Q(species__name__icontains=term)
                )

    worms = sorted(worms)

    return render(request, 'worms.html', {'worms': worms})


@login_required
def worm(request, name):
    """
    Page showing information on a particular worm strain.
    """
    worm = get_object_or_404(WormStrain, name=name)
    lines = (WormStrainLine.objects.filter(strain=worm)
             .order_by('date_received'))

    lab_code = worm.get_lab_code()
    if lab_code:
        worm.lab = WormLab.objects.filter(strain_code=lab_code).first()

    '''
    for line in lines:
        line.stocks = (Stock.objects
                       .filter(stockable=line.stockable)
                       .order_by('date_prepared'))

        for stock in line.stocks:
            # Get the tester thaws
            stock.thaw_80 = (Container.objects
                             .filter(stock=stock, parent=7).first())
            stock.thaw_N = (Container.objects
                            .filter(stock=stock, parent=8).first())

            # Get other thaws
            all_tubes = (Container.objects.filter(stock=stock)
                         .exclude(parent=7).exclude(parent=8))

            thawed_tubes = []
            unthawed_tubes = []

            for tube in all_tubes:
                tube.position = tube.get_overall_position()
                if tube.is_thawed:
                    thawed_tubes.append(tube)
                else:
                    unthawed_tubes.append(tube)

            stock.thawed_tubes = sorted(thawed_tubes,
                                        reverse=True,
                                        key=lambda x: x.position)
            stock.unthawed_tubes = sorted(unthawed_tubes,
                                          key=lambda x: x.position)
    '''

    context = {
        'worm': worm,
        'lines': lines,
    }

    return render(request, 'worm.html', context)
