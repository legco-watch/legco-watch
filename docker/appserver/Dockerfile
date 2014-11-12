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
COPY files/legco-watch.ini ${PROJECT_PATH}/legco-watch.ini

# Get the latest code
VOLUME ${PROJECT_PATH}
RUN git clone https://github.com/legco-watch/legco-watch.git ${PROJECT_PATH}

# Copy over configuration
COPY files/local.py ${PROJECT_PATH}/app/legcowatch/local.py

# uWSGI entrypoint
ENTRYPOINT ["/usr/local/bin/uwsgi", "--ini", "${PROJECT_PATH}/legco-watch.ini"]
