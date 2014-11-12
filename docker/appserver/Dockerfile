FROM legcowatch/base

# Environment variables
ENV VIRTUALENV_PATH /root/envs/appserver

# Set up the virtualenv
RUN virtualenv ${VIRTUALENV_PATH}
COPY files/base_reqs.txt /tmp/
RUN ${VIRTUALENV_PATH}/bin/pip install -r /tmp/base_reqs.txt
