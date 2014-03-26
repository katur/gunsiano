from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from worm_strains.models import WormLab, WormStrain, WormStrainLine
from storage.models import Stock, Container


@login_required
def strains(request):
    """
    Page listing worms strains, with possible filtering
    """
    strains = WormStrain.objects.all()
    strains = sorted(strains)

    # The following lines dynamically generate the genotype, using the strain's
    # background and transgene. For performance reasons, the genotype
    # is now hard-coded into the database (done using this same
    # generate_genotype function, run as:
    # ./manage.py insert_genotypes_into_database

    # for strain in strains:
        # generate_genotype(strain)

    dictionary = {
        'strains': strains,
    }
    return render_to_response('strains.html', dictionary,
                              context_instance=RequestContext(request))


@login_required
def strain(request, name):
    """
    Page showing information on a particular worm strain.
    """
    strain = get_object_or_404(WormStrain, name=name)
    lines = (WormStrainLine.objects.filter(strain=strain)
             .order_by('date_received'))

    lab_code = strain.get_lab_code()
    if lab_code:
        strain.lab = WormLab.objects.filter(strain_code=lab_code).first()

    for line in lines:
        line.stocks = (Stock.objects
                       .filter(stockable=line.stockable)
                       .order_by('date_prepared'))

        for stock in line.stocks:
            # Get the tester thaws no matter what
            stock.thaw_80 = (Container.objects
                             .filter(stock=stock, parent=7).first())
            stock.thaw_N = (Container.objects
                            .filter(stock=stock, parent=8).first())

            # Get non-tester tubes only if unthawed
            stock.tubes = (Container.objects
                           .filter(stock=stock, is_thawed=False)
                           .exclude(parent=7).exclude(parent=8))

            for tube in stock.tubes:
                tube.position = tube.get_overall_position()
            stock.tubes = sorted(stock.tubes, key=lambda x: x.position)

    dictionary = {
        'lines': lines,
        'strain': strain,
    }
    return render_to_response('strain.html', dictionary,
                              context_instance=RequestContext(request))


def generate_genotype(strain):
    if strain.transgene and strain.parent_strain:
        vector = strain.transgene.vector
        strain.genotype = (strain.transgene.name + "[" +
            vector.parent_vector.genotype_pattern + "]")
        strain.genotype = strain.genotype.replace("gene", vector.gene)
        strain.genotype = strain.genotype.replace("promoter", vector.promoter)
        strain.genotype = strain.genotype.replace(
            "threePrimeUTR", vector.three_prime_utr)
        if strain.parent_strain.name == "DP38":
            strain.genotype = "unc-119(ed3) III; " + strain.genotype
