Deploying gunsiano Project
======================
Here is a walkthrough of an Ubuntu deploy, using Apache
and modwsgi. WORK IN PROGRESS.


MySQL Database
--------------
```
mysql -u gunsiano -p gunsiano < <sql dump filename>
```

Code
----
```
cd /opt/local/gunsiano
git clone https://github.com/katur/gunsiano.git
cd /opt/local/gunsiano/gunsiano/gunsiano
# copy local_settings.py from development computer
# edit local_settings with database connection info, and set DEBUG=False
```

Virtual Environment and Dependencies
------------------------------------
```
cd /opt/local/gunsiano
virtualenv --python=/usr/bin/python2.7 gunsianovirtualenv
# NOTE: This use of virtualenv hardcodes the name and location of the
# virtualenv dir. But, the --relocatable arg has problems and is to be
# deprecated. So, to move or rename it, delete and recreate the virtualenv dir.
source gunsianovirtualenv/bin/activate
pip install -r gunsiano/requirements.txt
```

Running Django Built-in Development Server
------------------------------------------
```
source /opt/local/gunsiano/gunsianovirtualenv/bin/activate
/opt/local/gunsiano/gunsiano/manage.py runserver <IP address>:8000
```

Apache Configuration
--------------------
```
cd /opt/local/gunsiano
mkdir apache2
cd apache2
vi gunsiano.conf
# add project-specific apache settings, using port 8010
sudo ln -s /opt/local/gunsiano/apache2/gunsiano.conf /etc/apache2/sites-enabled/002-gunsiano.conf
cd /etc/apache2
vi ports.conf
# add line to Listen 8010.
# comment out line to Listen 80 if port 80 not being used
```

Apache Commands
---------------
```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```

Deploying (to be fleshed out and automated)
-------------------------------------------
```
### As user gunsiano...
# dump database, in case reverting is necessary
# record the currently-deployed git commit, in case reverting is necessary
cd /opt/local/gunsiano/gunsiano
source opt/local/gunsiano/gunsianovirtualenv/bin/activate
git pull
# if requirements.txt changed:
pip install -r requirements.txt
# if new database migrations:
./manage.py migrate
# if any scripts must be run, e.g. to modify data in keeping with schema changes:
./manage.py scriptname
# if unit tests:
./manage.py test

### As user katherine...
sudo service apache2 restart
# if front-end changes, visual inspection of site
# if necessary, revert the repo, db, and packages to the recorded versions.
```
