# to force float division
from __future__ import division
from itertools import chain
import math
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from website.models import (JoinLabSection, ResearchArea, Resource,
                            Publication, User, UserProfile)


def home(request):
    """
    Homepage
    """
    n = get_object_or_404(ResearchArea, id=1)
    c = get_object_or_404(ResearchArea, id=2)
    e = get_object_or_404(ResearchArea, id=3)
    g = get_object_or_404(ResearchArea, id=4)
    r = get_object_or_404(ResearchArea, id=5)
    m = get_object_or_404(ResearchArea, id=6)
    kris = get_object_or_404(User, username='kris')
    fabio = get_object_or_404(User, username='fabio')

    template_dictionary = {
        'network': n,
        'cell': c,
        'evolution': e,
        'gi': g,
        'rna': r,
        'mouse': m,
        'fabio': fabio,
        'kris': kris,
    }
    return render_to_response('home.html', template_dictionary,
                              context_instance=RequestContext(request))


def lab_members(request):
    """
    Page listing all lab members
    """
    # Order current lab members by position (for "group by" in template)
    current = (UserProfile.objects.all()
               .filter(user__is_active=True, is_current=True)
               .order_by('position__display_order', 'user__last_name',
                         'user__first_name'))
    former = (UserProfile.objects.all()
              .filter(user__is_active=True, is_current=False)
              .order_by('user__last_name', 'user__first_name'))

    all_members = list(chain(current, former))
    for member in all_members:
        member.location = member.get_location()

    num_former_columns = 3
    former_column_length = math.ceil(len(former) / num_former_columns)

    template_dictionary = {
        'current': current,
        'former': former,
        'former_column_length': former_column_length,
    }
    return render_to_response('lab_members.html', template_dictionary,
                              context_instance=RequestContext(request))


def lab_member(request, username):
    """
    Page for each lab member.
    Note: avoid 'user' as variable name to avoid conflict with the global
    variable (which is referenced for authentication purposes)
    """
    member = get_object_or_404(User, username=username)

    template_dictionary = {
        'member': member,
    }
    return render_to_response('lab_member.html', template_dictionary,
                              context_instance=RequestContext(request))


def resources(request):
    """
    Resources Page
    """
    r = Resource.objects.all()

    template_dictionary = {
        'resources': r,
    }
    return render_to_response('resources.html', template_dictionary,
                              context_instance=RequestContext(request))


def publications(request):
    """
    Publications page
    """
    publications = Publication.objects.filter(hidden=False)

    def italicize_all_species(text):
        species = (
            ('C', 'elegans'),
            ('C', 'briggsae'),
            ('S', 'cerevisiae'),
            ('D', 'melanogaster'),
            ('D', 'grimshawi'),
        )
        re_terms = []
        for s in species:
            re_terms.append(get_species_re(*s))

        # Add any other terms to italicize (e.g. genus only cases)
        re_terms.append(r'Protorhabditis')
        re_terms.append(r'Drosophila')

        re_pattern = '|'.join(['{}' for t in re_terms])
        re_net = re_pattern.format(*(tuple(re_terms)))
        species_found = re.findall(re_net, text)
        for s in species_found:
            text = italicize(s, text)
        return text

    for publication in publications:
        publication.title = italicize_all_species(publication.title)
        publication.abstract = italicize_all_species(publication.abstract)
        if 'Piano F' in publication.authors:
            publication.authors = embolden('Piano F', publication.authors)
        if 'Gunsalus K' in publication.authors:
            publication.authors = embolden('Gunsalus KC', publication.authors)
            publication.authors = embolden('Gunsalus K', publication.authors)

    template_dictionary = {
        'publications': publications,
    }
    return render_to_response('publications.html', template_dictionary,
                              context_instance=RequestContext(request))


def join(request):
    """
    Join the Lab Page
    """
    sections = JoinLabSection.objects.all().order_by('display_order')
    jessica = get_object_or_404(User, username='jessica')

    template_dictionary = {
        'sections': sections,
        'jessica': jessica,
    }
    return render_to_response('join.html', template_dictionary,
                              context_instance=RequestContext(request))


def contact(request):
    """
    Contact Page
    """
    fabio = get_object_or_404(User, username='fabio')
    jessica = get_object_or_404(User, username='jessica')
    kris = get_object_or_404(User, username='kris')

    template_dictionary = {
        'kris': kris,
        'fabio': fabio,
        'jessica': jessica,
    }
    return render_to_response('contact.html', template_dictionary,
                              context_instance=RequestContext(request))


@login_required
def lab_tools(request):
    """
    Internal Lab Tools landing page
    """
    return render_to_response('lab_tools.html',
                              context_instance=RequestContext(request))


def embolden(term, s):
    """
    Make bold for HTML all occurrences of 'term' in string 's'
    """
    return s.replace(term, '<b>{0}</b>'.format(term))


def italicize(term, s):
    """
    Italicize for HTML all occurrences of 'term' in string 's'
    """
    return s.replace(term, '<i>{0}</i>'.format(term))


def get_species_re(first_letter_genus, species):
    """
    Get a regular expression for a particular species from
    the first letter of its genus and its exact species name.

    For example, with arguments 'C' and 'elegans',
    the resulting regex will match the common cases 'C. elegans'
    and 'Caenorhabditis elegans'.
    In addition, it will accommodate 'C elegans' (no period),
    any number of lowercase letters directly following the 'C'
    (e.g. misspelled 'Ceanorhabditis elegans'),
    and repeated spaces directly preceding 'elegans'
    (e.g. C.    elegans).
    """
    return r'{0}[\.a-z]*[ ]*{1}'.format(first_letter_genus, species)
