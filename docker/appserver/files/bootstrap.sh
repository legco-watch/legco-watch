#!/bin/bash

source ${VIRTUALENV_PATH}/bin/activate
if [ $# -eq 0 ]
then
    # If no command passed in, then pull code, migrate, and run the uwsgi server
    git pull --force
    cd app
    python manage.py syncdb --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput

    ${VIRTUALENV_PATH}/bin/uwsgi --ini ${PROJECT_PATH}/legco-watch.ini
else
    # This allows us to attach to the container
    exec "$@"

fi