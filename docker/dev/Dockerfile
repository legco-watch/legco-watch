FROM legcowatch/appserver

# Set up the development environment
COPY files/.bashrc /root/.bashrc
COPY files/.profile /root/.profile

VOLUME /docker

ENTRYPOINT ["/bin/bash"]
EXPOSE 8000