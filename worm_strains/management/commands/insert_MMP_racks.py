import argparse
import csv
import re

from django.core.management.base import BaseCommand, CommandError

from worm_strains.models import WormStrain, WormStrainLine
from storage.models import (StockableType, Stockable, Stock,
                            ContainerType, Container)


class Command(BaseCommand):
    """
    Add new MMP strains to the database.
    """
    help = ('Add new MMP strains to the database.')

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=argparse.FileType('r'),
                            help=('CSV of the strains in the new racks. '
                                  'Mark Edgley usually sends a Word '
                                  'document with a table, which we '
                                  'copy/paste into a Google Spreadsheet. '
                                  'This can be exported as a CSV.'))

    def handle(self, **options):
        # Get database objects needed for foreign keys
        worm_stockable_type = StockableType.objects.get(name='worm strain')
        well_container_type = ContainerType.objects.get(name='well')

        # Create dictionary of the various parent containers
        parents = {}
        parent_containers = Container.objects.filter(
            name__startswith='MMP Rack').exclude(name__icontains='AD')

        for parent in parent_containers:
            number = int(re.search('\d+', parent.name).group(0))
            parents[number] = parent

        csvfile = options['input_file']
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            strain_name = row['Strain']

            # Skip blank rows
            if not strain_name:
                continue

            rack_number = int(row['Rack'])
            try:
                parent_container = parents[rack_number]
            except KeyError:
                raise CommandError('Must add MMP Racks to database first.'
                                   .format(rack_number))

            position = row['Slot']
            vertical_position = ord(position[0].lower()) - 96
            horizontal_position = int(position[1:])

            # Stop program if this rack/row/col has already been added to db
            if Container.objects.filter(
                    parent=parent_container,
                    horizontal_position=horizontal_position,
                    vertical_position=vertical_position).exists():
                raise CommandError(
                    '{}, row {}, col {} already exists in database'
                    .format(parent_container, horizontal_position,
                            vertical_position))

            # TODO: could use Django's get_or_create method here
            try:
                # There are a few cases where the lab received an MMP strain
                # individually from the CGC, so the WormStrain is already
                # in the database.
                strain = WormStrain.objects.get(name=strain_name)
                self.stdout.write('Warning: Not adding ' + strain.name +
                                  ' to WormStrain table (already present)')

            except WormStrain.DoesNotExist:
                strain = WormStrain(
                    name=strain_name,
                    on_wormbase=1,
                    genotype='Whole-genome sequenced strain',
                    remarks=('[MMP project website]'
                             '(http://genome.sfu.ca/mmp/search.html'
                             ' "MMP Project website")'))
                strain.save()

            previous_lines = WormStrainLine.objects.filter(
                strain=strain)

            if previous_lines:
                self.stdout.write('Warning: ' + strain.name +
                                  ' has ' + str(len(previous_lines)) +
                                  ' lines in db that were entered' +
                                  ' previously')

            stockable = Stockable(type=worm_stockable_type)
            stockable.save()

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
