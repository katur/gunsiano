"""
NOTE: This script is antiquated in favor of adding new publications
individually through the Django admin.

Parsing the PubMed XML resulting from an author search has always
suffered from there being other scientists with the names F Piano
and K Gunsalus, which has made manual intervention necessary to
hide publications that are not really from our lab.

Additionally, PubMed's XML output does not include the PMCID, which
we would like in order to link directly to the free text. And, there
are sometimes other inconsistencies between the PubMed XML output and
what shows in the PubMed webpage. For example, PMID 26887572 shows in
the website as issue "2016 Feb 17", but in the XML as just "2016".

So, going forward, we will just enter our new publications through the
Django Admin, which is very easy. I am keeping this script around just
in case we ever need to batch process the PubMed output.
"""
import argparse
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from website.models import Publication


class Command(BaseCommand):
    """
    Parse the publications from the XML output from a PubMed search,
    adding these publications to the database.

    Search term used in PubMed:
    (Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author])
    OR
    (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])

    Even with these exceptions, some other Pianos and Gunsaluses show
    up in the results, which must be marked "hidden" to not display on
    the website. This can be done in the Django admin.
    """
    help = ('Parse a PubMed XML file of publications, adding new ones '
            'to the database. NOTE: since we starting wanting PMCID in '
            'the database, which is absent in the PubMed XML dump, we '
            'now prefer just using the Django Admin for adding new '
            'publications.')

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=argparse.FileType('r'),
                            help='PubMed XML file of publications.')

    def handle(self, **options):
        input_file = options['input_file']
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Create set of already-recorded PMIDs, to avoid adding them again
        recorded_publications = Publication.objects.all()
        recorded_pmids = set()
        for publication in recorded_publications:
            recorded_pmids.add(publication.pmid)

        for publication in root.iter('item'):
            pmid_string = publication.find('guid').text.strip()
            pmid = int(pmid_string.split(':')[1])
            if pmid in recorded_pmids:
                continue

            title = publication.find('title').text.strip()
            authors = publication.find('author').text.strip()
            journal = publication.find('category').text.strip()

            description = publication.find('description').text.strip()

            description_title = (description.split('<p><b>')[1]
                                 .split('</b></p>')[0].strip())

            # Sanity check that title matches that in description
            assert title == description_title

            description = description.split(description_title)[1].strip()

            journal_line = description.split('<p>')[1].split('</p>')[0].strip()
            description_journal = journal_line.split('.')[0].strip()

            # Sanity check that journal matches that in description
            assert journal == description_journal

            issue = journal_line.split('.')[1].split(';')[0].strip()
            detail = journal_line.split(';')[1].split('</p>')[0].strip()

            description_authors = (description.split('Authors:')[1]
                                   .split('</p>')[0].strip())

            # Sanity check that authors matches that in description
            assert authors == description_authors

            abstract = description.split('<p>Abstract<br/>')
            if len(abstract) > 1:
                abstract = abstract[1]
                abstract = abstract.split('</p>')[0].strip()
                abstract = abstract.rpartition('<br/>')[0].strip()
            else:
                abstract = ''

            entry = Publication(pmid=pmid, title=title,
                                authors=authors, abstract=abstract,
                                journal=journal, issue=issue,
                                detail=detail)
            entry.save()
