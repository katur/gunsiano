from __future__ import division # force float division
from itertools import chain
import math
import urllib2
import string
import xml.etree.ElementTree as ET

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from website.models import (JoinLabSection, ResearchArea, Resource, User,
                            UserProfile)


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

    dictionary = {
        'network': n,
        'cell': c,
        'evolution': e,
        'gi': g,
        'rna': r,
        'mouse': m,
        'fabio': fabio,
        'kris': kris,
    }
    return render_to_response('home.html', dictionary,
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

    dictionary = {
        'current': current,
        'former': former,
        'former_column_length': former_column_length,
    }
    return render_to_response('lab_members.html', dictionary,
                              context_instance=RequestContext(request))


def lab_member(request, username):
    """
    Page for each lab member.
    Note: avoid 'user' as variable name to avoid conflict with the global
    variable (which is referenced for authentication purposes)
    """
    member = get_object_or_404(User, username=username)

    dictionary = {
        'member': member,
    }
    return render_to_response('lab_member.html', dictionary,
                              context_instance=RequestContext(request))


def resources(request):
    """
    Resources Page
    """
    r = Resource.objects.all()

    dictionary = {
        'resources': r,
    }
    return render_to_response('resources.html', dictionary,
                              context_instance=RequestContext(request))


def publications(request):
    """
    Page for publications, fetched dynamically from PubMed.
    PubMed search term:
    (Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author]) OR
      (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])
    """
    xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/"
                               "erss.cgi?rss_guid=12Wu35auLMyC-bw6heubsB4Aa"
                               "1vq6MH4xOLj1ILBD4Wimwikba")
    # NOTE: below used to work; not sure why they stopped
    # xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/"
    #   "erss.cgi?rss_guid=18qVEVbjJjoq2mO-bQKE6E_-D4pje3l2O5Jd1cFE70SdwIYw_1")
    # xml_file = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/entrez/eutils/"
    #   "erss.cgi?rss_guid=1v9I1sARILc4F30I7IyGwVTatLAIvtPsS641znyxpiAdx0xgXy")

    def embolden(s, term):
        return string.replace(s, term, "<b>{0}</b>".format(term))

    def italicize(s, term):
        return string.replace(s, term, "<i>{0}</i>".format(term))

    # Lists to populate with publications from the xml file
    pub_both = []
    pub_kris = []
    pub_fabio = []

    tree = ET.parse(xml_file)
    root = tree.getroot()
    for publication in root.iter('item'):
        d = publication.find('description').text

        # Italicize species names
        d = string.replace(d, "Caenorhabditis  elegans",
                           "Caenorhabditis elegans")
        d = italicize(d, "Caenorhabditis elegans")
        d = italicize(d, "C. elegans")
        d = italicize(d, "Drosophila")
        d = italicize(d, "Protorhabditis")
        d = italicize(d, "S. cerevisiae")

        if "Piano F" in d:
            pub_fabio.append(publication)
            d = embolden(d, "Piano F")
        if "Gunsalus K" in d:
            pub_kris.append(publication)
            d = embolden(d, "Gunsalus KC")
            d = embolden(d, "Gunsalus K")

        publication.description = d
        pub_both.append(publication)

    dictionary = {
        'pub_both': pub_both,
        'pub_kris': pub_kris,
        'pub_fabio': pub_fabio,
    }
    return render_to_response('publications.html', dictionary,
                              context_instance=RequestContext(request))


def join(request):
    """
    Join the Lab Page
    """
    sections = JoinLabSection.objects.all().order_by('display_order')
    jessica = get_object_or_404(User, username='jessica')

    dictionary = {
        'sections': sections,
        'jessica': jessica,
    }
    return render_to_response('join.html', dictionary,
                              context_instance=RequestContext(request))


def contact(request):
    """
    Contact Page
    """
    fabio = get_object_or_404(User, username='fabio')
    jessica = get_object_or_404(User, username='jessica')
    kris = get_object_or_404(User, username='kris')

    dictionary = {
        'kris': kris,
        'fabio': fabio,
        'jessica': jessica,
    }
    return render_to_response('contact.html', dictionary,
                              context_instance=RequestContext(request))


@login_required
def lab_tools(request):
    """
    Internal Lab Tools landing page
    """
    return render_to_response('lab_tools.html',
                              context_instance=RequestContext(request))
