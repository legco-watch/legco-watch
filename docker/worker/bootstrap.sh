#!/bin/bash

source ${VIRTUALENV_PATH}/bin/activate
export C_FORCE_ROOT="true"

echo "Pulling latest code and syncing database"
    # If no command passed in, then pull code, migrate, and run the uwsgi server
git pull --force

if [ $# -eq 0 ]
then
    cd app
    ${VIRTUALENV_PATH}/bin/celery -A legcowatch worker -l debug
else
    # This allows us to attach to the container
    exec "$@"

fi