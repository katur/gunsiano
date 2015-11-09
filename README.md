# Gunsiano Lab Website

Website for a *Caenorhabditis elegans* genomics lab.


## Code

The project is organized the standard
[Django](https://www.djangoproject.com/) way, with most code in Python.

Python version is listed in [runtime.txt](runtime.txt).
Python package dependencies, including Django,
are listed in [requirements.txt](requirements.txt).

HTML is in the
[Django template language](https://docs.djangoproject.com/en/dev/topics/templates/).

CSS is in [SASS](http://sass-lang.com/).

Javascript in [jQuery](http://jquery.com/).

Managerial scripts live in the standard Django location:
`appname/management/commands/scriptname.py`, to be run with
`./manage.py scriptname`.

To browse these scripts, run `./manage.py help`.
For help on a particular script, run `./manage.py help scriptname`.


## Features

The public interface gives basic information about the lab and its research.

Logging in provides interfaces for various internal lab databases.

Logging in also provides access to the Django admin, where every user
is granted limited update privileges for their own user.
Other access levels grant privileges to edit other users' information,
the public website text, and various internal databases.


## Database

[Click here](https://www.lucidchart.com/documents/view/149b1a73-c8c0-46cf-bc42-2841b784b69a)
to view the database schema on Lucidchart
(or [here](https://www.lucidchart.com/publicSegments/view/3ce8642d-6d2d-4157-9c5e-e9bdd71d881e/image.pdf)
to download a PDF).


## Installation

See [INSTALL.md](INSTALL.md).
