import re

from django.contrib.auth.models import User
from django.db import models

from gunsiano.settings import MARKDOWN_PROMPT


class Position(models.Model):
    position = models.CharField(max_length=50)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order', 'position']
        verbose_name_plural = 'lab member positions'

    def __unicode__(self):
        return self.position


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    position = models.ForeignKey(Position, models.CASCADE)

    # True for Abu Dhabi, False for NYC, null for both
    in_abu_dhabi = models.NullBooleanField()

    # Whether to show on Lab Members page
    display_on_website = models.BooleanField(default=True)

    # Whether to show as 'current' on Lab Members page
    is_current = models.BooleanField(default=True)

    net_id = models.CharField('NYU NetID', max_length=25, blank=True)
    url = models.URLField('Personal website URL', help_text='Your public'
                          ' profile will redirect to this URL if your blurb'
                          ' is empty.',
                          blank=True)
    image_filename = models.CharField(max_length=100, blank=True)
    blurb = models.TextField('Blurb about yourself',
                             help_text=MARKDOWN_PROMPT, blank=True)

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
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'research area blurbs'

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=40, unique=True)
    display_order = models.PositiveSmallIntegerField()
    logo_filename = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=100, blank=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.name


class Publication(models.Model):
    pubmed_id = models.PositiveIntegerField(null=True, blank=True)
    title = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    journal = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=30, blank=True)
    detail = models.CharField(max_length=60, blank=True)
    hidden = models.BooleanField('Hide?', default=False)

    def translate_html_br_to_markdown(self):
        html_line_break_tags = ('<br>', '<br/>')
        for tag in html_line_break_tags:
            self.abstract = self.abstract.replace(tag, '  ')

    def embolden_PI_names(self):
        def embolden(term, s):
            return s.replace(term, '**{0}**'.format(term))

        if 'Piano F' in self.authors:
            self.authors = embolden('Piano F', self.authors)

        if 'Gunsalus KC' in self.authors:
            self.authors = embolden('Gunsalus KC', self.authors)
        elif 'Gunsalus K' in self.authors:
            self.authors = embolden('Gunsalus K', self.authors)

    def italicize_species_names(self):
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

    def split_pubmed_date(self):
        parts = self.date.split()
        months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
                  'sep', 'oct', 'nov', 'dec')
        try:
            year = int(parts[0])
        except:
            year = 0

        try:
            month = months.index(parts[1].lower())
        except:
            month = 0

        try:
            day = int(parts[2])
        except:
            day = 0

        return (year, month, day)

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return self.__unicode__()

    def __cmp__(self, other):
        self_year, self_month, self_day = self.split_pubmed_date()
        other_year, other_month, other_day = other.split_pubmed_date()

        if self_year != other_year:
            return cmp(self_year, other_year)
        elif self_month != other_month:
            return cmp(self_month, other_month)
        else:
            return cmp(self_day, other_day)


class JoinLabSection(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.title
