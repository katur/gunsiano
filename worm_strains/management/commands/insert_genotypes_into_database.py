from django.core.management.base import BaseCommand, CommandError
from polls.models import Poll


def insert_generated_genotypes_into_database():
        strains = WormStrain.objects.all().exclude(parent_strain__exact='').exclude(transgene__exact='')
        i = 0
        for strain in strains:
                generate_genotype(strain)
                print strain.genotype
                i += 1
