from haystack import indexes
from worm_strains.models import WormStrain


class WormStrainIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # name = indexes.CharField(model_attr='name')
    # genotype = indexes.CharField(model_attr='genotype')
    # remarks = indexes.CharField(model_attr='remarks')

    def get_model(self):
        return WormStrain
