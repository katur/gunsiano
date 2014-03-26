from django.core.management.base import BaseCommand, CommandError

from worm_strains.models import WormStrain


class Command(BaseCommand):
    """
    Update worm strain genotypes in the database that are derived
    from the worm's background strain and transgene.

    WARNING: this modifies the database!! Please back up the database
    before running this program.

    Run with: ./manage.py insert_genotypes_into_database

    Any updated genotypes will print to standard output, along with
    total number of updates.
    """
    help = ('Update WormStrain table for genotypes based on '
            'parent strain, transgene, and the generate_genotype function')

    def handle(self, *args, **options):
        strains = WormStrain.objects.all()
        changed = 0
        for strain in strains:
            old_genotype = strain.genotype
            new_genotype = strain.generate_genotype()
            if new_genotype and new_genotype != old_genotype:
                strain.genotype = new_genotype
                strain.save()
                self.stdout.write('New genotype inserted: {0} was {1}, now {2}'
                                  .format(strain.name, old_genotype,
                                          new_genotype))
                changed += 1

        self.stdout.write('Total changed: {0}'.format(str(changed)))
