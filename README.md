# Gunsiano Lab Website

Django-based website for a _Caenorhabditis elegans_ genomics lab.

The public interface inclues basic information about the lab and its research.

Logging in provides access to interfaces for various internal lab databases.

Logging in also provides access to the Django admin interface,
where every user is granted limited update privileges for their own user.
Other access levels grant privileges to edit the public website text,
lab personnel information, and/or various internal databases.

## Dependencies

Python version is listed in `runtime.txt`.

Package dependencies are listed in `requirements.txt`.

## Database

[Here](https://www.lucidchart.com/documents/view/492c-0ebc-51d33178-9110-78400a001d4e)
is the database schema on Lucidchart.

## Code

CSS is in SASS. Run
`sass -wc --style compressed universal/static/stylesheets/styles.sass`
to compile.
