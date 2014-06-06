import re

from django.contrib.auth.models import User
from django.db import models

from gunsiano.settings import MARKDOWN_PROMPT


class Position(models.Model):
    position = models.CharField(max_length=50)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order', 'position']

    def __unicode__(self):
        return self.position


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    position = models.ForeignKey(Position)

    # True for Abu Dhabi, False for NYC, null for both
    in_abu_dhabi = models.NullBooleanField()

    # Whether to show as 'current' on Lab Members page
    is_current = models.BooleanField(default=True)

    net_id = models.CharField(max_length=25, blank=True)
    url = models.URLField(blank=True)
    image_filename = models.CharField(max_length=100, blank=True)
    blurb = models.TextField('Blurb', help_text=MARKDOWN_PROMPT, blank=True)

    class Meta:
        verbose_name = 'Profile'
        ordering = ['user__first_name', 'user__last_name']

    def __unicode__(self):
        return self.user.get_full_name()

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
    hidden = models.BooleanField(default=False)

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
        terms = (
            'Caenorhabditis elegans',
            'Caenorhabditis briggsae',
            'Caenorhabditis',
            'C. elegans',
            'C. briggsae',
            'Protorhabditis',
            'S. cerevisiae',
            'Drosophila melanogaster',
            'Drosophila grimshawi',
            'Drosophila',
            'D. melanogaster',
            'D. grimshawi',
        )
        skeleton = '|'.join(['{}' for term in terms])
        pattern = skeleton.format(*terms)
        self.abstract = re.sub(pattern, '*\g<0>*', self.abstract)
        self.title = re.sub(pattern, '*\g<0>*', self.title)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def __str__(self):
        return str(self.pubmed_id)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        if self.pubmed_id < other.pubmed_id:
            return -1
        elif self.pubmed_id > other.pubmed_id:
            return 1
        else:
            return 0


class JoinLabSection(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)
    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.title
