manage="${VENV}/bin/python ${INSTALLDIR}/${REPO}/manage.py"

$manage syncdb --noinput --migrate
$manage collectstatic --noinput

supervisorctl restart unicore_unicef_zambia
