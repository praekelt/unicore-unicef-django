#!/bin/bash

sudo apt-get install python-virtualenv python2.7-dev \
libjpeg-dev zlib1g-dev build-essential git-core \
sqlite3 libproj0 libproj-dev libgeos-3.2.2 libgdal1-dev \
libgdal1-1.7.0 libspatialite3 spatialite-bin libgeoip1 libgeoip-dev --no-upgrade

echo "Setting up sandboxed Python environment with Python 2.7"
virtualenv ve

# We must do a custom build of pysqlite
ve/bin/pip install --no-install pysqlite==2.6.0
echo "[build_ext]\

#define=\

include_dirs=/usr/local/include\

library_dirs=/usr/local/lib\

libraries=sqlite3\

#define=SQLITE_OMIT_LOAD_EXTENSION" > ve/build/pysqlite/setup.cfg
ve/bin/pip install --no-download pysqlite==2.6.0
ve/bin/pip install -r requirements.pip

read -p "Create a superuser when prompted. Do not generate default content. [enter]" y

source ve/bin/activate && \
./manage.py syncdb && \
spatialite unicef_django.db "SELECT InitSpatialMetaData();" && \
./manage.py migrate && \
./manage.py load_photosizes && \
./manage.py collectstatic --noinput && \
./manage.py loaddata unicef/fixtures/sites.json


echo "You may now start up the site with ./manage.py runserver"
echo "Browse to http://localhost:8000/ for the public site."
echo "Browse to http://localhost:8000/admin for the admin interface."
