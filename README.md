# Gunsiano Lab Website

Website for a _Caenorhabditis elegans_ genomics lab.


## Features

The public interface gives basic information about the lab and its research.

Logging in provides interfaces for various internal lab databases.

Logging in also provides access to the Django admin, where every user
is granted limited update privileges for their own user.
Other access levels grant privileges to edit other users' information,
the public website text, and various internal databases.

While simple database updates can be accomplished via the admin interface,
there are management scripts to accomplish more complex, routine updates.
The code for these scripts live in the standard location:
`app_name/management/commands/script_name.py`.
To list these scripts:

```
./manage.py help
```

For help on how to run a particular script:

```
./manage.py help script_name
```


## Installation

See [INSTALL.md](INSTALL.md) for sample Ubuntu deployment steps.


## Dependencies

Python version is listed in [runtime.txt](runtime.txt).

Python package dependencies, including Django,
are listed in [requirements.txt](requirements.txt).


## Database

[Click here](https://www.lucidchart.com/documents/view/492c-0ebc-51d33178-9110-78400a001d4e)
to view the database schema on Lucidchart.


## Code

Code is in Python, using the Django web framework.

CSS is in [SASS](http://sass-lang.com/). Run
`sass -wc --style compressed universal/static/stylesheets/styles.sass`
to compile.

Javascript in [jQuery](http://jquery.com/).
