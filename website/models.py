import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Position(models.Model):
    """
    A lab member position (e.g. Postdoc, Technician).
    """

    name = models.CharField(max_length=50)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'lab member positions'

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    """
    Supplemental information about Users (lab members) not included in
    the default Django User model.

    A UserProfile has a OneToOne relationship to the Django User model
    (i.e., it uses composition instead of inheritance).
    This is the preferred way of adding supplemental User information
    (extending the Django built-in model through inheritance tends
    to be sloppier).
    """

    user = models.OneToOneField(User, primary_key=True)
    position = models.ForeignKey(Position, models.CASCADE)

    # True for Abu Dhabi, False for NYC, null for both
    in_abu_dhabi = models.NullBooleanField()

    # Whether to show on Lab Members page
    display_on_website = models.BooleanField(default=True)

    # Whether to show as 'current' on Lab Members page
    is_current = models.BooleanField(default=True)

    net_id = models.CharField('NYU NetID', max_length=25, blank=True)
    url = models.URLField('Personal website URL', blank=True,
                          help_text='Your public profile will redirect '
                          'here if your blurb is empty.')

    image = models.ImageField(upload_to='people', null=True, blank=True)
    blurb = models.TextField('Blurb about yourself', blank=True,
                             help_text=settings.MARKDOWN_PROMPT)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __unicode__(self):
        return self.user.get_full_name()

    def __repr__(self):
        return self.__unicode__()

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_location(self):
        if self.in_abu_dhabi == 1:
            return 'NYUAD'
        elif self.in_abu_dhabi == 0:
            return 'NYUNY'
        else:
            return 'NYUAD/NY'


class ResearchArea(models.Model):
    """
    An area of research for the lab.

    These are the topics that display on the home page.
    """

    name = models.CharField(max_length=60, unique=True)
    description = models.TextField('Description',
                                   help_text=settings.MARKDOWN_PROMPT)
    display_order = models.PositiveSmallIntegerField()
    html_id = models.CharField(max_length=20, unique=True, null=True,
                               blank=True, editable=False)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'research area blurbs'

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    """
    A public resource of the lab (e.g. NBrowse).
    """

    name = models.CharField(max_length=40, unique=True)
    description = models.TextField('Description',
                                   help_text=settings.MARKDOWN_PROMPT)
    url = models.URLField(blank=True)
    display_order = models.PositiveSmallIntegerField()
    logo = models.ImageField(upload_to='resource_logos',
                             null=True, blank=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __unicode__(self):
        return self.name


class Publication(models.Model):
    """
    A publication by the lab.
    """

    pmid = models.PositiveIntegerField('PMID')

    # Many publications do not have a PMCID
    pmcid = models.CharField('PMCID', max_length=20, blank=True)

    title = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    journal = models.CharField(max_length=100, blank=True)

    # Usually a date, but sometimes a date range, or just a month
    issue = models.CharField(max_length=30, blank=True)

    # Extra details about the journal (e.g. page range)
    detail = models.CharField(max_length=60, blank=True)

    # Select to not show this publication on the website
    hidden = models.BooleanField('Hide?', default=False)

    class Meta:
        # PMIDs are assigned in ascending order, so this is like sorting
        # by date
        ordering = ['-pmid']

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return self.__unicode__()

    def get_pubmed_url(self):
        """
        Get the URL of this publication on PubMed.
        """
        if not self.pmid:
            return None
        return 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(self.pmid)

    def get_pmc_url(self):
        """
        Get the URL of this publication on PMC (free text).
        """
        if not self.pmcid:
            return None
        return 'http://www.ncbi.nlm.nih.gov/pmc/articles/{}/'.format(
            self.pmcid)

    def embolden_PI_names(self):
        """
        Make PI names bold in the authors field, with Markdown.
        """
        def embolden(term, s):
            return s.replace(term, '**{0}**'.format(term))

        if 'Piano F' in self.authors:
            self.authors = embolden('Piano F', self.authors)

        if 'Gunsalus KC' in self.authors:
            self.authors = embolden('Gunsalus KC', self.authors)
        elif 'Gunsalus K' in self.authors:
            self.authors = embolden('Gunsalus K', self.authors)

    def italicize_species_names(self):
        """
        Italicize species names in the abstracts, with Markdown.
        """
        species_dictionary = {
            'Caenorhabditis': (
                'elegans',
                'briggsae',
            ),
            'Protorhabditis': (
                '',
            ),
            'Saccharomyces': (
                'cerevisiae',
            ),
            'Drosophila': (
                'grimshawi',
                'melanogaster',
                'pseudoobscura',
            )
        }

        terms = []
        for genus, species_list in species_dictionary.iteritems():
            for species in species_list:
                if species:
                    terms.append(genus + ' ' + species)
                    terms.append(genus[0] + '. ' + species)
            terms.append(genus)

        pattern = '|'.join(terms)
        self.abstract = re.sub(pattern, '*\g<0>*', self.abstract)
        self.title = re.sub(pattern, '*\g<0>*', self.title)

    def get_split_date(self):
        """
        Get a tuple of (year, month, date), where each part is an integer,
        and 0 is used for the parts that do not exist.
        """
        parts = self.date.split()
        months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
                  'sep', 'oct', 'nov', 'dec')
        try:
            year = int(parts[0])
        except Exception:
            year = 0

        try:
            month = months.index(parts[1].lower())
        except Exception:
            month = 0

        try:
            day = int(parts[2])
        except Exception:
            day = 0

        return (year, month, day)


class JoinLabSection(models.Model):
    """
    A section on the "Join the Lab" page.
    """

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField('Description',
                                   help_text=settings.MARKDOWN_PROMPT)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order', 'title']

    def __unicode__(self):
        return self.title
