# Installing `gunsiano` Project

1. [Development](#development)
1. [Production](#production)


## Development


#### Code

```
git clone https://github.com/katur/gunsiano.git
cd gunsiano/gunsiano
# add localsettings.py; set DEBUG=True
```


#### Database

Add dev database connection info to `gunsiano/localsettings.py`.
This might be a dev database that already exists on another machine,
or a new database on your own machine.
You might import an existing dump, or you might generate an empty database
from scratch with `./manage.py migrate`. Do whatever suits your needs.


#### Python Dependencies

Python version is listed in [runtime.txt](runtime.txt).

Python package dependencies, including Django,
are listed in [requirements.txt](requirements.txt).
These should be [pip](https://pypi.python.org/pypi/pip)-install into a fresh
[Python virtual environment](http://virtualenv.readthedocs.org/). I use
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
to make working with Python virtual environments easier.

In a nutshell (assuming pip, virtualenv, and virtualenvwrapper installed):
```
mkvirtualenv gunsiano
workon gunsiano
pip install -r requirements.txt

# To deactivate virtual environment
deactivate
```


#### SASS Compilation

To compile SASS to CSS:
```
sass -wc --style compressed website/static/stylesheets/styles.sass
```


#### Running Django's Built-In Development Server

```
./manage.py runserver <IP address>:8000
```


#### Some Other Notes About Development

- There is no need to collect static files in development.
(When DEBUG=True, Django finds static files dynamically across the apps.)



## Production

Here is a walkthrough of how I deployed this with Apache and modwsgi on Ubuntu.

This assumes that most sysadmin setup is already complete.
This sysadmin steps includes the following:

- installing Python and virtualenv
- installing Apache and modwsgi
- installing git
- installing MySQL
- creating a UNIX user for this project (named gunsiano)
- creating the project directory at /opt/local/gunsiano, owned by gunsiano
- creating a directory for data and backups at /volume/data1/project/gunsiano, owned by gunsiano
- creating a MySQL database (gunsiano)
- creating a MySQL read-write user (gunsiano) and a MySQL read-only user (gunsiano_ro)


#### Database

```
mysql -u gunsiano -p gunsiano < <sql dump filename>
```


#### Database Backups

```
mkdir /volume/data1/project/gunsiano/database_backups

mkdir /opt/local/gunsiano/secret
chmod 700 /opt/local/gunsiano/secret

touch /opt/local/gunsiano/secret/gunsiano.my.cnf
chmod 600 /opt/local/gunsiano/secret/gunsiano.my.cnf
vi /opt/local/gunsiano/secret/gunsiano.my.cnf
> [client]
> user = gunsiano_ro
> password = <password>

mkdir /opt/local/gunsiano/bin
chmod 775 /opt/local/gunsiano/bin

vi ~/.zshenv
> path=(/opt/local/gunsiano/bin $path)
source ~/.zshenv

touch /opt/local/gunsiano/bin/mysqldump_gunsiano
chmod 774 /opt/local/gunsiano/bin/mysqldump_gunsiano
vi /opt/local/gunsiano/bin/mysqldump_gunsiano
> #!/bin/sh
>
> /usr/bin/mysqldump --defaults-file=/opt/local/gunsiano/secret/gunsiano.my.cnf --single-transaction gunsiano | pbzip2 -c -p16 > /volume/data1/project/gunsiano/database_backups/gunsiano_`date +%Y-%m-%d_%H-%M-%S`.sql.bz2

crontab -e
> 0 4 * * 7 /opt/local/gunsiano/bin/mysqldump_gunsiano
```


#### Code

```
cd /opt/local/gunsiano
git clone https://github.com/katur/gunsiano.git

cd /opt/local/gunsiano/gunsiano/gunsiano
# add localsettings.py; make sure to set DEBUG=False
```


#### Dependencies

```
cd /opt/local/gunsiano
virtualenv --python=/usr/bin/python2.7 gunsianovirtualenv
# NOTE: This use of virtualenv hardcodes the name and location of the virtualenv dir.
# But the --relocatable arg has problems and is to be deprecated.
# So, to move or rename it, delete and recreate the virtualenv dir.

source /opt/local/gunsiano/gunsianovirtualenv/bin/activate
pip install -r /opt/local/gunsiano/gunsiano/requirements.txt
```


#### Static Files

```
source /opt/local/gunsiano/gunsianovirtualenv/bin/activate
cd /opt/local/gunsiano/gunsiano
./manage.py collectstatic
```


#### Apache Configuration

```
mkdir /opt/local/gunsiano/apache2

vi /opt/local/gunsiano/apache2/gunsiano.conf
# Add project-specific apache settings.
# Note that part of this configuration involves serving static files directly.
# Please see the above file, on pyxis, for details.

sudo ln -s /opt/local/gunsiano/apache2/gunsiano.conf /etc/apache2/sites-enabled/002-gunsiano.conf

sudo vi /etc/apache2/ports.conf
# Enable/add line to Listen 80
```


#### Apache Commands

```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```


#### Deploying Changes

#### *As project user...*
```
# Dump database and record the currently-deployed git commit,
# in case reverting is necessary

# Activate Python virtual environment
source /opt/local/gunsiano/gunsianovirtualenv/bin/activate

# Pull changes
cd /opt/local/gunsiano/gunsiano
git pull

# If changes to requirements.txt
pip install -r requirements.txt

# If new/changed static files
./manage.py collectstatic

# If new database migrations
./manage.py migrate

# If any scripts must be run
./manage.py scriptname

# If there are unit tests
./manage.py test
```

#### *As user with sudo...*
```
sudo service apache2 restart
```

If front-end changes, inspect visually.
