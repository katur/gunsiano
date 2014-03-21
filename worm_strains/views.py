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

    # Lab determined from first 2+ letters of strain name
    if strain.is_properly_named():
        lab_code = strain.extract_lab_code()
        try:
            strain.lab = WormLab.objects.get(strain_code=lab_code)
        except WormLab.DoesNotExist:
            strain.lab = None

    for line in lines:
        line.stocks = (Stock.objects.filter(stockable=line.stockable)
                       .order_by('date_prepared'))

        for stock in line.stocks:
            # Get the tester thaws no matter what
            try:
                stock.thaw_80 = Container.objects.get(stock=stock, parent=7)
            except Container.DoesNotExist:
                stock.thaw_80 = None

            try:
                stock.thaw_N = Container.objects.get(stock=stock, parent=8)
            except Container.DoesNotExist:
                stock.thaw_N = None

            # Get only unthawed tubes for non-testers
            stock.tubes = (Container.objects
                           .filter(stock=stock, is_thawed=False)
                           .exclude(parent=7).exclude(parent=8))

            for tube in stock.tubes:
                # Get position inside the box
                position_in_box = "{0}{1}".format(
                    chr(tube.vertical_position + 64),
                    tube.horizontal_position
                )

                # Follow parent pointers for detailed position
                try:
                    tube.position = "{0} - Rack {1} - Box {2} - {3}".format(
                        tube.parent.parent.parent.name,
                        tube.parent.parent.name,
                        tube.parent.name,
                        position_in_box
                    )
                except AttributeError:
                    tube.position = position_in_box

                if tube.notes:
                    tube.position += ": " + tube.notes

            # Sort tubes by position
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
