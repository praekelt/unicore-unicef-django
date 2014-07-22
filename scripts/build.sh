#!/bin/bash

cp -a $REPO ./build/

${PIP} install https://github.com/praekelt/django-photologue/tarball/2.10.praekelt#egg=django-photologue
${PIP} install -r $REPO/requirements.pip

