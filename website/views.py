# to force float division
from __future__ import division
from itertools import chain
import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from website.models import (JoinLabSection, ResearchArea, Resource,
                            Publication, User, UserProfile)


def home(request):
    """
    Homepage
    """
    html_names = {
        1: 'network',
        2: 'cell',
        3: 'evolution',
        4: 'gi',
        5: 'rna',
        6: 'mouse',
    }

    display_order = {
        'network': 2,
        'cell': 4,
        'evolution': 5,
        'gi': 1,
        'rna': 3,
        'mouse': 6,
    }

    research_areas = ResearchArea.objects.all()
    for area in research_areas:
        area.html_name = html_names[area.id]
        area.display_order = display_order[area.html_name]

    research_areas = sorted(research_areas,
                            key=lambda x: display_order[x.html_name])

    kris = get_object_or_404(User, username='kris')
    fabio = get_object_or_404(User, username='fabio')

    template_dictionary = {
        'research_areas': research_areas,
        'fabio': fabio,
        'kris': kris,
    }
    return render_to_response('home.html', template_dictionary,
                              context_instance=RequestContext(request))


def people(request):
    """
    Page listing all people in the lab
    """
    # Order current people by position (for 'group by' in template)
    current = (UserProfile.objects.all()
               .filter(display_on_website=True,
                       is_current=True)
               .order_by('position', 'user__last_name',
                         'user__first_name'))

    # Order former lab members alphabetically
    former = (UserProfile.objects.all()
              .filter(display_on_website=True,
                      is_current=False)
              .order_by('user__last_name', 'user__first_name'))

    all_people = list(chain(current, former))
    for person in all_people:
        person.location = person.get_location()

    current_positions = set()
    for person in current:
        current_positions.add(person.position)

    num_columns = 3
    former_column_length = math.ceil(len(former) / num_columns)
    current_column_length = math.ceil(len(current_positions) / num_columns)

    template_dictionary = {
        'current': current,
        'former': former,
        'former_column_length': former_column_length,
        'current_column_length': current_column_length,
    }
    return render_to_response('people.html', template_dictionary,
                              context_instance=RequestContext(request))


def person(request, username):
    """
    Page for each lab member.
    Note: avoid 'user' as variable name to avoid conflict with the global
    variable (which is referenced for authentication purposes)
    """
    person = get_object_or_404(User, username=username)

    template_dictionary = {
        'person': person,
    }
    return render_to_response('person.html', template_dictionary,
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
    publications = sorted(Publication.objects.filter(hidden=False),
                          reverse=True)
    for publication in publications:
        publication.translate_html_br_to_markdown()
        publication.embolden_PI_names()
        publication.italicize_species_names()

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
