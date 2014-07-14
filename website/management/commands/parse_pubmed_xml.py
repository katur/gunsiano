import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from website.models import Publication


class Command(BaseCommand):
    """
    Run as: ./manage.py parse_pubmed_xml filename.xml

    Parse the publications from the XML output for a PubMed search,
    adding these publications to the database.

    Search term used in PubMed:
    (Piano F[Author] NOT De Piano F[Author] NOT Del Piano F[Author])
    OR
    (Gunsalus K[Author] OR Gunsalus KC[Author] NOT Gunsalus KT[Author])

    Even with these exceptions, some other Pianos and Gunsaluses show
    up in the results, which should be flagged to not display in the database.
    """
    def handle(self, *args, **options):
        filename = args[0]
        tree = ET.parse(filename)
        root = tree.getroot()
        recorded_publications = Publication.objects.all()
        recorded_pubmed_ids = set()
        for publication in recorded_publications:
            recorded_pubmed_ids.add(publication.pubmed_id)

        for publication in root.iter('item'):
            title = publication.find('title').text.strip()
            authors = publication.find('author').text.strip()
            journal = publication.find('category').text.strip()

            pubmed_string = publication.find('guid').text.strip()
            pubmed_id = int(pubmed_string.split(':')[1])

            description = publication.find('description').text.strip()
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
                abstract = abstract[1]
                abstract = abstract.split('</p>')[0].strip()
                abstract = abstract.rpartition('<br/>')[0].strip()
            else:
                abstract = ''

            entry = Publication(pubmed_id=pubmed_id, title=title,
                                authors=authors, abstract=abstract,
                                journal=journal, date=date,
                                detail=journal_detail)

            if pubmed_id not in recorded_pubmed_ids:
                entry.save()
