from django.core.management.base import BaseCommand

from worm_strains.models import WormStrain, WormStrainLine
from storage.models import (StockableType, Stockable, Stock,
                            ContainerType, Container)

import csv
import re


class Command(BaseCommand):
    """
    Run as: ./manage.py insert_new_MMP_racks filename.csv
    """
    help = ('Update WormStrain, WormStrainLine, Stockable, Stock, and '
            'Container tables to reflect newly received MMP strains')

    def handle(self, *args, **options):
        worm_stockable_type = StockableType.objects.get(name='worm strain')
        well_container_type = ContainerType.objects.get(name='well')

        parent_containers = Container.objects.filter(
            name__startswith='MMP Rack')
        parents = {}
        for parent in parent_containers:
            number = int(re.search('\d+', parent.name).group(0))
            parents[number] = parent

        filename = args[0]
        with open(filename, 'rU') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # skip header row
            for row in csvreader:
                if row[0].strip():  # skip any blank rows
                    strain_name = row[0]
                    rack_number = int(row[2])
                    parent_container = parents[rack_number]
                    position = row[3]
                    vertical_position = ord(position[0].lower()) - 96
                    horizontal_position = int(position[1:])

                    try:
                        strain = WormStrain.objects.get(name=strain_name)
                        self.stdout.write('Not adding ' + strain.name +
                                          ' to WormStrain (already present)')
                    except WormStrain.DoesNotExist:
                        strain = WormStrain(
                            name=strain_name,
                            on_wormbase=1,
                            genotype='Whole-genome sequenced strain',
                            remarks=('[MMP project website]'
                                     '(http://genome.sfu.ca/mmp/search.html'
                                     ' "MMP Project website")'))
                        strain.save()

                    stockable = Stockable(type=worm_stockable_type)
                    stockable.save()

                    previous_lines = WormStrainLine.objects.filter(
                        strain=strain)
                    if previous_lines:
                        self.stdout.write('Warning: ' + strain.name +
                                          ' has ' + str(len(previous_lines)) +
                                          ' lines in db that were entered' +
                                          ' previously')

                    line = WormStrainLine(strain=strain,
                                          stockable=stockable,
                                          received_from='Mark Edgley')
                    line.save()

                    stock = Stock(stockable=stockable,
                                  notes='received frozen from Moerman lab')
                    stock.save()

                    container = Container(
                        type=well_container_type,
                        parent=parent_container,
                        vertical_position=vertical_position,
                        horizontal_position=horizontal_position,
                        stock=stock)
                    container.save()
