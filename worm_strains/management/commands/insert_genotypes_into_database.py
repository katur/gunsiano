from django.core.management.base import BaseCommand, CommandError

from worm_strains.models import WormStrain
from worm_strains.views import generate_genotype


class Command(BaseCommand):
    help = ("Updates strain database to add genotypes based on "
            "parent strain, transgene, and the generate_genotype function")

    def handle(self, *args, **options):
        strains = WormStrain.objects.all()
        i = 0
        for strain in strains:
            original_genotype = strain.genotype
            generate_genotype(strain)
            if original_genotype != strain.genotype:
                message = "Generated genotype is: {0}".format(strain.genotype)
                self.stdout.write(message)
                strain.save()
                i += 1

        self.stdout.write("Number of strains changed: {0}".format(str(i)))
