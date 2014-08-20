# Gunsiano Lab Website

Website for a _Caenorhabditis elegans_ genomics lab.

The public interface gives basic information about the lab and its research.

Logging in provides interfaces for various internal lab databases.

Logging in also provides access to the Django admin, where every user 
is granted limited update privileges for their own user.
Other access levels grant privileges to edit other users' information,
the public website text, and various internal databases.

While simple database updates can be accomplished via the admin interface,
there are scripts to accomplish more complicated, routine updates.
These scripts live in `app_name/management/commands/script_name.py`.

## Dependencies

Python version is listed in `runtime.txt`.

Package dependencies are listed in `requirements.txt`.

## Database

[Here](https://www.lucidchart.com/documents/view/492c-0ebc-51d33178-9110-78400a001d4e)
is the database schema on Lucidchart.

[South](http://south.readthedocs.org/en/latest/) is used for database migrations.

## Code

Django/Python. Scripts live in the standard location (an app's management/commands).

CSS is in [SASS](http://sass-lang.com/). Run
`sass -wc --style compressed universal/static/stylesheets/styles.sass`
to compile.

Javascript in [jQuery](http://jquery.com/).
