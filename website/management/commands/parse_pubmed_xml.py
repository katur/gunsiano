import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError
from website.models import Publication


class Command(BaseCommand):
    """
    Parse the publications from the XML output for a PubMed search,
    adding these publications to the database.

    This used to be done dynamically, but the RSS feed would eventually
    break and show only a portion of the publications, so we decided to
    instead hardcode our publications in a database.

    Search term used in PubMed:
    (Piano F[Author]
    NOT De Piano F[Author] NOT Del Piano F[Author])
    OR
    (Gunsalus K[Author] OR Gunsalus KC[Author]
    NOT GunsalusKT[Author]).

    Required some filtering afterward of additional Pianos and Gunsaluses
    """
    def handle(self, *args, **options):
        xml_filepath = args[0]
        tree = ET.parse(xml_filepath)
        root = tree.getroot()

        for publication in root.iter('item'):
            title = publication.find('title').text
            authors = publication.find('author').text
            journal = publication.find('category').text

            pubmed_string = publication.find('guid').text
            pubmed_id = int(pubmed_string.split(':')[1])

            description = publication.find('description').text
            description_title = (description.split('<p><b>')[1]
                                 .split('</b></p>')[0])
            assert title == description_title
            description = description.split(description_title)[1]

            journal_line = description.split('<p>')[1].split('</p>')[0]
            description_journal = journal_line.split('.')[0]
            assert journal == description_journal
            date = journal_line.split('. ')[1].split(';')[0]
            journal_detail = journal_line.split(';')[1].split('</p>')[0]

            description_authors = (description.split('Authors: ')[1]
                                   .split('</p>')[0])
            assert authors == description_authors

            abstract = description.split('<p>Abstract<br/>')
            if len(abstract) > 1:
                abstract = abstract[1].split('<br/>')[0].strip()
            else:
                abstract = ''

            entry = Publication(pubmed_id=pubmed_id, title=title, authors=authors,
                                abstract=abstract, journal=journal, date=date,
                                detail=journal_detail)
            entry.save()
