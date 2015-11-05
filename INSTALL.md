Installing gunsiano Project
===========================
Here is a walkthrough of an Ubuntu deploy, using Apache
and modwsgi. WORK IN PROGRESS.


Import MySQL Database
---------------------
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

Static Files
------------
```
source /opt/local/gunsiano/gunsianovirtualenv/bin/activate
cd /opt/local/gunsiano/gunsiano
./manage.py collectstatic
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
# add project-specific apache settings, using port 80 and ServerName directive
sudo ln -s /opt/local/gunsiano/apache2/gunsiano.conf /etc/apache2/sites-enabled/002-gunsiano.conf

sudo vi /etc/apache2/ports.conf
# add line to Listen 80
```

Apache Commands
---------------
```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```

Database Backups
----------------
```
mkdir /volume/data1/project/gunsiano/database_backups

mkdir /opt/local/gunsiano/secret
chmod 700 /opt/local/gunsiano/secret

touch /opt/local/gunsiano/secret/.gunsiano.my.cnf
chmod 600 /opt/local/gunsiano/secret/.gunsiano.my.cnf
vi /opt/local/gunsiano/secret/.gunsiano.my.cnf
> [client]
> user = gunsiano_ro
> password = <password>

mkdir /opt/local/gunsiano/bin
chmod 775 /opt/local/gunsiano/bin

vi ~/.profile
> PATH="/opt/local/gunsiano/bin:$PATH"
source ~/.profile

touch /opt/local/gunsiano/bin/mysqldump_gunsiano
chmod 774 /opt/local/gunsiano/bin/mysqldump_gunsiano
vi /opt/local/gunsiano/bin/mysqldump_gunsiano

> #!/bin/sh
>
> /usr/bin/mysqldump --defaults-file=/opt/local/gunsiano/secret/.gunsiano.my.cnf --single-transaction gunsiano | pbzip2 -c -p16 > /volume/data1/project/gunsiano/database_backups/gunsiano_`date +%Y-%m-%d_%H-%M-%S`.sql.bz2
```


Deploying in a Nutshell -- DRAFT
--------------------------------
### As user gunsiano

```
# dump database, in case reverting is necessary
# record the currently-deployed git commit, in case reverting is necessary

# Activate Python virtual environment
cd /opt/local/gunsiano/gunsiano
source opt/local/gunsiano/gunsianovirtualenv/bin/activate

# Pull changes
git pull

# If changes to requirements.txt:
pip install -r requirements.txt

# If new/changed static files:
./manage.py collectstatic

# If new database migrations:
./manage.py migrate

# If any scripts must be run:
./manage.py scriptname

# If there are unit tests:
./manage.py test
```

### As user with sudo
```
sudo service apache2 restart
```

If front-end changes, inspect visually.
