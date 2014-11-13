FROM legcowatch/base

# Environment variables
ENV VIRTUALENV_PATH /root/envs/appserver
ENV PROJECT_PATH /legcowatch

# Set up the virtualenv
RUN virtualenv ${VIRTUALENV_PATH}
COPY files/base_reqs.txt /tmp/
RUN ${VIRTUALENV_PATH}/bin/pip install -r /tmp/base_reqs.txt

# Install uWSGI
RUN ${VIRTUALENV_PATH}/bin/pip install uwsgi

# Get the latest code
RUN git clone https://github.com/legco-watch/legco-watch.git ${PROJECT_PATH}

# Set up the database
WORKDIR ${PROJECT_PATH}
run pwd
run ls -la
#RUN /bin/bash -c 'source ${VIRTUALENV_PATH}/bin/activate \
#    && python manage.py syncdb --noinput \
#    && python manage.py migrate --noinput \
#    && python manage.py collectstatic --noinput'

# Copy over configuration
#COPY files/local.py ${PROJECT_PATH}/app/legcowatch/local.py
#COPY files/legco-watch.ini ${PROJECT_PATH}/legco-watch.ini

# uWSGI entrypoint
#ENTRYPOINT ["${VIRTUALENV_PATH}/bin/uwsgi", "--ini", "${PROJECT_PATH}/legco-watch.ini"]
