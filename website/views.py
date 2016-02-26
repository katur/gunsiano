# to force float division
from __future__ import division
from itertools import chain
import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from website.models import (JoinLabSection, ResearchArea, Resource,
                            Publication, User, UserProfile)


def home(request):
    """
    Homepage
    """
    research_areas = ResearchArea.objects.all()
    kris = get_object_or_404(User, username='kris')
    fabio = get_object_or_404(User, username='fabio')

    context = {
        'research_areas': research_areas,
        'fabio': fabio,
        'kris': kris,
    }

    return render(request, 'home.html', context)


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

    context = {
        'current': current,
        'former': former,
        'former_column_length': former_column_length,
        'current_column_length': current_column_length,
    }

    return render(request, 'people.html', context)


def person(request, username):
    """
    Page for each lab member.
    Note: avoid 'user' as variable name to avoid conflict with the global
    variable (which is referenced for authentication purposes)
    """
    person = get_object_or_404(User, username=username)
    return render(request, 'person.html', {'person': person})


def resources(request):
    """
    Resources Page
    """
    resources = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources})


def publications(request):
    """
    Publications page
    """
    pubs = Publication.objects.exclude(hidden=True)

    for pub in pubs:
        pub.embolden_PI_names()
        pub.italicize_species_names()

    return render(request, 'publications.html', {'publications': pubs})


def join(request):
    """
    Join the Lab Page
    """
    sections = JoinLabSection.objects.all()
    jessica = get_object_or_404(User, username='jessica')

    context = {
        'sections': sections,
        'jessica': jessica,
    }

    return render(request, 'join.html', context)


def contact(request):
    """
    Contact Page
    """
    fabio = get_object_or_404(User, username='fabio')
    jessica = get_object_or_404(User, username='jessica')
    kris = get_object_or_404(User, username='kris')

    context = {
        'kris': kris,
        'fabio': fabio,
        'jessica': jessica,
    }

    return render(request, 'contact.html', context)


@login_required
def lab_tools(request):
    """
    Internal Lab Tools landing page
    """
    return render(request, 'lab_tools.html')
