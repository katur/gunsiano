Lab Website and Organizational Tools
====================================

Django-based website for a _Caenorhabditis elegans_ genomics lab.

Click [here](https://www.lucidchart.com/documents/view/492c-0ebc-51d33178-9110-78400a001d4e) for database schema on Lucidchart.

See dependencies in `requirements.txt`. Some notes about these:
* `wsgiref` is part of the Python standard library, but appears in pip by
accident/default (this bug fixed in Python3.3)
* `Django` and `MySQL-Python`: straightforward
* `South` is for database migrations. Migrations will be built into Django 1.7.
* `mdx-smartypants` is a Python Markdown extension for nicer curly quotes
and proper em/en dashes. It requires `Markdown`, `namedentities`
and `guess-language-spirit`
* `python-slugify` is used to convert text to be url-safe (removing whitespace,
certain symbols, etc.). Used to turn protocol titles into urls. Requires
`Unidecode`

Public interface includes basic information about the lab and its research.
The pages are:
* home, with skrollr effects describing research areas for the lab
* lab members, which links to pages for individual lab members
* resources, which links to the lab's published computational resources
* publications
* join the lab
* contact

Logging in provides access to interfaces to navigate the following internal lab
databases:
* worm strains
* bacterial clones
* vectors and plasmids
* antibodies
* primers
* chemicals

Logging in also provides access to the Django admin interface,
where every user is minimally granted update privileges for limited
information about their own user and user profile.

Other access levels permit edit privileges for the public website copy,
for all lab personnel, or for various internal lab databases.
